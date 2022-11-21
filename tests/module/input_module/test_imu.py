import unittest

from modi_plus.module.module import Module
from modi_plus.module.input_module.imu import Imu
from modi_plus.util.message_util import parse_get_property_message
from modi_plus.util.connection_util import MockConn


class TestImu(unittest.TestCase):
    """Tests for 'Imu' class."""

    def setUp(self):
        """Set up test fixtures, if any."""

        self.conn = MockConn()
        mock_args = (-1, -1, self.conn)
        self.imu = Imu(*mock_args)

    def tearDown(self):
        """Tear down test fixtures, if any."""

        del self.imu

    def test_get_roll(self):
        """Test get_roll method."""

        try:
            _ = self.imu.roll
        except Module.GetValueInitTimeout:
            pass

        self.assertEqual(
            self.conn.send_list[0],
            parse_get_property_message(-1, Imu.PROPERTY_ANGLE_STATE, self.imu.prop_samp_freq)
        )

    def test_get_pitch(self):
        """Test get_pitch method."""

        try:
            _ = self.imu.pitch
        except Module.GetValueInitTimeout:
            pass

        self.assertEqual(
            self.conn.send_list[0],
            parse_get_property_message(-1, Imu.PROPERTY_ANGLE_STATE, self.imu.prop_samp_freq)
        )

    def test_get_yaw(self):
        """Test get_yaw method."""

        try:
            _ = self.imu.yaw
        except Module.GetValueInitTimeout:
            pass

        self.assertEqual(
            self.conn.send_list[0],
            parse_get_property_message(-1, Imu.PROPERTY_ANGLE_STATE, self.imu.prop_samp_freq)
        )

    def test_get_angular_vel_x(self):
        """Test get_angular_vel_x method."""

        try:
            _ = self.imu.angular_vel_x
        except Module.GetValueInitTimeout:
            pass

        self.assertEqual(
            self.conn.send_list[0],
            parse_get_property_message(-1, Imu.PROPERTY_GYRO_STATE, self.imu.prop_samp_freq)
        )

    def test_get_angular_vel_y(self):
        """Test get_angular_vel_y method."""

        try:
            _ = self.imu.angular_vel_y
        except Module.GetValueInitTimeout:
            pass

        self.assertEqual(
            self.conn.send_list[0],
            parse_get_property_message(-1, Imu.PROPERTY_GYRO_STATE, self.imu.prop_samp_freq)
        )

    def test_get_angular_vel_z(self):
        """Test get_angular_vel_z method."""

        try:
            _ = self.imu.angular_vel_z
        except Module.GetValueInitTimeout:
            pass

        self.assertEqual(
            self.conn.send_list[0],
            parse_get_property_message(-1, Imu.PROPERTY_GYRO_STATE, self.imu.prop_samp_freq)
        )

    def test_get_acceleration_x(self):
        """Test get_acceleration_x method."""

        try:
            _ = self.imu.acceleration_x
        except Module.GetValueInitTimeout:
            pass

        self.assertEqual(
            self.conn.send_list[0],
            parse_get_property_message(-1, Imu.PROPERTY_ACC_STATE, self.imu.prop_samp_freq)
        )

    def test_get_acceleration_y(self):
        """Test get_acceleration_x method."""

        try:
            _ = self.imu.acceleration_y
        except Module.GetValueInitTimeout:
            pass

        self.assertEqual(
            self.conn.send_list[0],
            parse_get_property_message(-1, Imu.PROPERTY_ACC_STATE, self.imu.prop_samp_freq)
        )

    def test_get_acceleration_z(self):
        """Test get_acceleration_z method."""

        try:
            _ = self.imu.acceleration_z
        except Module.GetValueInitTimeout:
            pass

        self.assertEqual(
            self.conn.send_list[0],
            parse_get_property_message(-1, Imu.PROPERTY_ACC_STATE, self.imu.prop_samp_freq)
        )

    def test_get_vibration(self):
        """Test get_vibration method."""

        try:
            _ = self.imu.vibration
        except Module.GetValueInitTimeout:
            pass

        self.assertEqual(
            self.conn.send_list[0],
            parse_get_property_message(-1, Imu.PROPERTY_VIBRATION_STATE, self.imu.prop_samp_freq)
        )


if __name__ == "__main__":
    unittest.main()
