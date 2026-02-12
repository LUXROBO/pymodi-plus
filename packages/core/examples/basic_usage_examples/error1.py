import modi_plus
import time

bundle = modi_plus.MODIPlus()

button = bundle.buttons[0]
led = bundle.leds[0]

mode = 0
while True:
    if button.double_clicked:
        break
    if button.clicked:
        mode = mode + 1
        if mode == 1:
            led.rgb = 20, 20, 20
        elif mode == 2:
            led.rgb = 60, 60, 60
        elif mode == 3:
            led.rgb = 100, 100, 100
        elif mode == 4:
            led.rgb = 0, 0, 0
            mode = 0
