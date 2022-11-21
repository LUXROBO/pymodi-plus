import modi_plus
import time

"""
Example script for the usage of led module
Make sure you connect 1 led module to your network module
"""

if __name__ == "__main__":
    bundle = modi_plus.MODIPlus()
    led = bundle.leds[0]

    led.set_rgb(0, 0, 255)
    time.sleep(3)
    led.set_rgb(0, 0, 0)
    time.sleep(1)
    led.set_rgb(0, 255, 0)
    time.sleep(3)
    led.set_rgb(0, 0, 0)
    time.sleep(1)
    led.set_rgb(255, 0, 0)
    time.sleep(3)
    for c in range(255):
        led.set_rgb(255 - c, c, 0)
        time.sleep(0.02)

    led.turn_on()
    time.sleep(2)
    led.turn_off()
    time.sleep(1)
