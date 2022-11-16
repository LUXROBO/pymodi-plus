from typing import Tuple, Union
from modi_plus.module.module import Module
from modi_plus.util.message_util import parse_set_property_message


class OutputModule(Module):

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
        message = parse_set_property_message(
            destination_id,
            property_num,
            property_values,
        )
        self._conn.send(message)

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
