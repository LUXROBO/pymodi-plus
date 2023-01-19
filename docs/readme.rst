.. container::

   |Python Versions| |PyPI Release (latest by date)| |Read the Docs
   (version)| |GitHub Workflow Status (Build)| |GitHub LICENSE| |Lines
   of Code|

Description
===========

   Python API for controlling modular electronics, MODI+.

Features
--------

PyMODI+ provides a control of modular electronics. \* Platform agnostic
control of modules through serial connection \* Utilities of wireless
connection with BLE (Bluetooth Low Engery)

Build Status
------------

+-----------------------------------+-----------------------------------+
| master                            | develop                           |
+===================================+===================================+
| |GitHub Workflow Status|          | |image1|                          |
+-----------------------------------+-----------------------------------+

System Support
--------------

+-----------+-----------+-----------+-----------+-----------+-----------+
| System    | 3.7       | 3.8       | 3.9       | 3.10      | 3.11      |
+===========+===========+===========+===========+===========+===========+
| Linux     | |GitHub   | |GitHub   | |GitHub   | |GitHub   | |GitHub   |
|           | Workflow  | Workflow  | Workflow  | Workflow  | Workflow  |
|           | Status    | Status    | Status    | Status    | Status    |
|           | (branch)| | (branch)| | (branch)| | (branch)| | (branch)| |
+-----------+-----------+-----------+-----------+-----------+-----------+
| Mac OS    | |image2|  | |image3|  | |image4|  | |image5|  | |image6|  |
+-----------+-----------+-----------+-----------+-----------+-----------+
| Windows   | |image7|  | |image8|  | |image9|  | |image10| | |image11| |
+-----------+-----------+-----------+-----------+-----------+-----------+

Contribution Guidelines
-----------------------

We appreciate all contributions. If you are planning to report bugs,
please do so `here <https://github.com/LUXROBO/pymodi/issues>`__. Feel
free to fork our repository to your local environment, and please send
us feedback by filing an issue.

If you want to contribute to pymodi, be sure to review the contribution
guidelines. This project adheres to pymodi’s code of conduct. By
participating, you are expected to uphold this code.

|Contributor Covenant|

Installation
------------

   When installing PyMODI+ package, we highly recommend you to use
   Anaconda to manage the distribution. With Anaconda, you can use an
   isolated virtual environment, solely for PyMODI+.

[Optional] Once you install
`Anaconda <https://docs.anaconda.com/anaconda/install/>`__, then:

::

   # Install new python environment for PyMODI+ package, choose python version >= 3.7
   conda create --name pymodi_plus python=3.7

   # After you properly install the python environment, activate it
   conda activate pymodi_plus

   # Ensure that your python version is compatible with PyMODI+
   python --version

Install the latest PyMODI+ if you haven’t installed it yet:

::

   python -m pip install pymodi-plus --user --upgrade

Usage
-----

Import modi_plus package and create MODIPlus object (we call it
“bundle”, a bundle of MODI+ modules).

.. code:: python

   # Import modi_plus package
   import modi_plus

   """
   Create MODIPlus object, make sure that you have connected your network module
   to your machine while other modules are attached to the network module
   """
   bundle = modi_plus.MODIPlus()

[Optional] Specify how you would like to establish the connection
between your machine and the network module.

.. code:: python

   # 1. Serial connection (via USB), it's the default connection method
   bundle = modi_plus.MODIPlus(connection_type="serialport")

   # 2. BLE (Bluetooth Low Energy) connection, it's wireless! But it can be slow :(
   bundle = modi_plus.MODIPlus(conn_type="ble", network_uuid="YOUR_NETWORK_MODULE_UUID")

List and create connected modules’ object.

.. code:: python

   # List connected modules
   print(bundle.modules)

   # List connected leds
   print(bundle.leds)

   # Pick the first led object from the bundle
   led = bundle.leds[0]

Let’s blink the LED 5 times.

.. code:: python

   import time

   for _ in range(5):
       # turn on for 0.5 second
       led.turn_on()
       time.sleep(0.5)

       # turn off for 0.5 second
       led.turn_off()
       time.sleep(0.5)

If you are still not sure how to use PyMODI, you can play PyMODI
tutorial over REPL:

::

   $ python -m modi_plus --tutorial

As well as an interactive usage examples:

::

   $ python -m modi_plus --usage

Additional Usage
----------------

To diagnose MODI+ modules (helpful to find existing malfunctioning
modules),

::

   $ python -m modi_plus --inspect

To initialize MODI+ modules implicitly (set ``i`` flag to enable REPL
mode),

