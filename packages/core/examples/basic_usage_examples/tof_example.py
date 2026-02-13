import modi_plus
import time

"""
Example script for the usage of tof module
Make sure you connect 1 tof module to your network module
"""

if __name__ == "__main__":
    bundle = modi_plus.MODIPlus()
    tof = bundle.tofs[0]

    while True:
        print(f"Distance(cm): {tof.distance:<10}                ", end="\r")
        time.sleep(0.02)
