from gpiozero import LED

green = LED(25)
yellow = LED(7)
red = LED(8)


def set_lights(r_state, y_state, g_state):
    """Utility helper to set LED states directly."""
    red.value = r_state
    yellow.value = y_state
    green.value = g_state