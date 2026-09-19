from gpiozero import LED

red = LED(10)
yellow = LED(9)
green = LED(11)


def set_lights(r_state, y_state, g_state):
    """Utility helper to set LED states directly."""
    red.value = r_state
    yellow.value = y_state
    green.value = g_state