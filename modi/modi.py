"""Main MODI module."""

import sys
import time
import atexit
import logging

from importlib import import_module as im

from modi._exe_thrd import ExeThrd
from modi.util.connection_util import is_network_module_connected, is_on_pi
from modi.util.miscellaneous_util import ModuleList
from modi.util.strange_util import check_complete
# from modi.util.firmware_updater import STM32FirmwareUpdater
# from modi.util.firmware_updater import ESP32FirmwareUpdater

from modi.about import __version__


class MODI:
    network_uuids = {}

    def __call__(cls, *args, **kwargs):
        network_uuid = kwargs.get('network_uuid')
        conn_type = kwargs.get('conn_type')
        if conn_type != 'ble':
            return super(MODI, cls).__call__(*args, **kwargs)
        if not network_uuid:
            raise ValueError('Should input a valid network uuid!')
        if network_uuid not in cls.network_uuids:
            cls.network_uuids[network_uuid] = super(MODI, cls).__call__(*args, **kwargs)
        return cls.network_uuids[network_uuid]

    def __init__(
        self, conn_type="", verbose=False, port=None,
        network_uuid="", virtual_modules=None,
    ):
        if virtual_modules and conn_type != "vir":
            raise ValueError("Virtual modules can only be defined in virtual connection")
        self._modules = list()

        self._conn = self.__init_task(conn_type, verbose, port, network_uuid)

        self._exe_thrd = ExeThrd(self._modules, self._conn)
        print('Start initializing connected MODI modules')
        self._exe_thrd.start()

        init_time = time.time()
        check_complete(self)
        print("MODI modules are initialized!")

        bad_modules = (self.__wait_user_code_check() if conn_type != 'ble' else [])
        if bad_modules:
            cmd = input(f"{[str(module) for module in bad_modules]} has user code in it.\nReset the user code? [y/n] ")
            if 'y' in cmd:
                self.close()
                modules_to_reset = filter(lambda m: m.is_up_to_date, bad_modules)
                modules_to_update = filter(lambda m: not m.is_up_to_date, bad_modules)
                reset_module_firmware(tuple(module.id for module in modules_to_reset))
                update_module_firmware(tuple(module.id for module in modules_to_update))
                self.open()
        atexit.register(self.close)

    @staticmethod
    def __init_logger():
        logger = logging.getLogger(f'PyMODI (v{__version__}) Logger')
        logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler = logging.FileHandler('pymodi.log')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        return logger

    def __wait_user_code_check(self):
        def is_not_checked(module):
            return module.user_code_status < 0

        while list(filter(is_not_checked, self._modules)):
            time.sleep(0.1)
        bad_modules = []
        for module in self._modules:
            if module.has_user_code:
                bad_modules.append(module)
        return bad_modules

    def __init_task(self, conn_type, verbose, port, network_uuid):
        if not conn_type:
            is_can = not is_network_module_connected() and is_on_pi()
            conn_type = 'can' if is_can else 'ser'

        if conn_type == 'ser':
            return im('modi.task.serialport_task').SerialportTask(verbose, port)
        elif conn_type == 'soc':
            return im('modi.task.soc_task').SocTask(verbose, port)
        elif conn_type == 'vir':
            return im('modi.task.vir_task').VirTask(verbose, port)
        elif conn_type == 'can':
            return im('modi.task.can_task').CanTask(verbose)
        elif conn_type == 'ble':
            if not network_uuid:
                raise ValueError('Network UUID not specified!')
            self.network_uuids[network_uuid] = self
            mod_path = {
                'win32': 'modi.task.ble_task.ble_task_mac',
                'linux': 'modi.task.ble_task.ble_task_rpi',
                'darwin': 'modi.task.ble_task.ble_task_mac',
            }.get(sys.platform)
            return im(mod_path).BleTask(verbose, network_uuid)
        else:
            raise ValueError(f'Invalid conn mode: {conn_type}')

    def open(self):
        atexit.register(self.close)
        self._exe_thrd = ExeThrd(self._modules, self._conn)
        self._conn.open_conn()
        self._exe_thrd.start()

    def close(self):
        atexit.unregister(self.close)
        print("Closing MODI connection...")
        self._exe_thrd.close()
        self._conn.close_conn()

    def send(self, message):
        """Low level method to send json pkt directly to modules

        :param message: Json packet to send
        :return: None
        """
        self._conn.send_nowait(message)

    def recv(self):
        """Low level method to receive json pkt directly from modules

        :return: Json msg received
        :rtype: str if msg exists, else None
        """
        return self._conn.recv()

    @property
    def modules(self) -> ModuleList:
        """Module List of connected modules except network module.
        """
        return ModuleList(self._modules)

    @property
    def networks(self) -> ModuleList:
        """Module List of connected Network modules.
        """
        return ModuleList(self._modules, 'network')

    @property
    def batterys(self) -> ModuleList:
        """Module List of connected Battery modules.
        """
        return ModuleList(self._modules, 'battery')

    @property
    def envs(self) -> ModuleList:
        """Module List of connected Env modules.
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
        return ModuleList(self._modules, 'button')

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

# def update_module_firmware(target_ids=(0xFFF, )):
#     updater = STM32FirmwareUpdater(target_ids=target_ids)
#     updater.update_module_firmware()
#     updater.close()


# def reset_module_firmware(target_ids=(0xFFF, )):
#     updater = STM32FirmwareUpdater(is_os_update=False, target_ids=target_ids)
#     updater.update_module_firmware()
#     updater.close()


# def update_network_firmware(force=False):
#     updater = ESP32FirmwareUpdater()
#     updater.update_firmware(force=force)
