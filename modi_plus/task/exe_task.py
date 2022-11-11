import json
import time
from base64 import b64decode

from modi_plus.module.module import Module, BROADCAST_ID, get_module_from_name, get_module_type_from_uuid
from modi_plus.util.message_util import unpack_data, parse_message


class ExeTask:

    def __init__(self, modules, connection_task):
        self._modules = modules
        self._conn = connection_task

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
                self.__command_handler(json_msg["c"])(json_msg)
            except json.decoder.JSONDecodeError:
                print("current json message:", json_pkt)

    def __command_handler(self, command):
        """ Execute task based on command message

        :param command: command code
        :type command: int
        :return: a function the corresponds to the command code
        :rtype: Callable[[Dict[str, int]], None]
        """
        return {
            0x00: self.__update_health,
            0x05: self.__update_assign_id,
            0x1F: self.__update_channel,
            0xA1: self.__update_esp_version,
        }.get(command, lambda _: None)

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
        curr_time = time.time()

        # Checking starts only when module is registered
        if module_id in (module.id for module in self._modules):
            module = self.__get_module_by_id(module_id)
            module.last_updated = curr_time
            module.is_connected = True

            # Reset disconnection alert status
            if module.has_printed:
                module.has_printed = False
        else:
            self.__request_find_id(module_id)
            self.__request_find_network_id(module_id)

        # Disconnect module with no health message for more than 2 second
        for module in self._modules:
            if curr_time - module.last_updated > 2:
                module.is_connected = False
                module._last_set_message = None

    def __update_assign_id(self, message):
        """ Update module information
        :param message: Dictionary format module info
        :type message: Dictionary
        :return: None
        """
        module_id = message["s"]
        module_uuid, module_os_version_info, module_app_version_info = unpack_data(message["b"], (6, 2, 2))
        module_type = get_module_type_from_uuid(module_uuid)

        # Handle new modules
        if module_id not in (module.id for module in self._modules):
            new_module = self.__add_new_module(module_type, module_id, module_uuid, module_app_version_info, module_os_version_info)
            new_module.module_type = module_type
            if module_type == "network":
                self.__request_esp_version(module_id)
        else:
            module = self.__get_module_by_id(module_id)
            if not module.is_connected:
                # Handle Reconnected modules
                module.is_connected = True
                self.__request_pnp_off(module.id)
                print(f"{str(module)} has been reconnected!")

    def __add_new_module(self, module_type, module_id, module_uuid, module_app_version_info, module_os_version_info):
        module_template = get_module_from_name(module_type)
        module_instance = module_template(module_id, module_uuid, self._conn)
        self.__request_pnp_off(module_instance.id)
        module_instance.app_version = module_app_version_info
        module_instance.os_version = module_os_version_info
        self._modules.append(module_instance)
        print(f"{str(module_instance)} has been connected!")
        return module_instance

    def __update_channel(self, message):
        """ Update module property

        :param message: Dictionary format message
        :type message: Dictionary
        :return: None
        """

        module_id = message["s"]
        property_number = message["d"]
        property_data = bytearray(b64decode(message["b"]))

        # Do not update reserved property
        if property_number == 0 or property_number == 1:
            return

        module = self.__get_module_by_id(module_id)
        if not module:
            return

        module.update_property(property_number, property_data)

    def __update_esp_version(self, message):
        network_module = None
        for module in self._modules:
            if module.module_type == "network":
                network_module = module
                break
        if not network_module:
            return

        raw_data = b64decode(message["b"])
        network_module.esp_version = raw_data.lstrip(b"\x00").decode()

    def __request_pnp_on(self, id):
        self._conn.send_nowait(parse_message(0x09, 0, id, (Module.RUN, Module.PNP_ON)))

    def __request_pnp_off(self, id):
        self._conn.send_nowait(parse_message(0x09, 0, id, (Module.RUN, Module.PNP_OFF)))

    def __request_find_id(self, id):
        self._conn.send_nowait(parse_message(0x08, 0x00, id, (0xFF, 0x0F)))

    def __request_find_network_id(self, id):
        self._conn.send_nowait(parse_message(0x28, 0x00, id, (0xFF, 0x0F)))

    def __request_esp_version(self, id):
        self._conn.send_nowait(parse_message(0xA0, 25, id, (0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF)))
