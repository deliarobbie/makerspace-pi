import keyboard
import time
from gpiozero import LED

# --- GPIO Setup ---
# Matching pin numbers from your traffic setup
green = LED(25)
yellow = LED(7)
red = LED(8)

# --- Buffer & Listener Config ---
buffer = []
last_keypress = 0
TIMEOUT = 0.1  # Seconds between keystrokes before resetting the buffer

def set_lights(r_state, y_state, g_state):
    """Utility helper to set LED states directly."""
    red.value = r_state
    yellow.value = y_state
    green.value = g_state

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

def on_key(event):
    global buffer, last_keypress

    now = time.time()

    # Clear old buffer if keystrokes were too far apart
    if now - last_keypress > TIMEOUT:
        buffer.clear()

    last_keypress = now

    if event.event_type == keyboard.KEY_DOWN:
        if event.name == 'enter':
            card_id = ''.join(buffer)
            if card_id:
                process_card(card_id)
            buffer.clear()
        elif len(event.name) == 1:
            buffer.append(event.name)

if __name__ == "__main__":
    print("Initializing RFID Traffic Controller...")
    set_lights(False, False, False)  # Start with all lights off
    
    # Hook the keyboard event listener
    keyboard.hook(on_key)
    
    print("Ready! Scan an RFID card...")
    try:
        # Keep the script running
        keyboard.wait()
    except KeyboardInterrupt:
        print("\nShutting down...")
        set_lights(False, False, False)
