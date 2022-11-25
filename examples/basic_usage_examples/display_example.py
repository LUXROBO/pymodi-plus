import modi_plus
import time

"""
Example script for the usage of display module
Make sure you connect 1 display module to your network module
"""

if __name__ == "__main__":
    bundle = modi_plus.MODIPlus()
    display = bundle.displays[0]

    display.text = "Bouncing ball simulation..."
    time.sleep(3)

    vel = (1, 1)
    pos = (20, 30)

    for i in range(500):
        display.write_variable(0, pos[0], pos[1])
        pos = (pos[0] + vel[0], pos[1] + vel[1])
        if pos[0] < 0 or pos[0] > 40:
            vel = (-vel[0], vel[1])
        if pos[1] < 0 or pos[1] > 60:
            vel = (vel[0], -vel[1])
        if pos[1] < 0:
            pos = (pos[0], 0)
        if pos[0] < 0:
            pos = (0, pos[1])
        time.sleep(0.02)

    display.reset()
    time.sleep(2)
