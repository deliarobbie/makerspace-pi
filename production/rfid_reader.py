import keyboard
import time

# Buffer & Listener Config
buffer = []
last_keypress = 0
TIMEOUT = 0.1  # Seconds between keystrokes before resetting the buffer


def start_reader(callback):
    global buffer, last_keypress

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
                    callback(card_id)

                buffer.clear()

            elif len(event.name) == 1:
                buffer.append(event.name)

    # Hook the keyboard event listener
    keyboard.hook(on_key)

    # Keep the reader running
    keyboard.wait()