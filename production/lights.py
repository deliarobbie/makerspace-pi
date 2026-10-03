import warnings
import time

# Suppress fallback warnings when lgpio/RPi.GPIO are not installed in the venv
try:
    from gpiozero.exc import PinFactoryFallback
    warnings.filterwarnings("ignore", category=PinFactoryFallback)
    from gpiozero.exc import NativePinFactoryFallback
    warnings.filterwarnings("ignore", category=NativePinFactoryFallback)
except ImportError:
    pass

from gpiozero import LED

red = LED(9)
yellow = LED(10)
green = LED(11)


def set_lights(r_state, y_state, g_state):
    """Utility helper to set LED states directly."""
    red.value = r_state
    yellow.value = y_state
    green.value = g_state
    time.sleep(2) # give it time to display to user

def set_lights_quick(r_state, y_state, g_state):
    """Utility helper to set LED states directly."""
    red.value = r_state
    yellow.value = y_state
    green.value = g_state

def turn_off_lights():
    red.value = False
    yellow.value = False
    green.value = False

def blink_error():
    for i in range(3):
        set_lights_quick(True, False, False)
        time.sleep(.5)
        turn_off_lights()
        time.sleep(.5)


def confirm_startup():
    """Repeat R-Y-G-R-Y-G three times, then blink all LEDs twice."""
    sequence = ((True, False, False), (False, True, False), (False, False, True))
    try:
        for _ in range(2):
            for states in sequence * 2:
                set_lights_quick(*states)
                time.sleep(.1)
        turn_off_lights()
        time.sleep(.1)
        for _ in range(2):
            set_lights_quick(True, True, True)
            time.sleep(.1)
            turn_off_lights()
            time.sleep(.1)
    finally:
        turn_off_lights()
