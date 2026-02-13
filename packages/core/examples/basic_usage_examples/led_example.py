import modi_plus
import time

"""
Example script for the usage of led module
Make sure you connect 1 led module to your network module
"""

if __name__ == "__main__":
    bundle = modi_plus.MODIPlus()
    led = bundle.leds[0]

    led.blue = 100
    time.sleep(1)
    led.blue = 0
    time.sleep(1)
    led.green = 255
    time.sleep(1)
    led.green = 0
    time.sleep(1)
    led.red = 100
    time.sleep(1)
    for c in range(100):
        led.rgb = 100 - c, c, 0
        time.sleep(0.02)

    led.turn_on()
    time.sleep(1)
    led.turn_off()
    time.sleep(1)
