"""Env module."""

import struct
from modi_plus.module.module import InputModule


class Env(InputModule):

    PROPERTY_ENV_STATE = 2

    PROPERTY_OFFSET_ILLUMINANCE = 0
    PROPERTY_OFFSET_TEMPERATURE = 2
    PROPERTY_OFFSET_HUMIDITY = 4
    PROPERTY_OFFSET_VOLUME = 6
    PROPERTY_OFFSET_RED = 8
    PROPERTY_OFFSET_GREEN = 10
    PROPERTY_OFFSET_BLUE = 12

    @property
    def illuminance(self) -> int:
        """Returns the value of illuminance between 0 and 100

        :return: The environment's illuminance.
        :rtype: int
        """

        offset = Env.PROPERTY_OFFSET_ILLUMINANCE
        raw = self._get_property(Env.PROPERTY_ENV_STATE)
        data = struct.unpack("h", raw[offset:offset + 2])[0]
        return data

    @property
    def temperature(self) -> int:
        """Returns the value of temperature between -10 and 60

        :return: The environment's temperature.
        :rtype: int
        """

        offset = Env.PROPERTY_OFFSET_TEMPERATURE
        raw = self._get_property(Env.PROPERTY_ENV_STATE)
        data = struct.unpack("h", raw[offset:offset + 2])[0]
        return data

    @property
    def humidity(self) -> int:
        """Returns the value of humidity between 0 and 100

        :return: The environment's humidity.
        :rtype: int
        """

        offset = Env.PROPERTY_OFFSET_HUMIDITY
        raw = self._get_property(Env.PROPERTY_ENV_STATE)
        data = struct.unpack("h", raw[offset:offset + 2])[0]
        return data

    @property
    def volume(self) -> int:
        """Returns the value of volume between 0 and 100

        :return: The environment's volume.
        :rtype: int
        """

        offset = Env.PROPERTY_OFFSET_VOLUME
        raw = self._get_property(Env.PROPERTY_ENV_STATE)
        data = struct.unpack("h", raw[offset:offset + 2])[0]
        return data

    def _is_rgb_supported(self) -> bool:
        """Check if RGB properties are supported based on app version

        RGB is supported in app version 2.x and above.
        Version 1.x does not support RGB.

        :return: True if RGB is supported, False otherwise
        :rtype: bool
        """
        if not hasattr(self, '_Module__app_version') or self._Module__app_version is None:
            return False

        # Extract major version: version >> 13
        major_version = self._Module__app_version >> 13
        return major_version >= 2

    @property
    def red(self) -> int:
        """Returns the red color value between 0 and 255

        Note: This property is only available in Env module version 2.x and above.
        Version 1.x does not support RGB properties.

        :return: The environment's red color value.
        :rtype: int
        :raises AttributeError: If app version is 1.x (RGB not supported)
        """
        if not self._is_rgb_supported():
            raise AttributeError(
                "RGB properties are not supported in Env module version 1.x. "
                "Please upgrade to version 2.x or above."
            )

        offset = Env.PROPERTY_OFFSET_RED
        raw = self._get_property(Env.PROPERTY_ENV_STATE)
        data = struct.unpack("h", raw[offset:offset + 2])[0]
        return data

    @property
    def green(self) -> int:
        """Returns the green color value between 0 and 255

        Note: This property is only available in Env module version 2.x and above.
        Version 1.x does not support RGB properties.

        :return: The environment's green color value.
        :rtype: int
        :raises AttributeError: If app version is 1.x (RGB not supported)
        """
        if not self._is_rgb_supported():
            raise AttributeError(
                "RGB properties are not supported in Env module version 1.x. "
                "Please upgrade to version 2.x or above."
            )

        offset = Env.PROPERTY_OFFSET_GREEN
        raw = self._get_property(Env.PROPERTY_ENV_STATE)
        data = struct.unpack("h", raw[offset:offset + 2])[0]
        return data

    @property
    def blue(self) -> int:
        """Returns the blue color value between 0 and 255

        Note: This property is only available in Env module version 2.x and above.
        Version 1.x does not support RGB properties.

        :return: The environment's blue color value.
        :rtype: int
        :raises AttributeError: If app version is 1.x (RGB not supported)
        """
        if not self._is_rgb_supported():
            raise AttributeError(
                "RGB properties are not supported in Env module version 1.x. "
                "Please upgrade to version 2.x or above."
            )

        offset = Env.PROPERTY_OFFSET_BLUE
        raw = self._get_property(Env.PROPERTY_ENV_STATE)
        data = struct.unpack("h", raw[offset:offset + 2])[0]
        return data

    @property
    def rgb(self) -> tuple:
        """Returns the RGB color values as a tuple (red, green, blue)

        Note: This property is only available in Env module version 2.x and above.
        Version 1.x does not support RGB properties.

        :return: Tuple of (red, green, blue) values, each between 0 and 255.
        :rtype: tuple
        :raises AttributeError: If app version is 1.x (RGB not supported)
        """
        if not self._is_rgb_supported():
            raise AttributeError(
                "RGB properties are not supported in Env module version 1.x. "
                "Please upgrade to version 2.x or above."
            )

        return (self.red, self.green, self.blue)
