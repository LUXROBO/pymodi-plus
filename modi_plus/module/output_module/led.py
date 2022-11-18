"""Led module."""

import struct

from typing import Tuple
from modi_plus.module.output_module.output_module import OutputModule


class Led(OutputModule):

    PROPERTY_LED_STATE = 2

    PROPERTY_LED_SET_RGB = 16

    PROPERTY_OFFSET_RED = 0
    PROPERTY_OFFSET_GREEN = 2
    PROPERTY_OFFSET_BLUE = 4

    @property
    def rgb(self) -> Tuple[float, float, float]:
        return self.red, self.green, self.blue

    def set_rgb(self, red, green, blue) -> None:
        """Sets the color of the LED light with given RGB values, and returns
        the current RGB values.

        :param color: RGB value to set
        :type color: Tuple[int, int, int]
        :return: None
        """
        self._set_property(
            destination_id=self._id,
            property_num=Led.PROPERTY_LED_SET_RGB,
            property_values=(("u16", red),
                             ("u16", green),
                             ("u16", blue))
        )

    @property
    def red(self) -> int:
        """Returns the current value of the red component of the LED

        :return: Red component
        :rtype: int
        """
        offset = Led.PROPERTY_OFFSET_RED
        raw = self._get_property(Led.PROPERTY_LED_STATE)
        data = struct.unpack("H", raw[offset:offset + 2])[0]
        return data

    @property
    def green(self) -> int:
        """Returns the current value of the green component of the LED

        :return: Green component
        :rtype: int
        """
        offset = Led.PROPERTY_OFFSET_GREEN
        raw = self._get_property(Led.PROPERTY_LED_STATE)
        data = struct.unpack("H", raw[offset:offset + 2])[0]
        return data

    @property
    def blue(self) -> int:
        """Returns the current value of the blue component of the LED

        :return: Blue component
        :rtype: int
        """
        offset = Led.PROPERTY_OFFSET_BLUE
        raw = self._get_property(Led.PROPERTY_LED_STATE)
        data = struct.unpack("H", raw[offset:offset + 2])[0]
        return data

    #
    # Legacy Support
    #
    def turn_on(self) -> None:
        """Turn on led at maximum brightness.

        :return: RGB value of the LED set to maximum brightness
        :rtype: None
        """
        self.set_rgb(100, 100, 100)

    def turn_off(self) -> None:
        """Turn off led.

        :return: None
        """
        self.set_rgb(0, 0, 0)
