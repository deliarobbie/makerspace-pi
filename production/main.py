import os

# Try loading .env if python-dotenv is available
try:
    from dotenv import load_dotenv
    _project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    load_dotenv(os.path.join(_project_root, ".env"))
    load_dotenv()
except ImportError:
    pass

from lights import set_lights, turn_off_lights
from rfid_reader import start_reader
from database import lookup_card


def process_card(card_id):
    card_id = card_id.lower().strip()

    print(f"\n--- Card scanned: {card_id} ---")

    response = lookup_card(card_id)

    if response is not None:
        status = response.get("status", "red").lower()
        message = response.get("message", "")
        user_info = response.get("user")
        name = (
            f" ({user_info.get('first_name', '')} {user_info.get('last_name', '')})"
            if user_info
            else ""
        )

        if status == "green":
            print(f"Status: GREEN{name} - {message}")
            set_lights(False, False, True)

        elif status == "yellow":
            print(f"Status: YELLOW{name} - {message}")
            set_lights(False, True, False)

        else:
            print(f"Status: RED{name} - {message}")
            set_lights(True, False, False)

    else:
        # Fallback if the webapp cannot be reached (offline mode)
        print("Notice: Webapp unreachable. Running offline card check...")
        if card_id == "44171ddc":
            print("Status: YELLOW (Offline Match)")
            set_lights(False, True, False)
        elif card_id in ("b34a339c", "b35dec2c"):
            print("Status: GREEN (Offline Match)")
            set_lights(False, False, True)
        else:
            print("Status: RED (Offline - Access Denied)")
            set_lights(True, False, False)

    turn_off_lights()


if __name__ == "__main__":
    print("Initializing RFID Traffic Controller...")

    turn_off_lights()  # Start with all lights off

    print("Ready! Scan an RFID card...")

    try:
        # Start RFID reader
        start_reader(process_card)

    except KeyboardInterrupt:
        print("\nShutting down...")
        turn_off_lights()