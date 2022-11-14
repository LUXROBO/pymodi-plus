"""Main MODI+ module."""

import sys
import platform
import atexit
from typing import Optional

from importlib import import_module as im

from modi_plus.module.setup_module.network import Network
from modi_plus.module.setup_module.battery import Battery
from modi_plus.module.input_module.env import Env
from modi_plus.module.input_module.imu import Imu
from modi_plus.module.input_module.button import Button
from modi_plus.module.input_module.dial import Dial
from modi_plus.module.input_module.joystick import Joystick
from modi_plus.module.input_module.tof import Tof
from modi_plus.module.output_module.display import Display
from modi_plus.module.output_module.motor import Motor
from modi_plus.module.output_module.led import Led
from modi_plus.module.output_module.speaker import Speaker

from modi_plus.module.module import get_module_type_from_uuid
from modi_plus._exe_thread import ExeThread

from modi_plus.about import __version__


class ModuleList(list):

    def __init__(self, src, module_type=None):
        self.__src = src
        self.__module_type = module_type
        super().__init__(self.sublist())

    def __len__(self):
        return len(self.sublist())

    def __eq__(self, other):
        return super().__eq__(other)

    def get(self, module_id):
        for module in self.sublist():
            if module.id == module_id:
                return module
        raise Exception("Module with given id does not exits!!")

    def sublist(self):
        """ When accessing the module, the modules are sorted in an ascending order of
        1. the connected time from network module

        :return: Module
        """
        if self.__module_type:
            modules = list(filter(lambda module: module.module_type == self.__module_type, self.__src))
        else:
            modules = self.__src
        modules.sort()
        return modules

    def find(self, module_id):
        for idx, module in enumerate(self.sublist()):
            if module_id == module.id:
                return idx
        return -1

