import modi_plus
import time

"""
Example script for the usage of motor module
Make sure you connect 1 motor module to your network module
"""

if __name__ == "__main__":
    bundle = modi_plus.MODI()
    motor = bundle.motors[0]

    motor.set_angle(0, 70)
    time.sleep(3)
    motor.set_angle(50, 70)
    time.sleep(3)
    motor.set_speed(50)
    time.sleep(3)
    motor.set_speed(100)
    time.sleep(3)
    motor.set_speed(0)
    time.sleep(1)
