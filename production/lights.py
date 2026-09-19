import warnings
import time

# Suppress fallback warnings when lgpio/RPi.GPIO are not installed in the venv
try:
    from gpiozero.exc import PinFactoryFallback
    warnings.filterwarnings("ignore", category=PinFactoryFallback)
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

def turn_off_lights():
    time.sleep(2) # give it time to display to user
    red.value = False
    yellow.value = False
    green.value = False