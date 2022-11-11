"""Motor module."""

from typing import Tuple
from modi_plus.module.output_module.output_module import OutputModule


class Motor(OutputModule):

    PROPERTY_MOTOR_STATE = 2

    PROPERTY_MOTOR_SPEED = 17
    PROPERTY_MOTOR_ANGLE = 18
    PROPERTY_MOTOR_ANGLE_APPEND = 19
    PROPERTY_MOTOR_STOP = 20

    PROPERTY_OFFSET_CURRENT_ANGLE = 0
    PROPERTY_OFFSET_CURRENT_SPEED = 2
    PROPERTY_OFFSET_TARGET_ANGLE = 4
    PROPERTY_OFFSET_TARGET_SPEED = 6

    @property
    def angle(self) -> float:
        """Returns first degree

        :return: first degree value
        :rtype: float
        """
        return self._get_property(Motor.PROPERTY_OFFSET_CURRENT_ANGLE)

    @angle.setter
    @OutputModule._validate_property(nb_values=2, value_range=(0, 360))
    def angle(self, target_value: Tuple[int, int]) -> None:
        """Sets the angle of the motor at channel I

        :param degree_value: Angle to set the first motor.
        :type degree_value: int
        :return: None
        """
        self._set_property(
            destination_id=self._id,
            property_num=Motor.PROPERTY_MOTOR_ANGLE,
            property_values=(('u16', target_value[0]),
                             ('u16', target_value[1]))
        )

    @property
    def speed(self) -> float:
        """Returns first degree

        :return: first degree value
        :rtype: float
        """
        return self._get_property(Motor.PROPERTY_OFFSET_CURRENT_ANGLE)

    @speed.setter
    @OutputModule._validate_property(nb_values=1, value_range=(-100, 100))
    def speed(self, target_speed: int) -> None:
        """Sets the speed of the motor at channel I

        :param degree_value: Angle to set the first motor.
        :type degree_value: int
        :return: None
        """
        
        self._set_property(
            destination_id=self._id,
            property_num=Motor.PROPERTY_MOTOR_SPEED,
            property_values=(('s32', target_speed),)
        )

    def angle_append(self, target_angle, target_speed) -> None:
        """Returns current angle

        :return: Angle of two motors
        :rtype: float
        """
        self._set_property(
            destination_id=self._id,
            property_num=Motor.PROPERTY_MOTOR_ANGLE_APPEND,
            property_values=(('s16', target_angle),
                             ('u16', target_speed))
        )
    
    def stop(self) -> None:
        """Returns current angle

        :return: Angle of two motors
        :rtype: float
        """
        self._set_property(
            destination_id=self._id,
            property_num=Motor.PROPERTY_MOTOR_STOP,
            property_values=()
        )