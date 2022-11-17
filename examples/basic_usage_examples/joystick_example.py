import modi_plus

"""
Example script for the usage of joystick module
Make sure you connect 1 joystick module to your network module
"""

if __name__ == "__main__":
    bundle = modi_plus.MODIPlus()
    joystick = bundle.joysticks[0]

    while True:
        print("x: {0:<10} y: {1:<10} direction: {2:<10}".format(joystick.x, joystick.y, joystick.direction), end="\r")