::

   $ python -im modi_plus --initialize

To see what other commands are available,

::

   $ python -m modi_plus --help

.. |Python Versions| image:: https://img.shields.io/pypi/pyversions/pymodi-plus.svg?style=flat-square
   :target: https://pypi.python.org/pypi/pymodi-plus
.. |PyPI Release (latest by date)| image:: https://img.shields.io/github/v/release/LUXROBO/pymodi-plus?style=flat-square
   :target: https://pypi.python.org/pypi/pymodi-plus
.. |Read the Docs (version)| image:: https://img.shields.io/readthedocs/pymodi-plus/latest?style=flat-square
   :target: https://pymodi-plus.readthedocs.io/en/latest/?badge=master
.. |GitHub Workflow Status (Build)| image:: https://img.shields.io/github/actions/workflow/status/LUXROBO/pymodi-plus/build.yml?branch=master
   :target: https://github.com/LUXROBO/pymodi-plus/actions
.. |GitHub LICENSE| image:: https://img.shields.io/github/license/LUXROBO/pymodi-plus?style=flat-square&color=blue
   :target: https://github.com/LUXROBO/pymodi-plus/blob/master/LICENSE
.. |Lines of Code| image:: https://img.shields.io/tokei/lines/github/LUXROBO/pymodi-plus?style=flat-square
   :target: https://github.com/LUXROBO/pymodi-plus/tree/master/modi_plus
.. |GitHub Workflow Status| image:: https://img.shields.io/github/actions/workflow/status/LUXROBO/pymodi-plus/build.yml?branch=master
   :target: https://github.com/LUXROBO/pymodi-plus/actions
.. |image1| image:: https://img.shields.io/github/actions/workflow/status/LUXROBO/pymodi-plus/build.yml?branch=develop
   :target: https://github.com/LUXROBO/pymodi-plus/actions
.. |GitHub Workflow Status (branch)| image:: https://img.shields.io/github/actions/workflow/status/LUXROBO/pymodi-plus/unit_test_ubuntu.yml?branch=master
   :target: https://github.com/LUXROBO/pymodi-plus/actions
.. |image2| image:: https://img.shields.io/github/actions/workflow/status/LUXROBO/pymodi-plus/unit_test_macos.yml?branch=master
   :target: https://github.com/LUXROBO/pymodi-plus/actions
.. |image3| image:: https://img.shields.io/github/actions/workflow/status/LUXROBO/pymodi-plus/unit_test_macos.yml?branch=master
   :target: https://github.com/LUXROBO/pymodi-plus/actions
.. |image4| image:: https://img.shields.io/github/actions/workflow/status/LUXROBO/pymodi-plus/unit_test_macos.yml?branch=master
   :target: https://github.com/LUXROBO/pymodi-plus/actions
.. |image5| image:: https://img.shields.io/github/actions/workflow/status/LUXROBO/pymodi-plus/unit_test_macos.yml?branch=master
   :target: https://github.com/LUXROBO/pymodi-plus/actions
.. |image6| image:: https://img.shields.io/github/actions/workflow/status/LUXROBO/pymodi-plus/unit_test_macos.yml?branch=master
   :target: https://github.com/LUXROBO/pymodi-plus/actions
.. |image7| image:: https://img.shields.io/github/actions/workflow/status/LUXROBO/pymodi-plus/unit_test_windows.yml?branch=master
   :target: https://github.com/LUXROBO/pymodi-plus/actions
.. |image8| image:: https://img.shields.io/github/actions/workflow/status/LUXROBO/pymodi-plus/unit_test_windows.yml?branch=master
   :target: https://github.com/LUXROBO/pymodi-plus/actions
.. |image9| image:: https://img.shields.io/github/actions/workflow/status/LUXROBO/pymodi-plus/unit_test_windows.yml?branch=master
   :target: https://github.com/LUXROBO/pymodi-plus/actions
.. |image10| image:: https://img.shields.io/github/actions/workflow/status/LUXROBO/pymodi-plus/unit_test_windows.yml?branch=master
   :target: https://github.com/LUXROBO/pymodi-plus/actions
.. |image11| image:: https://img.shields.io/github/actions/workflow/status/LUXROBO/pymodi-plus/unit_test_windows.yml?branch=master
   :target: https://github.com/LUXROBO/pymodi-plus/actions
.. |Contributor Covenant| image:: https://img.shields.io/badge/Contributor%20Covenant-v2.0%20adopted-ff69b4.svg?style=flat-square
   :target: CODE_OF_CONDUCT.md
