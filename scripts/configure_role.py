"""Interactive assignment; commit the role only after all choices validate."""
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

import requests
from dotenv import dotenv_values, set_key


def choose(prompt, count, read, write):
    while True:
        value = read(prompt)
        if value.isascii() and value.isdecimal() and 1 <= int(value) <= count:
            return int(value) - 1
        write("Choose a displayed menu number.\n")


def configure(path, read, write):
    values = dotenv_values(path)
    saved_mode = values.get("MAKERSPACE_MODE")
    saved_resource = values.get("MAKERSPACE_RESOURCE_ID", "")
    if saved_mode in ("space", "equipment", "studio"):
        write(f"Current assignment: {saved_mode}, resource {saved_resource or 'none'}\n")
        if choose("1) Keep assignment\n2) Change assignment\nChoice: ", 2, read, write) == 0:
            if saved_mode == "space" or (saved_resource.isascii() and saved_resource.isdecimal() and int(saved_resource) > 0):
                return
            write("Saved resource ID is invalid; choose a new assignment.\n")

    mode = ("space", "equipment", "studio")[choose(
        "1) Space membership\n2) Equipment reservation\n3) Studio rental\nChoice: ", 3, read, write)]
    resource_id = ""
    if mode != "space":
        parsed = urlsplit(values.get("MAKERSPACE_API_URL", ""))
        if parsed.scheme not in ("http", "https") or not parsed.netloc or not values.get("MAKERSPACE_API_KEY"):
            raise ValueError("Configure the API URL and key first")
        url = urlunsplit((parsed.scheme, parsed.netloc, "/api/rfid/resources", "", ""))
        response = requests.get(url, params={"mode": mode},
                                headers={"Authorization": f"Bearer {values['MAKERSPACE_API_KEY']}"}, timeout=10)
        response.raise_for_status()
        resources = response.json().get("resources")
        if not isinstance(resources, list) or not resources:
            raise ValueError("No resources available")
        rows = []
        for index, resource in enumerate(resources, 1):
            if not isinstance(resource, dict) or not str(resource.get("id", "")).isascii() or not str(resource.get("id", "")).isdecimal() or int(resource["id"]) <= 0:
                raise ValueError("Invalid resource menu response")
            rows.append((str(index), resource.get('name') or 'Unnamed', resource.get('type') or 'Unspecified', str(resource['id'])))
        label = "Machine" if mode == "equipment" else "Studio"
        headers = ("#", label, "Type", "ID")
        widths = [max(len(str(row[column])) for row in [headers, *rows]) for column in range(4)]
        write(f"\n{mode.upper()} CHECK-IN\n")
        for row in [headers, tuple("-" * width for width in widths), *rows]:
            write("  ".join(str(value).ljust(width) for value, width in zip(row, widths)).rstrip() + "\n")
        selected = resources[choose(f"Select a {label.lower()}: ", len(resources), read, write)]
        resource_id = str(selected["id"])
    path.chmod(0o600)
    set_key(str(path), "MAKERSPACE_MODE", mode)
    set_key(str(path), "MAKERSPACE_RESOURCE_ID", resource_id)
    write(f"Saved assignment: {mode}, resource {resource_id or 'none'}\n")


def main():
    path = Path(__file__).resolve().parents[1] / ".env"
    with open("/dev/tty", "r") as terminal_input, open("/dev/tty", "w", buffering=1) as terminal_output:
        def read(message):
            terminal_output.write(message)
            value = terminal_input.readline()
            if not value:
                raise ValueError("Setup cancelled")
            return value.strip()
        try:
            configure(path, read, terminal_output.write)
        except (requests.RequestException, ValueError, AttributeError) as error:
            raise SystemExit(f"Assignment failed ({type(error).__name__}). Check API deployment, credentials, and available resources; rerun setup. Existing assignment unchanged.") from None


if __name__ == "__main__":
    main()
