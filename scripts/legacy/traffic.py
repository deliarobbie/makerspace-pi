from gpiozero import Button, LED
import time

button = Button(21)
green = LED(25)
yellow = LED(7)
red = LED(8)

active = green

def traffic():
    redLight(red,yellow,green)
    time.sleep(5)
    greenLight(red,yellow,green)
#global active

#active.on()
#button.wait_for_press()
#if active == green:
#   redLight(red, yellow, green)
#   active = red
#elif active == red:
#   greenLight(red, yellow, green)
#   active = green
#   
def redLight(red, yellow, green):
    time.sleep(1)
    green.off()
    yellow.on()
    time.sleep(1)
    yellow.off()
    red.on()
    time.sleep(1)

def greenLight(red, yellow, green):
    time.sleep(1)
    red.off()
    yellow.on()
    time.sleep(1)
    yellow.off()
    green.on()
    time.sleep(1)
    
if __name__ == "__main__":
    traffic()
