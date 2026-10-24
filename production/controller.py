import os
import signal

from database import lookup_card


def run(mode):
    resource_id = os.environ.get("MAKERSPACE_RESOURCE_ID", "")
    if mode != "space" and (not resource_id.isascii() or not resource_id.isdecimal() or int(resource_id) <= 0):
        raise SystemExit("Configure a positive MAKERSPACE_RESOURCE_ID using bash setup.sh")

    from lights import set_lights, turn_off_lights, blink_error, confirm_startup
    from rfid_reader import start_reader

    def process_card(card_id):
        try:
            response = lookup_card(card_id.strip().lower(), mode, resource_id)
            if response is None:
                print("Check-in failed: API unavailable or invalid response")
                blink_error()
                return
            status = response["status"]
            print(f"Status: {status.upper()} - {response.get('message', '')}")
            set_lights(status == "red", status == "yellow", status == "green")
        finally:
            turn_off_lights()

    def ready():
        confirm_startup()
        print(f"Ready: {mode}, resource {resource_id or 'none'}. Scan an RFID card...")

    def stop(_signum, _frame):
        raise KeyboardInterrupt

    signal.signal(signal.SIGTERM, stop)
    turn_off_lights()
    try:
        start_reader(process_card, on_ready=ready)
    except KeyboardInterrupt:
        print("Shutting down...")
    finally:
        turn_off_lights()
