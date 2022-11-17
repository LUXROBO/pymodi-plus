import modi_plus

"""
This example explains the convention that pymodi uses when multiple modules
with the same type are connected.

When multiple modules are connected, the modules are sorted in ascending connected time.
"""

# Let say you run the code below, then one of the four cases below will occur
if __name__ == "__main__":
    bundle = modi_plus.MODIPlus()
    led0 = bundle.leds[0]
    led1 = bundle.leds[1]

"""
It is also possible to access modules by there id or uuid.

led0 = bundle.leds.get(0x881)
led1 = bundle.leds.get(0xA55)

or

led0 = bundle.led(0x40207D214881)
led1 = bundle.led(0x40207D214A55)
"""
