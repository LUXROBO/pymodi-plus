"""Module module."""

import time
import json
from typing import Union
from os import path

from modi.util.message_util import parse_message
from modi.util.miscellaneous_util import get_module_type_from_uuid

BROADCAST_ID = 0xFFF


class Module:
    """
    :param int id_: The id of the module.
    :param int uuid: The uuid of the module.
    """

    class Property:
        def __init__(self):
            self.value = bytearray(12)
            self.last_update_time = time.time()

    RUN = 0
    WARNING = 1
    FORCED_PAUSE = 2
    ERROR_STOP = 3
    UPDATE_FIRMWARE = 4
    UPDATE_FIRMWARE_READY = 5
    REBOOT = 6
    PNP_ON = 1
    PNP_OFF = 2

    def __init__(self, id_, uuid, conn_task):
        self._id = id_
        self._uuid = uuid
        self._conn = conn_task

        self.module_type = str()
        self._properties = dict()

        # sampling_rate = (100 - property_sampling_frequency) * 11, in ms
        self.prop_samp_freq = 91

        self.is_connected = True
        self.has_printed = False
        self.last_updated = time.time()
        self.battery = 100
        self.position = (0, 0)
        self.__app_version = None
        self.__os_version = None
        self.user_code_status = -1  # 1 if user code and 0 if not

    def __gt__(self, other):
        if self.order == other.order:
            if self.position[0] == other.position[0]:
                return self.position[1] < other.position[1]
            else:
                return self.position[0] > other.position[0]
        else:
            return self.order > other.order

    def __lt__(self, other):
        if self.order == other.order:
            if self.position[0] == other.position[0]:
                return self.position[1] > other.position[1]
            else:
                return self.position[0] < other.position[0]
        else:
            return self.order < other.order

    def __str__(self):
        return f"{self.__class__.__name__} ({self._id})"

    @property
    def has_user_code(self):
        return self.user_code_status == 1

    @property
    def app_version(self):
        version_string = ""
        version_string += str(self.__app_version >> 13) + '.'
        version_string += str(self.__app_version % (2 ** 13) >> 8) + '.'
        version_string += str(self.__app_version % (2 ** 8))
        return version_string

    @app_version.setter
    def app_version(self, version_info):
        self.__app_version = version_info

    @property
    def os_version(self):
        version_string = ""
        version_string += str(self.__os_version >> 13) + '.'
        version_string += str(self.__os_version % (2 ** 13) >> 8) + '.'
        version_string += str(self.__os_version % (2 ** 8))
        return version_string

    @os_version.setter
    def os_version(self, version_info):
        self.__os_version = version_info

    @property
    def order(self):
        return self.position[0] ** 2 + self.position[1] ** 2

    @property
    def id(self) -> int:
        return self._id

    @property
    def uuid(self) -> int:
        return self._uuid

    @property
    def is_up_to_date(self):
        root_path = (
            path.join(
                path.dirname(__file__),
                '..', 'assets'
            )
        )
        version_path = path.join(root_path, 'version.txt')
        with open(version_path, "r") as version_file:
            try:
                version_info = json.loads(version_file.read())
            except Exception as e:
                pass

        app_version_info = version_info[self.module_type].lstrip('v').rstrip('\n')
        if self.module_type in ['env', 'display', 'speaker']:
            os_version_info = version_info['os_e103'].lstrip('v').rstrip('\n')
        else:
            os_version_info = version_info['os_e230'].lstrip('v').rstrip('\n')

        app_version_digits = [int(digit) for digit in app_version_info.split('.')]
        os_version_digits = [int(digit) for digit in os_version_info.split('.')]

        latest_app_version = (
            app_version_digits[0] << 13
            | app_version_digits[1] << 8
            | app_version_digits[2]
        )
        latest_os_version = (
            os_version_digits[0] << 13
            | os_version_digits[1] << 8
            | os_version_digits[2]
        )

        return latest_app_version <= self.__app_version or latest_os_version <= self.__os_version

    def _get_property(self, property_type: int) -> bytearray:
        """ Get module property value and request

        :param property_type: Type of the requested property
        :type property_type: int
        """

        # Register property if not exists
        if property_type not in self._properties:
            self._properties[property_type] = self.Property()
            self.__request_property(self._id, property_type)

        # Request property value if not updated for 1.5 sec
        last_update = self._properties[property_type].last_update_time
        if time.time() - last_update > 1.5:
            self.__request_property(self._id, property_type)

        return self._properties[property_type].value

    def update_property(self, property_type: int, property_value: bytearray) -> None:
        """ Update property value and time

        :param property_type: Type of the updated property
        :type property_type: int
        :param property_value: Value to update the property
        :type property_value: bytearray
        """
        if property_type not in self._properties:
            self._properties[property_type] = self.Property()
        self._properties[property_type].value = property_value
        self._properties[property_type].last_update_time = time.time()

    def __request_property(self, destination_id: int, property_type: int) -> None:
        """ Generate message for request property

        :param destination_id: Id of the destination module
        :type destination_id: int
        :param property_type: Type of the requested property
        :type property_type: int
        :return: None
        """
        self._properties[property_type].last_update_time = time.time()
        req_prop_msg = parse_message(0x03, 0, destination_id, (property_type, 0x00, self.prop_samp_freq, 0x00))
        self._conn.send(req_prop_msg)
