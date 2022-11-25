import modi_plus
import time

"""
Example script for the usage of battery module
Make sure you connect 1 battery module to your
network module
"""

if __name__ == "__main__":
    bundle = modi_plus.MODIPlus()
    battery = bundle.batterys[0]

    while True:
        print(f"level(%): {battery.level:<10}", end="\r")
        time.sleep(0.02)
