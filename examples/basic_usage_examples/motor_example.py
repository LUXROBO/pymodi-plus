import modi_plus
import time

"""
Example script for the usage of motor module
Make sure you connect 1 motor module to your network module
"""

if __name__ == "__main__":
    bundle = modi_plus.MODIPlus()
    motor = bundle.motors[0]

    motor.angle = 0, 70
    time.sleep(3)
    motor.angle = 50, 70
    time.sleep(3)
    motor.speed = 50
    time.sleep(3)
    motor.speed = 100
    time.sleep(3)
    motor.speed = 0
    time.sleep(1)
