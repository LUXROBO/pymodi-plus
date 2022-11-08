import json
import time
from base64 import b64decode

from modi.module.module import Module, BROADCAST_ID
from modi.module.setup_module.battery import Battery
from modi.util.miscellaneous_util import get_module_from_name
from modi.util.miscellaneous_util import get_module_type_from_uuid
from modi.util.message_util import unpack_data, parse_message


class ExeTask:

    def __init__(self, modules, conn_task):
        self._modules = modules
        self._conn = conn_task

        # Reboot all modules
        self.__set_module_state(BROADCAST_ID, Module.REBOOT, Module.PNP_OFF)

        # Request data required to initialize MODI
        self.__request_module_uuid()
        self.__request_network_uuid()

    def run(self, delay):
        """ Run in ExecutorThread

        :param delay: time value to wait in seconds
        :type delay: float
        """
        json_pkt = self._conn.recv()
        if not json_pkt:
            time.sleep(delay)
        else:
            try:
                json_msg = json.loads(json_pkt)
                self.__command_handler(json_msg['c'])(json_msg)
            except json.decoder.JSONDecodeError:
                print('current json message:', json_pkt)

    def __command_handler(self, command):
        """ Execute task based on command message

        :param command: command code
        :type command: int
        :return: a function the corresponds to the command code
        :rtype: Callable[[Dict[str, int]], None]
        """
        return {
            0x00: self.__update_health,
            0x05: self.__update_modules,
            0x1F: self.__update_property,
            0xA1: self.__update_esp_version,
        }.get(command, lambda _: None)

    def __update_esp_version(self, message):
        network_module = None
        for module in self._modules:
            if module.module_type == 'network':
                network_module = module
                break
        if not network_module:
            return
        network_module.esp_version = b64decode(message['b'])[3:].decode()

    def __get_module_by_id(self, module_id):
        for module in self._modules:
            if module.id == module_id:
                return module

    def __update_health(self, message):
        """ Update information by health message

        :param message: Dictionary format message of the module
        :type message: Dictionary
        :return: None
        """
        # Record battery information and user code state
        module_id = message["s"]
        _, _, _, battery_state, user_code_state = unpack_data(message['b'], (1, 1, 1, 1, 1))
        curr_time = time.time()

        # Checking starts only when module is registered
        if module_id in (module.id for module in self._modules):
            module = self.__get_module_by_id(module_id)
            module.last_updated = curr_time
            module.is_connected = True
            # Update user code status
            if module.user_code_status < 0:
                module.user_code_status = user_code_state % 2
            # Turn off pnp if pnp flag is on
            if module.module_type != 'network' and user_code_state < 2:
                self.__set_module_state(module_id, Module.RUN, Module.PNP_OFF)
            # Reset disconnection alert status
            if module.has_printed:
                module.has_printed = False

        # Disconnect module with no health message for more than 2 second
        for module in self._modules:
            if module.module_type != 'network' and curr_time - module.last_updated > 2:
                module.is_connected = False
                module._last_set_message = None

    def __update_modules(self, message):
        """ Update module information
        :param message: Dictionary format module info
        :type message: Dictionary
        :return: None
        """
        module_id = message['s']
        module_uuid, module_os_version_info, module_app_version_info = unpack_data(message['b'], (6, 2, 2))

        # Handle new modules
        if module_id not in (module.id for module in self._modules):
            module_type = get_module_type_from_uuid(module_uuid)
            new_module = self.__add_new_module(module_type, module_id, module_uuid, module_app_version_info, module_os_version_info)
            new_module.module_type = module_type
            if module_type != 'network' and not new_module.is_up_to_date:
                print(f"{str(new_module)} is not up to date. Please update the module by calling modi.update_module_firmware")

        elif not self.__get_module_by_id(module_id).is_connected:
            # Handle Reconnected modules
            self.__get_module_by_id(module_id).is_connected = True
            module_type = get_module_type_from_uuid(module_uuid)
            print(f"{module_type} ({module_id}) has been reconnected!!")

    def __add_new_module(self, module_type, module_id, module_uuid, module_app_version_info, module_os_version_info):
        module_template = get_module_from_name(module_type)
        module_instance = module_template(module_id, module_uuid, self._conn)
        self.__set_module_state(module_instance.id, Module.RUN, Module.PNP_OFF)
        module_instance.app_version = module_app_version_info
        module_instance.os_version = module_os_version_info
        self._modules.append(module_instance)
        print(f"{str(module_instance)} has been connected!")
        return module_instance

    def __update_property(self, message):
        """ Update module property

        :param message: Dictionary format message
        :type message: Dictionary
        :return: None
        """

        # Do not update reserved property
        property_number = message["d"]
        if property_number == 0 or property_number == 1:
            return
        module = self.__get_module_by_id(message['s'])
        if not module:
            return
        data = bytearray(b64decode(message['b']))
        if module.module_type == 'network':
            module.update_property(property_number, data)
        else:
            module.update_property(property_number, data)

    def __set_module_state(self, destination_id, module_state, pnp_state):
        """ Generate message for set module state and pnp state

        :param destination_id: Id to target destination
        :type destination_id: int
        :param module_state: State value of the module
        :type module_state: int
        :param pnp_state: Pnp state value
        :type pnp_state: int
        :return: None
        """
        self._conn.send_nowait(parse_message(0x09, 0, destination_id, (module_state, pnp_state)))

    def __request_module_uuid(self):
        self._conn.send_nowait(parse_message(0x8, BROADCAST_ID, BROADCAST_ID, (0xFF, 0x0F)))

    def __request_network_uuid(self):
        self._conn.send_nowait(
            parse_message(0x28, BROADCAST_ID, BROADCAST_ID, (0xFF, 0x0F))
        )