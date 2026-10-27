"""Hardware-free checks: python -m unittest discover -s scripts -p 'test_*.py'."""
import importlib.util
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest.mock import Mock, patch

ROOT = Path(__file__).resolve().parents[1]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CheckinTests(unittest.TestCase):
    def setUp(self):
        self.requests = types.ModuleType("requests")
        self.requests.RequestException = type("RequestException", (Exception,), {})
        self.requests.post = Mock()
        self.requests.get = Mock()
        self.dotenv = types.ModuleType("dotenv")
        self.dotenv.load_dotenv = Mock()
        self.dotenv.dotenv_values = Mock()
        self.dotenv.set_key = Mock()
        self.modules = patch.dict(sys.modules, {"requests": self.requests, "dotenv": self.dotenv})
        self.modules.start()
        self.addCleanup(self.modules.stop)
        self.db = load("reader_database", ROOT / "production/database.py")
        self.db.API_URL = "https://example.test/api/checkin"
        self.db.API_KEY = "test-key"

    def test_api_modes(self):
        self.requests.post.return_value.json.return_value = {"ok": True, "status": "green"}
        for mode in ("space", "equipment", "studio"):
            self.assertEqual(self.db.lookup_card("abc", mode, "7")["status"], "green")
            args, kwargs = self.requests.post.call_args
            self.assertEqual(args[0], self.db.API_URL + ("" if mode == "space" else f"/{mode}"))
            self.assertEqual(kwargs["json"], {"card_id": "abc", **({"resource_id": "7"} if mode != "space" else {})})

    def test_invalid_and_offline_responses(self):
        for result in ([], {}, {"status": "green", "ok": False}):
            self.requests.post.return_value.json.return_value = result
            self.assertIsNone(self.db.lookup_card("abc"))
        self.requests.post.side_effect = self.requests.RequestException("offline")
        self.assertIsNone(self.db.lookup_card("abc"))

    def test_menu_saves_database_id(self):
        setup = load("configure_role_test", ROOT / "scripts/configure_role.py")
        self.dotenv.dotenv_values.return_value = {"MAKERSPACE_API_URL": self.db.API_URL, "MAKERSPACE_API_KEY": "test-key"}
        self.requests.get.return_value.json.return_value = {"resources": [{"id": 42, "name": "Laser"}]}
        answers = iter(["2", "1"])
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / ".env"
            path.touch()
            setup.configure(path, lambda _: next(answers), lambda _: None)
        self.assertEqual(self.dotenv.set_key.call_args_list[-1].args[1:], ("MAKERSPACE_RESOURCE_ID", "42"))

    def test_menu_failure_preserves_assignment(self):
        setup = load("configure_role_failure", ROOT / "scripts/configure_role.py")
        self.dotenv.dotenv_values.return_value = {"MAKERSPACE_API_URL": self.db.API_URL, "MAKERSPACE_API_KEY": "test-key"}
        self.requests.get.side_effect = self.requests.RequestException("offline")
        with self.assertRaises(self.requests.RequestException):
            setup.configure(Path("unused.env"), lambda _: "3", lambda _: None)
        self.dotenv.set_key.assert_not_called()

    def test_controller_drives_lights_for_each_role(self):
        lights = types.ModuleType("lights")
        for name in ("set_lights", "turn_off_lights", "blink_error", "confirm_startup"):
            setattr(lights, name, Mock())
        reader = types.ModuleType("rfid_reader")
        def scan(callback, on_ready):
            on_ready()
            callback(" ABC ")
        reader.start_reader = scan
        for mode in ("space", "equipment", "studio"):
            with patch.dict(sys.modules, {"database": self.db, "lights": lights, "rfid_reader": reader}), patch.dict("os.environ", {"MAKERSPACE_RESOURCE_ID": "7"}):
                controller = load("controller_test", ROOT / "production/controller.py")
                controller.lookup_card = Mock(return_value={"ok": True, "status": "green"})
                with patch.object(controller.signal, "signal"):
                    controller.run(mode)
                controller.lookup_card.assert_called_once_with("abc", mode, "7")
                lights.set_lights.assert_called_with(False, False, True)


if __name__ == "__main__":
    unittest.main()
