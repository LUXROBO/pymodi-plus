"""Imu module."""

import struct

from modi.module.input_module.input_module import InputModule

class Imu(InputModule):

    PROP_ANGLE_STATE = 2
    PROP_OFFSET_ROLL = 0
    PROP_OFFSET_PITCH = 4
    PROP_OFFSET_YAW = 8

    PROP_ACC_STATE = 3
    PROP_OFFSET_ACC_X = 0
    PROP_OFFSET_ACC_Y = 4
    PROP_OFFSET_ACC_Z = 8

    PROP_GYRO_STATE = 4
    PROP_OFFSET_GYRO_X = 0
    PROP_OFFSET_GYRO_Y = 4
    PROP_OFFSET_GYRO_Z = 8

    PROP_VIBRATION_STATE = 5
    PROP_OFFSET_VIBRATION = 0

    @property
    def roll(self) -> float:
        """Returns the roll angle of the imu

        :return: Roll angle.
        :rtype: float
        """

        offset = Imu.PROP_OFFSET_ROLL
        raw = self._get_property(Imu.PROP_ANGLE_STATE)
        data = struct.unpack('f', raw[offset:offset+4])[0]
        return data

    @property
    def pitch(self) -> float:
        """Returns the pitch angle of the imu

        :return: Pitch angle.
        :rtype: float
        """

        offset = Imu.PROP_OFFSET_PITCH
        raw = self._get_property(Imu.PROP_ANGLE_STATE)
        data = struct.unpack('f', raw[offset:offset+4])[0]
        return data

    @property
    def yaw(self) -> float:
        """Returns the yaw angle of the imu

        :return: Yaw angle.
        :rtype: float
        """

        offset = Imu.PROP_OFFSET_YAW
        raw = self._get_property(Imu.PROP_ANGLE_STATE)
        data = struct.unpack('f', raw[offset:offset+4])[0]
        return data

    @property
    def angle(self) -> list:
        """Returns the roll, pitch and yaw angle of the imu

        :return: angle.
        :rtype: list
        """

        return [self.roll, self.pitch, self.yaw]

    @property
    def angular_vel_x(self) -> float:
        """Returns the roll angle of the imu

        :return: Angular velocity the about x-axis.
        :rtype: float
        """

        offset = Imu.PROP_OFFSET_GYRO_X
        raw = self._get_property(Imu.PROP_GYRO_STATE)
        data = struct.unpack('f', raw[offset:offset+4])[0]
        return data

    @property
    def angular_vel_y(self) -> float:
        """Returns the angular velocity about y-axis

        :return: Angular velocity the about y-axis.
        :rtype: float
        """

        offset = Imu.PROP_OFFSET_GYRO_Y
        raw = self._get_property(Imu.PROP_GYRO_STATE)
        data = struct.unpack('f', raw[offset:offset+4])[0]
        return data

    @property
    def angular_vel_z(self) -> float:
        """Returns the angular velocity about z-axis

        :return: Angular velocity the about z-axis.
        :rtype: float
        """

        offset = Imu.PROP_OFFSET_GYRO_Z
        raw = self._get_property(Imu.PROP_GYRO_STATE)
        data = struct.unpack('f', raw[offset:offset+4])[0]
        return data

    @property
    def angular_velocity(self) -> list:
        """Returns the angular velocity about x, y and z axis

        :return: Angular velocity the about x, y and z axis.
        :rtype: list
        """

        return [self.angular_vel_x, self.angular_vel_y, self.angular_vel_z]

    @property
    def acceleration_x(self) -> float:
        """Returns the x component of the acceleration

        :return: X-axis acceleration.
        :rtype: float
        """

        offset = Imu.PROP_OFFSET_ACC_X
        raw = self._get_property(Imu.PROP_ACC_STATE)
        data = struct.unpack('f', raw[offset:offset+4])[0]
        return data

    @property
    def acceleration_y(self) -> float:
        """Returns the y component of the acceleration

        :return: Y-axis acceleration.
        :rtype: float
        """

        offset = Imu.PROP_OFFSET_ACC_Y
        raw = self._get_property(Imu.PROP_ACC_STATE)
        data = struct.unpack('f', raw[offset:offset+4])[0]
        return data

    @property
    def acceleration_z(self) -> float:
        """Returns the z component of the acceleration

        :return: Z-axis acceleration.
        :rtype: float
        """

        offset = Imu.PROP_OFFSET_ACC_Z
        raw = self._get_property(Imu.PROP_ACC_STATE)
        data = struct.unpack('f', raw[offset:offset+4])[0]
        return data

    @property
    def acceleration(self) -> list:
        """Returns the acceleration about x, y and z axis

        :return: Acceleration the about x, y and z axis.
        :rtype: list
        """

        return [self.acceleration_x, self.acceleration_y, self.acceleration_z]

    @property
    def vibration(self) -> float:
        """Returns the vibration value

        :return: Vibration.
        :rtype: float
        """

        offset = Imu.PROP_OFFSET_VIBRATION
        raw = self._get_property(Imu.PROP_VIBRATION_STATE)
        data = struct.unpack('f', raw[offset:offset+4])[0]
        return data
