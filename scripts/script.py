import keyboard
import time
import pyautogui
import random

buffer = []
last_keypress = 0
TIMEOUT = 0.1  # seconds between chars before we consider it a new scan

# reading rfid keyboard inputs
def on_key(event):
    global buffer, last_keypress

    now = time.time()

    # If gap too long, it's a new scan — clear old buffer
    if now - last_keypress > TIMEOUT:
        buffer.clear()

    last_keypress = now

    if event.event_type == keyboard.KEY_DOWN:
        if event.name == 'enter':
            # Full scan received — process it
            card_id = ''.join(buffer)
            if card_id:
                process_card(card_id)
            buffer.clear()
        elif len(event.name) == 1:
            buffer.append(event.name)

def process_card(card_id):
    print(f"Card scanned: {card_id}")
    # do your lookup / action here

# TESTING, generating them without reader

def generate_hex(length=8):
    """Generate a random hex string of given length."""
    return ''.join(random.choices('0123456789ABCDEF', k=length))

def type_hex():

    # Give yourself time to click into the target window
    print("Switching focus in 3 seconds...")
    time.sleep(3)
    hex_value = generate_hex()
    print(f"Generated: {hex_value}")

    # Type it out
    pyautogui.typewrite(hex_value, interval=0.05)



