"""Tof module."""

import struct
from modi_plus.module.input_module.input_module import InputModule


class Tof(InputModule):

    PROP_DISTANCE_STATE = 2
    PROP_DISTANCE = 0

    @property
    def distance(self) -> float:
        """Returns the distance of te object between 0cm and 100cm

        :return: Distance to object.
        :rtype: float
        """

        offset = Tof.PROP_DISTANCE
        raw = self._get_property(Tof.PROP_DISTANCE_STATE)
        data = struct.unpack("f", raw[offset:offset+4])[0]
        return data
