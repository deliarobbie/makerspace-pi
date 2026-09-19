from lights import set_lights
from rfid_reader import start_reader


def process_card(card_id):
    card_id = card_id.lower().strip()

    print(f"Card scanned: {card_id}")

    # Logic based on card input:
    # 44171ddc -> Yellow
    # b34a339c, b35dec2c -> Green
    # Otherwise -> Red

    if card_id == "44171ddc":
        print("Status: YELLOW")
        set_lights(False, True, False)

    elif card_id in ("b34a339c", "b35dec2c"):
        print("Status: GREEN")
        set_lights(False, False, True)

    else:
        print("Status: RED (Access Denied / Unknown Card)")
        set_lights(True, False, False)


if __name__ == "__main__":
    print("Initializing RFID Traffic Controller...")

    set_lights(False, False, False)  # Start with all lights off

    print("Ready! Scan an RFID card...")

    try:
        # Start RFID reader
        start_reader(process_card)

    except KeyboardInterrupt:
        print("\nShutting down...")
        set_lights(False, False, False)