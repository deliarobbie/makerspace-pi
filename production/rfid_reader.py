import keyboard
import time

# Buffer & Listener Config
buffer = []
last_keypress = 0
TIMEOUT = 0.1  # Seconds between keystrokes before resetting the buffer


def start_reader(callback, on_ready=None):
    global buffer, last_keypress
    accepting_cards = False

    def on_key(event):
        global buffer, last_keypress

        if not accepting_cards:
            return

        now = time.time()

        # Clear old buffer if keystrokes were too far apart
        if now - last_keypress > TIMEOUT:
            buffer.clear()

        last_keypress = now

        if event.event_type == keyboard.KEY_DOWN:
            if event.name == 'enter':
                card_id = ''.join(buffer)

                if card_id:
                    callback(card_id)

                buffer.clear()

            elif len(event.name) == 1:
                buffer.append(event.name)

    # Hook the keyboard event listener
    hook = keyboard.hook(on_key)
    try:
        if on_ready is not None:
            on_ready()
        buffer.clear()
        last_keypress = 0
        accepting_cards = True
        # Keep the reader running
        keyboard.wait()
    finally:
        keyboard.unhook(hook)