class MODIPlus:
    network_uuids = {}

    def __call__(cls, *args, **kwargs):
        network_uuid = kwargs.get("network_uuid")
        connection_type = kwargs.get("connection_type")
        if connection_type != "ble":
            return super(MODIPlus, cls).__call__(*args, **kwargs)
        if not network_uuid:
            raise ValueError("Should input a valid network uuid!")
        if network_uuid not in cls.network_uuids:
            cls.network_uuids[network_uuid] = super(MODIPlus, cls).__call__(*args, **kwargs)
        return cls.network_uuids[network_uuid]

    def __init__(self, connection_type="serialport", verbose=False, port=None, network_uuid=""):
        self._modules = list()
        self._connection = self.__init_task(connection_type, verbose, port, network_uuid)
        self._exe_thread = ExeThread(self._modules, self._connection)

        print("Start initializing connected MODI+ modules")
        self._exe_thread.start()
        print("MODI+ modules are initialized!")

        atexit.register(self.close)

    def __init_task(self, connection_type, verbose, port, network_uuid):
        if connection_type == "serialport":
            return im("modi_plus.task.serialport_task").SerialportTask(verbose, port)
        elif connection_type == "ble":
            if not network_uuid:
                raise ValueError("Network UUID not specified!")
            self.network_uuids[network_uuid] = self
            mod_path = {
                "win32": "modi_plus.task.ble_task.ble_task_win",
                "darwin": "modi_plus.task.ble_task.ble_task_mac",
                "rpi": "modi_plus.task.ble_task.ble_task_rpi",
            }.get(self.__get_platform())
            return im(mod_path).BleTask(verbose, network_uuid)
        else:
            raise ValueError(f"Invalid conn mode: {connection_type}")

    def open(self):
        atexit.register(self.close)
        self._exe_thread = ExeThread(self._modules, self._connection)
        self._connection.open_connection()
        self._exe_thread.start()

    def close(self):
        atexit.unregister(self.close)
        print("Closing MODI+ connection...")
        self._exe_thread.close()
        self._connection.close_connection()

    def send(self, message):
        """Low level method to send json pkt directly to modules

        :param message: Json packet to send
        :return: None
        """
        self._connection.send_nowait(message)

    def recv(self):
        """Low level method to receive json pkt directly from modules

        :return: Json msg received
        :rtype: str if msg exists, else None
        """
        return self._connection.recv()

    def __get_platform(self):
        if platform.uname().node == "raspberrypi":
            return "rpi"
        return sys.platform

    def __get_module_by_uuid(self, module_uuid):
        for module in self._modules:
            if module.uuid == module_uuid:
                return module
        return None

    def network(self, uuid: int) -> Optional[Network]:
        """Module Class of connected Network module.
        """
        if get_module_type_from_uuid(uuid) != "network":
            return None
        return self.__get_module_by_uuid(uuid)

    def battery(self, uuid: int) -> Optional[Battery]:
        """Module Class of connected Battery module.
        """
        if get_module_type_from_uuid(uuid) != "battery":
            return None
        return self.__get_module_by_uuid(uuid)

    def env(self, uuid: int) -> Optional[Env]:
        """Module Class of connected Environment modules.
        """
        if get_module_type_from_uuid(uuid) != "env":
            return None
        return self.__get_module_by_uuid(uuid)

    def imu(self, uuid: int) -> Optional[Imu]:
        """Module Class of connected IMU modules.
        """
        if get_module_type_from_uuid(uuid) != "imu":
            return None
        return self.__get_module_by_uuid(uuid)

    def button(self, uuid: int) -> Optional[Button]:
        """Module Class of connected Button modules.
        """
        if get_module_type_from_uuid(uuid) != "button":
            return None
        return self.__get_module_by_uuid(uuid)

    def dial(self, uuid: int) -> Optional[Dial]:
        """Module Class of connected Dial modules.
        """
        if get_module_type_from_uuid(uuid) != "dial":
            return None
        return self.__get_module_by_uuid(uuid)

    def joystick(self, uuid: int) -> Optional[Joystick]:
        """Module Class of connected Joystick modules.
        """
        if get_module_type_from_uuid(uuid) != "joystick":
            return None
        return self.__get_module_by_uuid(uuid)

    def tof(self, uuid: int) -> Optional[Tof]:
        """Module Class of connected ToF modules.
        """
        if get_module_type_from_uuid(uuid) != "tof":
            return None
        return self.__get_module_by_uuid(uuid)

    def display(self, uuid: int) -> Optional[Display]:
        """Module Class of connected Display modules.
        """
        if get_module_type_from_uuid(uuid) != "display":
            return None
        return self.__get_module_by_uuid(uuid)

    def motor(self, uuid: int) -> Optional[Motor]:
        """Module Class of connected Motor modules.
        """
        if get_module_type_from_uuid(uuid) != "motor":
            return None
        return self.__get_module_by_uuid(uuid)

    def led(self, uuid: int) -> Optional[Led]:
        """Module Class of connected Led modules.
        """
        if get_module_type_from_uuid(uuid) != "led":
            return None
        return self.__get_module_by_uuid(uuid)

    def speaker(self, uuid: int) -> Optional[Speaker]:
        """Module Class of connected Speaker modules.
        """
        if get_module_type_from_uuid(uuid) != "speaker":
            return None
        return self.__get_module_by_uuid(uuid)

    @property
    def modules(self) -> ModuleList:
        """Module List of connected modules except network module.
        """
        return ModuleList(self._modules)

    @property
    def networks(self) -> ModuleList:
        """Module List of connected Network modules.
        """
        return ModuleList(self._modules, "network")

    @property
    def batterys(self) -> ModuleList:
        """Module List of connected Battery modules.
        """
        return ModuleList(self._modules, "battery")

    @property
    def envs(self) -> ModuleList:
        """Module List of connected Environment modules.
        """
        return ModuleList(self._modules, "env")

    @property
    def imus(self) -> ModuleList:
        """Module List of connected IMU modules.
        """
        return ModuleList(self._modules, "imu")

    @property
    def buttons(self) -> ModuleList:
        """Module List of connected Button modules.
        """
        return ModuleList(self._modules, "button")

    @property
    def dials(self) -> ModuleList:
        """Module List of connected Dial modules.
        """
        return ModuleList(self._modules, "dial")

    @property
    def joysticks(self) -> ModuleList:
        """Module List of connected Joystick modules.
        """
        return ModuleList(self._modules, "joystick")

    @property
    def tofs(self) -> ModuleList:
        """Module List of connected ToF modules.
        """
        return ModuleList(self._modules, "tof")

    @property
    def displays(self) -> ModuleList:
        """Module List of connected Display modules.
        """
        return ModuleList(self._modules, "display")

    @property
    def motors(self) -> ModuleList:
        """Module List of connected Motor modules.
        """
        return ModuleList(self._modules, "motor")

    @property
    def leds(self) -> ModuleList:
        """Module List of connected Led modules.
        """
        return ModuleList(self._modules, "led")

    @property
    def speakers(self) -> ModuleList:
        """Module List of connected Speaker modules.
        """
        return ModuleList(self._modules, "speaker")
