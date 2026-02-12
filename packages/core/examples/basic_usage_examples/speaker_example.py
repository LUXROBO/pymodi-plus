import modi_plus
import time

"""
Example script for the usage of speaker module
Make sure you connect 1 speaker module to your network module
"""

if __name__ == "__main__":
    bundle = modi_plus.MODIPlus()
    speak = bundle.speakers[0]

    speak.tune = 800, 70
    time.sleep(3)
    speak.frequency = 700
    time.sleep(3)
    speak.volume = 100
    time.sleep(1)
    speak.reset()
    time.sleep(1)
