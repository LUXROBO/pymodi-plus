import time

from typing import Tuple, List, Union
from modi.module.module import Module
from modi.util.message_util import parse_message, parse_data


class OutputModule(Module):

    INT = 0
    FLOAT = 1
    STRING = 2
    RAW = 3
    DISPLAY_VAR = 4

    @staticmethod
    def __parse_set_message(destination_id: int,
                            property_num: int,
                            property_values: Tuple) -> List[str]:

        """Generate set_property json serialized message
        :param destination_id: Id of the destination module
        :type destination_id: int
        :param property_num: Property Type
        :type property_num: int
        :param property_values: Property values
        :type property_values: Tuple
        :return: List of json messages
        :rtype: List[str]
        """

        data = []
        for value_type, value in property_values:
            data += parse_data(value, value_type)
            # TODO: exception need
        return parse_message(0x04, property_num, destination_id, data)

    def _set_property(self, destination_id: int,
                      property_num: int, 
                      property_values: Union[Tuple, str]) -> None:
        """Send the message of set_property command to the module

        :param destination_id: Id of the destination module
        :type destination_id: int
        :param property_num: Property Type
        :type property_num: int
        :param property_values: Property Values
        :type property_values: Tuple
        :return: None
        """
        messages = self.__parse_set_message(
            destination_id,
            property_num,
            property_values,
        )

        for message in messages:
            self._conn.send(message)
            time.sleep(0.01)

    @staticmethod
    def _validate_property(nb_values: int, value_range: Tuple = None):
        def check_value(setter):
            def set_property(self, value):
                if nb_values > 1 and isinstance(value, int):
                    raise ValueError(f"{setter.__name__} needs {nb_values} "
                                     f"values")
                elif value_range and nb_values == 1 and not (
                        value_range[1] >= value >= value_range[0]):
                    raise ValueError(f"{setter.__name__} should be in range "
                                     f"{value_range[0]}~{value_range[1]}")
                elif value_range and nb_values > 1:
                    for val in value:
                        if not (value_range[1] >= val >= value_range[0]):
                            raise ValueError(f"{setter.__name__} "
                                             f"should be in range"
                                             f" {value_range[0]}~"
                                             f"{value_range[1]}")
                setter(self, value)

            return set_property
        return check_value
