import modi_plus
import time

"""
Example script for the usage of imu module
Make sure you connect 1 imu module to your network module
"""

if __name__ == "__main__":
    bundle = modi_plus.MODIPlus()
    imu = bundle.imus[0]

    while True:
        print(f"Angle_y: {imu.angle_y:<10}"
              f"Angle_x: {imu.angle_x:<10}"
              f"Angle_z: {imu.angle_z:<10}"
              f"Vel x: {imu.angular_vel_x:<10}"
              f"Vel y: {imu.angular_vel_y:<10}"
              f"Vel z: {imu.angular_vel_z:<10}"
              f"Acc x: {imu.acceleration_x:<10}"
              f"Acc y: {imu.acceleration_y:<10}"
              f"Acc z: {imu.acceleration_z:<10}", end="\r")
        time.sleep(0.02)
