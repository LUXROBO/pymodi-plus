import unittest

from modi_plus.module.input_module.imu import Imu
from modi_plus.util.message_util import parse_message
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
        _ = self.imu.roll
        self.assertEqual(
            self.conn.send_list[0],
            parse_message(
                0x03, 0, -1, (Imu.PROP_ANGLE_STATE, None, self.imu.prop_samp_freq, None)
            )
        )

    def test_get_pitch(self):
        """Test get_pitch method."""
        _ = self.imu.pitch
        self.assertEqual(
            self.conn.send_list[0],
            parse_message(
                0x03, 0, -1, (Imu.PROP_ANGLE_STATE, None, self.imu.prop_samp_freq, None)
            )
        )

    def test_get_yaw(self):
        """Test get_yaw method."""
        _ = self.imu.yaw
        self.assertEqual(
            self.conn.send_list[0],
            parse_message(
                0x03, 0, -1, (Imu.PROP_ANGLE_STATE, None, self.imu.prop_samp_freq, None)
            )
        )

    def test_get_angular_vel_x(self):
        """Test get_angular_vel_x method."""
        _ = self.imu.angular_vel_x
        self.assertEqual(
            self.conn.send_list[0],
            parse_message(
                0x03, 0, -1,
                (Imu.PROP_GYRO_STATE, None, self.imu.prop_samp_freq, None)
            )
        )

    def test_get_angular_vel_y(self):
        """Test get_angular_vel_y method."""
        _ = self.imu.angular_vel_y
        self.assertEqual(
            self.conn.send_list[0],
            parse_message(
                0x03, 0, -1,
                (Imu.PROP_GYRO_STATE, None, self.imu.prop_samp_freq, None)
            )
        )

    def test_get_angular_vel_z(self):
        """Test get_angular_vel_z method."""
        _ = self.imu.angular_vel_z
        self.assertEqual(
            self.conn.send_list[0],
            parse_message(
                0x03, 0, -1,
                (Imu.PROP_GYRO_STATE, None, self.imu.prop_samp_freq, None)
            )
        )

    def test_get_acceleration_x(self):
        """Test get_acceleration_x method."""
        _ = self.imu.acceleration_x
        self.assertEqual(
            self.conn.send_list[0],
            parse_message(
                0x03, 0, -1,
                (Imu.PROP_ACC_STATE, None, self.imu.prop_samp_freq, None)
            )
        )

    def test_get_acceleration_y(self):
        """Test get_acceleration_x method."""
        _ = self.imu.acceleration_y
        self.assertEqual(
            self.conn.send_list[0],
            parse_message(
                0x03, 0, -1,
                (Imu.PROP_ACC_STATE, None, self.imu.prop_samp_freq, None)
            )
        )

    def test_get_acceleration_z(self):
        """Test get_acceleration_z method."""
        _ = self.imu.acceleration_z
        self.assertEqual(
            self.conn.send_list[0],
            parse_message(
                0x03, 0, -1,
                (Imu.PROP_ACC_STATE, None, self.imu.prop_samp_freq, None)
            )
        )

    def test_get_vibration(self):
        """Test get_vibration method."""
        _ = self.imu.vibration
        self.assertEqual(
            self.conn.send_list[0],
            parse_message(
                0x03, 0, -1,
                (Imu.PROP_VIBRATION_STATE, None, self.imu.prop_samp_freq, None)
            )
        )


if __name__ == "__main__":
    unittest.main()