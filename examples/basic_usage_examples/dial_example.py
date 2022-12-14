import modi_plus
import time

"""
Example script for the usage of dial module
Make sure you connect 1 dial module and 1 speaker module to your network module
"""

if __name__ == "__main__":
    bundle = modi_plus.MODIPlus()
    dial = bundle.dials[0]
    speak = bundle.speakers[0]

    while True:
        speak.tune = "DO6", dial.turn
        time.sleep(0.02)
