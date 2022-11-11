"""Motor module."""
import struct
from typing import Tuple
from modi_plus.module.output_module.output_module import OutputModule


class Motor(OutputModule):

    PROPERTY_MOTOR_STATE = 2

    PROPERTY_MOTOR_VELOCITY = 17
    PROPERTY_MOTOR_ANGLE = 18
    PROPERTY_MOTOR_ANGLE_APPEND = 19
    PROPERTY_MOTOR_STOP = 20

    PROPERTY_OFFSET_CURRENT_ANGLE = 0
    PROPERTY_OFFSET_CURRENT_VELOCITY = 2
    PROPERTY_OFFSET_TARGET_ANGLE = 4
    PROPERTY_OFFSET_TARGET_SPEED = 6

    @property
    def angle(self) -> float:
        """Returns current angle

        :return: current angle value
        :rtype: float
        """
        offset = Motor.PROPERTY_OFFSET_CURRENT_ANGLE
        raw = self._get_property(Motor.PROPERTY_MOTOR_STATE)
        data = struct.unpack("H", raw[offset:offset+2])[0]
        return data

    @property
    def target_angle(self) -> float:
        """Returns current angle

        :return: current angle value
        :rtype: float
        """
        offset = Motor.PROPERTY_OFFSET_TARGET_ANGLE
        raw = self._get_property(Motor.PROPERTY_MOTOR_STATE)
        data = struct.unpack("H", raw[offset:offset+2])[0]
        return data

    @property
    def velocity(self) -> float:
        """Returns current velocity

        :return: current velocity value
        :rtype: float
        """
        offset = Motor.PROPERTY_OFFSET_CURRENT_VELOCITY
        raw = self._get_property(Motor.PROPERTY_MOTOR_STATE)
        data = struct.unpack("H", raw[offset:offset+2])[0]
        return data

    @property
    def target_velocity(self) -> float:
        """Returns current velocity

        :return: current velocity value
        :rtype: float
        """
        offset = Motor.PROPERTY_OFFSET_TARGET_VELOCITY
        raw = self._get_property(Motor.PROPERTY_MOTOR_STATE)
        data = struct.unpack("H", raw[offset:offset+2])[0]
        return data

    def set_angle(self, target_angle: int, target_speed: int) -> None:
        """Sets the angle of the motor

        :param target_angle: Angle to set the motor.
        :type target_angle: int
        :param target_speed: Speed to reach target angle.
        :type target_angle: int
        :return: None
        """
        self._set_property(
            destination_id=self._id,
            property_num=Motor.PROPERTY_MOTOR_ANGLE,
            property_values=(('u16', target_angle),
                             ('u16', target_speed))
        )
        self._target_angle = target_angle

    def set_velocity(self, target_velocity: int) -> None:
        """Sets the velocity of the motor at channel I

        :param target_velocity: Velocity to set the motor.
        :type target_velocity: int
        :return: None
        """
        
        self._set_property(
            destination_id=self._id,
            property_num=Motor.PROPERTY_MOTOR_VELOCITY,
            property_values=(('s32', target_velocity),)
        )
        self._target_velocity = target_velocity

    def append_angle(self, target_angle, target_speed) -> None:
        """append the angle form current angle of the motor

        :param target_angle: Angle to append the motor angle.
        :type target_angle: int
        :param target_speed: Speed to reach target angle.
        :type target_angle: int
        :return: None
        """
        self._set_property(
            destination_id=self._id,
            property_num=Motor.PROPERTY_MOTOR_ANGLE_APPEND,
            property_values=(('s16', target_angle),
                             ('u16', target_speed))
        )
    
    def stop(self) -> None:
        """Stop operating motor

        :return: None
        """
        self._set_property(
            destination_id=self._id,
            property_num=Motor.PROPERTY_MOTOR_STOP,
            property_values=()
        )