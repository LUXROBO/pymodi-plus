"""Led module."""

from typing import Tuple
from modi_plus.module.output_module.output_module import OutputModule


class Led(OutputModule):

    RED = 2
    GREEN = 3
    BLUE = 4

    SET_RGB = 16

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
        if (red, green, blue) == self.rgb:
            return
        self._set_property(
            destination_id=self._id,
            property_num=Led.SET_RGB,
            property_values=(('u16', red),
                             ('u16', green),
                             ('u16', blue))
        )
        self.update_property(Led.RED, red)
        self.update_property(Led.GREEN, green)
        self.update_property(Led.BLUE, blue)

    @property
    def red(self) -> float:
        """Returns the current value of the red component of the LED

        :return: Red component
        :rtype: float
        """
        return self._get_property(Led.RED)

    @property
    def green(self) -> float:
        """Returns the current value of the green component of the LED

        :return: Green component
        :rtype: float
        """
        return self._get_property(Led.GREEN)

    @property
    def blue(self) -> float:
        """Returns the current value of the blue component of the LED

        :return: Blue component
        :rtype: float
        """
        return self._get_property(Led.BLUE)

    #
    # Legacy Support
    #
    def turn_on(self) -> None:
        """Turn on led at maximum brightness.

        :return: RGB value of the LED set to maximum brightness
        :rtype: None
        """
        self.rgb = 100, 100, 100

    def turn_off(self) -> None:
        """Turn off led.

        :return: None
        """
        self.rgb = 0, 0, 0
