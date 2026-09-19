from gpiozero import LED

red = LED(9)
yellow = LED(10)
green = LED(11)


def set_lights(r_state, y_state, g_state):
    """Utility helper to set LED states directly."""
    red.value = r_state
    yellow.value = y_state
    green.value = g_state