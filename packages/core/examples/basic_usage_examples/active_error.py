import modi_plus
import time
bundle=modi_plus.MODIPlus()

led=bundle.leds[0]
time.sleep(3)
led.red=255
time.sleep(3)
led.red=0
time.sleep(1)

led.green=100
time.sleep(3)
led.green=0
time.sleep(1)

led.blue=100
time.sleep(3)
led.blue=0
time.sleep(1)

led.turn_on()
time.sleep(2)
led.turn_off()
time.sleep(1)

led.rgb=(100, 0, 100)
time.sleep(2)
led.turn_off()
