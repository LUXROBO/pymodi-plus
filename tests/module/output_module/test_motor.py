import unittest

from modi_plus.module.output_module.motor import Motor
from modi_plus.util.message_util import parse_set_property_message, parse_get_property_message
from modi_plus.util.connection_util import MockConn


class TestMotor(unittest.TestCase):
    """Tests for 'Motor' class."""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.conn = MockConn()
        self.mock_kwargs = [-1, -1, self.conn]
        self.motor = Motor(*self.mock_kwargs)

    def tearDown(self):
        """Tear down test fixtures, if any."""
        del self.motor

    def test_set_speed(self):
        """Test set_speed method."""
        target_speed = 50
        self.motor.set_speed(target_speed)
        set_message = parse_set_property_message(
            -1, Motor.PROPERTY_MOTOR_SPEED,
            (("s32", target_speed), )
        )
        sent_messages = []
        while self.conn.send_list:
            sent_messages.append(self.conn.send_list.pop())
        self.assertTrue(set_message in sent_messages)

    def test_get_speed(self):
        """Test get_speed method with none input."""
        _ = self.motor.speed
        self.assertEqual(
            self.conn.send_list[0],
            parse_get_property_message(-1, Motor.PROPERTY_MOTOR_STATE, self.motor.prop_samp_freq)
        )

    def test_set_angle(self):
        """Test set_angle method."""
        target_angle, target_speed = 90, 50
        self.motor.set_angle(target_angle, target_speed)
        set_message = parse_set_property_message(
            -1, Motor.PROPERTY_MOTOR_ANGLE,
            (("u16", target_angle), ("u16", target_speed), )
        )
        sent_messages = []
        while self.conn.send_list:
            sent_messages.append(self.conn.send_list.pop())
        self.assertTrue(set_message in sent_messages)

    def test_get_angle(self):
        """Test get_angle method with none input."""
        _ = self.motor.angle
        self.assertEqual(
            self.conn.send_list[0],
            parse_get_property_message(-1, Motor.PROPERTY_MOTOR_STATE, self.motor.prop_samp_freq)
        )


if __name__ == "__main__":
    unittest.main()
