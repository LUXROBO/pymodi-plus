"""Joystick module."""

import struct

from modi.module.input_module.input_module import InputModule

class Joystick(InputModule):

    PROP_POSITION_STATE = 2
    PROP_OFFSET_X = 0
    PROP_OFFSET_Y = 2

    PROP_DIRECTION_STATE = 3
    PROP_OFFSET_DIRECTION = 0

    @property
    def x(self) -> int:
        """Returns the x position of the joystick between -100 and 100

        :return: The joystick's x position.
        :rtype: int
        """

        offset = Joystick.PROP_OFFSET_X
        raw = self._get_property(Joystick.PROP_POSITION_STATE)
        data = struct.unpack('h', raw[offset:offset+2])[0]
        return data

    @property
    def y(self) -> int:
        """Returns the y position of the joystick between -100 and 100

        :return: The joystick's y position.
        :rtype: int
        """

        offset = Joystick.PROP_OFFSET_Y
        raw = self._get_property(Joystick.PROP_POSITION_STATE)
        data = struct.unpack('h', raw[offset:offset+2])[0]
        return data

    @property
    def direction(self) -> int:
        """Returns the direction of the joystick between -100 and 100

        :return: The joystick's direction.
        :rtype: int
        """

        offset = Joystick.PROP_OFFSET_DIRECTION
        raw = self._get_property(Joystick.PROP_DIRECTION_STATE)
        data = struct.unpack('h', raw[offset:offset+2])[0]
        return data
