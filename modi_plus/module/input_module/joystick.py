"""Joystick module."""

import struct
from modi_plus.module.input_module.input_module import InputModule


class Joystick(InputModule):

    PROPERTY_POSITION_STATE = 2
    PROPERTY_DIRECTION_STATE = 3

    PROPERTY_OFFSET_X = 0
    PROPERTY_OFFSET_Y = 2
    PROPERTY_OFFSET_DIRECTION = 0

    @property
    def x(self) -> int:
        """Returns the x position of the joystick between -100 and 100

        :return: The joystick's x position.
        :rtype: int
        """

        offset = Joystick.PROPERTY_OFFSET_X
        raw = self._get_property(Joystick.PROPERTY_POSITION_STATE)
        data = struct.unpack("h", raw[offset:offset + 2])[0]
        return data

    @property
    def y(self) -> int:
        """Returns the y position of the joystick between -100 and 100

        :return: The joystick's y position.
        :rtype: int
        """

        offset = Joystick.PROPERTY_OFFSET_Y
        raw = self._get_property(Joystick.PROPERTY_POSITION_STATE)
        data = struct.unpack("h", raw[offset:offset + 2])[0]
        return data

    @property
    def direction(self) -> int:
        """Returns the direction of the joystick
        Up : 100
        Down : -100
        Right : 50
        Left : -50
        None : 0

        :return: The joystick's direction.
        :rtype: int
        """

        offset = Joystick.PROPERTY_OFFSET_DIRECTION
        raw = self._get_property(Joystick.PROPERTY_DIRECTION_STATE)
        data = struct.unpack("h", raw[offset:offset + 2])[0]
        return data
