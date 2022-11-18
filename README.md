Description
===========
> Python API for controlling modular electronics, MODI+.


Features
--------
PyMODI+ provides a control of modular electronics.
* Platform agnostic control of modules through serial connection
* Utilities of wireless connection with BLE (Bluetooth Low Engery)

Installation
------------
> When installing PyMODI+ package, we highly recommend you to use Anaconda to manage the distribution.
> With Anaconda, you can use an isolated virtual environment, solely for PyMODI+.

[Optional] Once you install [Anaconda](https://docs.anaconda.com/anaconda/install/), then:
```
# Install new python environment for PyMODI+ package, choose python version >= 3.9
conda create --name pymodi_plus python=3.9

# After you properly install the python environment, activate it
conda activate pymodi_plus

# Ensure that your python version is compatible with PyMODI+
python --version
```

Install the latest PyMODI+ if you haven't installed it yet:
```
python -m pip install pymodi_plus --user --upgrade
```

Usage
-----
Import modi_plus package and create MODIPlus object (we call it "bundle", a bundle of MODI+ modules).
```python
# Import modi_plus package
import modi_plus

"""
Create MODIPlus object, make sure that you have connected your network module
to your machine while other modules are attached to the network module
"""
bundle = modi_plus.MODIPlus()
```

[Optional] Specify how you would like to establish the connection between your machine and the network module.
```python
# 1. Serial connection (via USB), it's the default connection method
bundle = modi_plus.MODIPlus(connection_type="serialport")

# 2. BLE (Bluetooth Low Energy) connection, it's wireless! But it can be slow :(
bundle = modi_plus.MODIPlus(conn_type="ble", network_uuid="YOUR_NETWORK_MODULE_UUID")
```

List and create connected modules' object.
```python
# List connected modules
print(bundle.modules)

# List connected leds
print(bundle.leds)

# Pick the first led object from the bundle
led = bundle.leds[0]
```

Let's blink the LED 5 times.
```python
import time

for _ in range(5):
    # turn on for 0.5 second
    led.turn_on()
    time.sleep(0.5)

    # turn off for 0.5 second
    led.turn_off()
    time.sleep(0.5)
```

If you are still not sure how to use PyMODI, you can play PyMODI tutorial over REPL:
```
$ python -m modi_plus --tutorial
```
As well as an interactive usage examples:
```
$ python -m modi_plus --usage
```

Additional Usage
----------------
To diagnose MODI+ modules (helpful to find existing malfunctioning modules),
```
$ python -m modi_plus --inspect
```

To initialize MODI+ modules implicitly (set `i` flag to enable REPL mode),
```
$ python -im modi_plus --initialize
```

To see what other commands are available,
```
$ python -m modi_plus --help
```
