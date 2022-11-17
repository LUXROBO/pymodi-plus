Usage
=====

To use pyMODI+ in a project::

    import modi_plus

Connect MODI+ modules to your device, and make a MODIPlus object.::

    bundle = modi_plus.MODIPlus()

You can access the modules by::

    bundle.modules

You can also access specific module by::

    bundle.<your_module_name>[0]

The following example code will blink LED module for 10 times::

    import modi_plus
    import time

    if __name__ == '__main__':
        bundle = modi_plus.MODIPlus(1)
        led = bundle.leds[0]

        for i in range(10):
            led.set_blue(255)
            time.sleep(0.5)
            led.set_off()
            time.sleep(0.5)

Enjoy your unique MODI+ experiences!!


