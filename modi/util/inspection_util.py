import os
import time

import threading as th

from textwrap import fill
from textwrap import dedent


class StoppableThread(th.Thread):

    def __init__(self, module, method):
        super(StoppableThread, self).__init__(daemon=True)
        self._stop = th.Event()
        self._module = module
        self._method = method

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    def run(self):
        while True:
            prop = eval(f"self._module.{self._method}")
            print(f"\rObtained property value: {prop} ", end="")
            time.sleep(0.1)


class Inspector:
    """
    Inspector diagnoses malfunctioning STM32 modules (all modules but network)
    """

    row_len = 79

    def __init__(self):
        self.bundle = None

    @staticmethod
    def clear():
        clear_cmd = 'cls' if os.name == 'nt' else 'clear'
        os.system(clear_cmd)

    def print_wrap(self, msg):
        message = fill(dedent(msg), self.row_len).lstrip()
        print(message)

    def print_module_page(self, module, i, nb_modules):
        print('-' * self.row_len)
        module_to_inspect = \
            f"| {' ' * 5} Diagnosing {module.module_type} ({module.id})"
        progress_indicator = f"({i + 1} / {nb_modules}) {' ' * 5} |"
        ls = f"{module_to_inspect:<{self.row_len}}"
        s = progress_indicator.join(
            ls.rsplit(' ' * len(progress_indicator), 1)
        )
        print(s)
        print('-' * self.row_len)

    def inspect(self, module, i, nb_modules):
        self.print_module_page(module, i, nb_modules)

        inspect_module = {
            # inspection method for setup modules
            "battery": self.inspect_battery,

            # inspection method for input modules
            "env": self.inspect_env,
            "imu": self.inspect_imu,
            "button": self.inspect_button,
            "dial": self.inspect_dial,
            "joystick": self.inspect_joystick,
            "tof": self.inspect_tof,

            # inspection method for input modules
            "display": self.inspect_display,
            "led": self.inspect_led,
            "motor_a": self.inspect_motor_a,
            "motor_b": self.inspect_motor_b,
            "speaker": self.inspect_speaker,
        }.get(module.module_type)
        inspect_module(module, i, nb_modules)

        self.clear()

    def inspect_battery(self, battery, i, nb_modules):
        self.print_wrap(
            """
            Battery module has level as its property.
            """
        )
        input("\nIf you are ready to inspect this module, Press ENTER: ")
        self.clear()

        self.print_module_page(battery, i, nb_modules)
        print("If the level shown below seems correct, press ENTER: \n")
        t = StoppableThread(battery, "level")
        t.start()
        input()
        t.stop()
        self.clear()

    def inspect_env(self, env, i, nb_moudles):
        self.print_wrap(
            """
            Environment module has intensicy, temperature, humidity, volume as its
            property.
            """
        )
        input("\nIf you are ready to inspect this module, Press ENTER: ")
        self.clear()

        self.print_module_page(env, i, nb_modules)
        print("If the intensicy shown below seems correct, press ENTER: \n")
        t = StoppableThread(env, "intensicy")
        t.start()
        input()
        t.stop()
        self.clear()

        self.print_module_page(env, i, nb_modules)
        print("If the temperature shown below seems correct, press ENTER: \n")
        t = StoppableThread(env, "temperature")
        t.start()
        input()
        t.stop()
        self.clear()

        self.print_module_page(env, i, nb_modules)
        print("If the humidity shown below seems correct, press ENTER: \n")
        t = StoppableThread(env, "humidity")
        t.start()
        input()
        t.stop()
        self.clear()

        self.print_module_page(env, i, nb_modules)
        print("If the volume shown below seems correct, press ENTER: \n")
        t = StoppableThread(env, "volume")
        t.start()
        input()
        t.stop()
        self.clear()

    def inspect_imu(self, imu, i, nb_moudles):
        self.print_wrap(
            """
            IMU module has angle, angular_velocity and acceleration as its property.
            """
        )
        input("\nIf you are ready to inspect this module, Press ENTER: ")
        self.clear()

        self.print_module_page(imu, i, nb_modules)
        print("If the angle shown below seems correct, press ENTER: \n")
        t = StoppableThread(imu, "angle")
        t.start()
        input()
        t.stop()
        self.clear()

        self.print_module_page(imu, i, nb_modules)
        print("If the angular_velocity shown below seems correct, press ENTER: \n")
        t = StoppableThread(imu, "angular_velocity")
        t.start()
        input()
        t.stop()
        self.clear()

        self.print_module_page(imu, i, nb_modules)
        print("If the acceleration shown below seems correct, press ENTER: \n")
        t = StoppableThread(env, "acceleration")
        t.start()
        input()
        t.stop()
        self.clear()

    def inspect_button(self, button, i, nb_modules):
        self.print_wrap(
            """
            Button module has cliked, double_clicked, pressed, toggled as its
            property.
            """
        )
        input("\nIf you are ready to inspect this module, Press ENTER: ")
        self.clear()

        self.print_module_page(button, i, nb_modules)
        print("If the click state shown below seems correct, press ENTER: \n")
        t = StoppableThread(button, "clicked")
        t.start()
        input()
        t.stop()
        self.clear()

        self.print_module_page(button, i, nb_modules)
        print("If the double click state shown below seems correct, "
              "press ENTER: \n")
        t = StoppableThread(button, "double_clicked")
        t.start()
        input()
        t.stop()
        self.clear()

        self.print_module_page(button, i, nb_modules)
        print("If the press state shown below seems correct, press ENTER: \n")
        t = StoppableThread(button, "pressed")
        t.start()
        input()
        t.stop()
        self.clear()

        self.print_module_page(button, i, nb_modules)
        print("If the toggle state shown below seems correct, press ENTER: \n")
        t = StoppableThread(button, "toggled")
        t.start()
        input()
        t.stop()
        self.clear()

    def inspect_dial(self, dial, i, nb_modules):
        self.print_wrap(
            """
            Dial module has turn and speed as its property.
            """
        )
        input("\nIf you are ready to inspect this module, Press ENTER: ")
        self.clear()

        self.print_module_page(dial, i, nb_modules)
        print("If the turn shown below seems correct, press ENTER: \n")
        t = StoppableThread(dial, "turn")
        t.start()
        input()
        t.stop()

        self.print_module_page(dial, i, nb_modules)
        print("If the speed shown below seems correct, press ENTER: \n")
        t = StoppableThread(dial, "speed")
        t.start()
        input()
        t.stop()

    def inspect_joystick(self, joystick, i, nb_modules):
        self.print_wrap(
            """
            Joystick module has x, y and direction as its property.
            """
        )
        input("\nIf you are ready to inspect this module, Press ENTER: ")
        self.clear()

        self.print_module_page(joystick, i, nb_modules)
        print("If the x shown below seems correct, press ENTER: \n")
        t = StoppableThread(joystick, "x")
        t.start()
        input()
        t.stop()

        self.print_module_page(joystick, i, nb_modules)
        print("If the y shown below seems correct, press ENTER: \n")
        t = StoppableThread(joystick, "y")
        t.start()
        input()
        t.stop()

        self.print_module_page(joystick, i, nb_modules)
        print("If the direction shown below seems correct, press ENTER: \n")
        t = StoppableThread(joystick, "direction")
        t.start()
        input()
        t.stop()

    def inspect_tof(self, tof, i, nb_modules):
        self.print_wrap(
            """
            ToF module has distance as its property.
            """
        )
        input("\nIf you are ready to inspect this module, Press ENTER: ")
        self.clear()

        self.print_module_page(tof, i, nb_modules)
        print("If the distance shown below seems correct, press ENTER: \n")
        t = StoppableThread(tof, "distance")
        t.start()
        input()
        t.stop()

    def inspect_display(self, display, i, nb_modules):
        self.print_wrap(
            """
            Display module has a text field as its property. We wil inspect
            this property for the module.
            """
        )
        input("\nIf you are ready to inspect this module, Press ENTER: ")
        self.clear()

        self.print_module_page(display, i, nb_modules)
        display.text = "Hello MODI!"
        input(dedent(
            """
            We have set "Hello MODI!" as its text, if you see this press ENTER:
            """.lstrip().rstrip() + " "
        ))
        display.text = ""

    def inspect_led(self, led, i, nb_modules):
        self.print_wrap(
            """
            LED module has red, green and blue as its property. We will inspect
            these properties each.
            """
        )
        input("\nPress ENTER to continue: ")
        self.clear()

        self.print_module_page(led, i, nb_modules)
        self.print_wrap(
            """
            To inspect RED, We have set LED's RED to its maximum intensity.
            """
        )
        led.rgb = 255, 0, 0
        input("\nIf you see strong red from the led module, Press ENTER: ")
        self.clear()

        self.print_module_page(led, i, nb_modules)
        self.print_wrap(
            """
            To inspect GREEN, We have set LED's GREEN to its maximum intensity.
            """
        )
        led.rgb = 0, 255, 0
        input("\nIf you see strong green from the led module, Press ENTER: ")
        self.clear()

        self.print_module_page(led, i, nb_modules)
        self.print_wrap(
            """
            To inspect BLUE, We have set LED's BLUE to its maximum intensity.
            """
        )
        led.rgb = 0, 0, 255
        input("\nIf you see strong blue from the led module, Press ENTER: ")
        self.clear()

        self.print_module_page(led, i, nb_modules)
        input(dedent(
            f"""
            It looks like the LED module ({led.id}) is properly functioning!
            To inspect next module, press ENTER to continue:
            """
        ))

    def inspect_motor_a(self, motor, i, nb_modules):
        self.print_wrap(
            """
            Motor module has degree (i.e. position), speed and torque as its
            property. We will inspect position property of the module.
            """
        )
        print()
        self.print_wrap(
            """
            Before continuing, we have set motors' initial position to zero
            (your motor module may have moved a bit), so be clam :)
            """
        )
        input("\nPress ENTER to continue: ")
        self.clear()
        motor.degree = 0, 70

        self.print_module_page(motor, i, nb_modules)
        self.print_wrap(
            """
            To inspect position property, we have rotated 360
            degree of the motor.
            """
        )
        motor.degree = 360, 70
        time.sleep(1.5)
        input("\nIf the first motor has rotated 360 degrees, press ENTER: ")
        print()

        self.print_module_page(motor, i, nb_modules)
        self.print_wrap(
            f"""
            It looks like the motor module ({motor.id}) is properly
            functioning!
            """
        )
        input("\nTo inspect next module, press ENTER to continue: ")

    def inspect_motor_b(self, motor, i, nb_modules):
        self.print_wrap(
            """
            Motor module has degree (i.e. position), speed and torque as its
            property. We will inspect position property of the module.
            """
        )
        print()
        self.print_wrap(
            """
            Before continuing, we have set motors' initial position to zero
            (your motor module may have moved a bit), so be clam :)
            """
        )
        input("\nPress ENTER to continue: ")
        self.clear()
        motor.degree = 0, 70

        self.print_module_page(motor, i, nb_modules)
        self.print_wrap(
            """
            To inspect position property, we have rotated 360
            degree of the motor.
            """
        )
        motor.degree = 360, 70
        time.sleep(1.5)
        input("\nIf the first motor has rotated 360 degrees, press ENTER: ")
        print()

        self.print_module_page(motor, i, nb_modules)
        self.print_wrap(
            f"""
            It looks like the motor module ({motor.id}) is properly
            functioning!
            """
        )
        input("\nTo inspect next module, press ENTER to continue: ")

    def inspect_speaker(self, speaker, i, nb_modules):
        self.print_wrap(
            """
            Speaker module has tune as its property, tune is composed of
            frequency and volume. Thus inspecting the tune property consists of
            inspecting frequency and volume properties.
            """
        )
        self.clear()

        self.print_module_page(speaker, i, nb_modules)
        self.print_wrap(
            """
            To inspect tune property, we have set frequency of 880 and volume
            of 50.
            """
        )
        speaker.tune = 1046, 50
        input(dedent(
            "\nPress ENTER if you hear a gentle sound from the speaker module!"
        ))
        speaker.tune = 1046, 0
        self.clear()

    #
    # Main methods are defined below
    #
    def run_inspection(self):
        self.clear()
        print("=" * self.row_len)
        print(f"= {'This is PyMODI Module Inspector':^{self.row_len - 4}} =")
        print("=" * self.row_len)

        self.print_wrap(
            """
            PyMODI provides a number of tools that can be utilized in different
            purpose. One of them is the STM32 module (all modules but network)
            inspector which diagnoses any malfunctioning MODI module.
            """
        )

        nb_modules = int(input(dedent(
            """
            Connect network module to your local machine, attach other modi
            modules to the network module. When attaching modi modules, make
            sure that you provide sufficient power to the modules. Using modi
            battery module is a good way of supplying the power to the modules.

            Type the number of modi modules (integer value) that are connected
            to the network module (note that the maximum number of modules is
            20) and press ENTER:
            """.rstrip() + " "
        )))
        self.clear()

        if not (1 <= nb_modules <= 20):
            print(f"ERROR: {nb_modules} is invalid for the number of modules")
            os._exit(0)

        print("Importing modi package and creating a modi bundle object...\n")
        import modi
        self.bundle = modi.MODI()

        stm32_modules = \
            [m for m in self.bundle.modules if m.module_type != "network"]
        nb_modules_detected = len(stm32_modules)
        if nb_modules != nb_modules_detected:
            self.print_wrap(
                f"""
                You said that you have attached {nb_modules} modules but PyMODI
                detects only {nb_modules_detected} number of modules! Look at
                the printed log above regarding module connection and check
                which modules have not been printed above.
                """
            )
            os._exit(0)

        input(dedent(
            """
            It looks like all stm modules have been initialized properly! Let's
            diagnose each module, one by one!

            Press ENTER to continue:
            """.rstrip() + " "
        ))
        self.clear()

        # Let's inspect each stm module!
        for i, module in enumerate(stm32_modules):
            self.inspect(module, i, nb_modules)
