import time

import modi_plus

"""
Example script for the usage of button module
Make sure you connect 1 button module to your
network module
"""

if __name__ == "__main__":
    bundle = modi_plus.MODIPlus()

    input()

    # button0 = bundle.buttons[0]
    # motor0 = bundle.motors[0]
    # led0 = bundle.leds[0]
    # dial0 = bundle.dials[0]
    # joystick0 = bundle.joysticks[0]
    # tof0 = bundle.tofs[0]
    # imu0 = bundle.imus[0]
    # display0 = bundle.displays[0]
    speaker0 = bundle.speakers[0]
    env0 = bundle.envs[0]

    while True:
        # print(f"pressed:{button0.pressed},\tclicked:{button0.clicked},\tdouble clicked:{button0.double_clicked},\ttoggled:{button0.toggled}      ", end="\n") 
        # print(f"current angle:{motor0.angle},\tcurrent speed:{motor0.speed},\ttarget angle:{motor0.target_angle},\ttarget_speed:{motor0.target_speed}      ", end="\r")
        # print(f"turn:{dial0.turn},\tturn_speed:{dial0.speed}")
        # print(f"red:{led0.red},\tgreen:{led0.green},\tblue:{led0.blue}")
        # print(f"x:{joystick0.x}, y:{joystick0.y}")
        # print(f"distance:{tof0.distance}")
        # print(f"roll:{imu0.roll},\tpitch:{imu0.pitch},\tyaw:{imu0.yaw}")
        # print(f"roll pitch yaw :{imu0.angle}")
        print(f"temperature:{env0.temperature},\thumidity:{env0.humidity},\tintensity:{env0.intensity},\tvolume:{env0.volume}")

        if env0.intensity > 20:
            speaker0.play_music(1, 100, "car.wav")
        else:
            speaker0.play_music(0, 100, "car.wav")

        time.sleep(0.02)
