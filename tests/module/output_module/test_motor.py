import unittest

from modi_plus.module.output_module.motor import Motor
from modi_plus.util.message_util import parse_set_property_message, parse_get_property_message
from modi_plus.util.unittest_util import MockConnection, MockMotor


class TestMotor(unittest.TestCase):
    """Tests for 'Motor' class."""

    def setUp(self):
        """Set up test fixtures, if any."""

        self.connection = MockConnection()
        self.mock_kwargs = [-1, -1, self.connection]
        self.motor = MockMotor(*self.mock_kwargs)

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
        while self.connection.send_list:
            sent_messages.append(self.connection.send_list.pop())
        self.assertTrue(set_message in sent_messages)

    def test_get_speed(self):
        """Test get_speed method with none input."""

        _ = self.motor.speed
        self.assertEqual(
            self.connection.send_list[0],
            parse_get_property_message(-1, Motor.PROPERTY_MOTOR_STATE, self.motor.prop_samp_freq)
        )
        self.assertEqual(_, 0)

    def test_set_angle(self):
        """Test set_angle method."""

        target_angle, target_speed = 90, 50
        self.motor.set_angle(target_angle, target_speed)
        set_message = parse_set_property_message(
            -1, Motor.PROPERTY_MOTOR_ANGLE,
            (("u16", target_angle), ("u16", target_speed), )
        )
        sent_messages = []
        while self.connection.send_list:
            sent_messages.append(self.connection.send_list.pop())
        self.assertTrue(set_message in sent_messages)

    def test_get_angle(self):
        """Test get_angle method with none input."""

        _ = self.motor.angle
        self.assertEqual(
            self.connection.send_list[0],
            parse_get_property_message(-1, Motor.PROPERTY_MOTOR_STATE, self.motor.prop_samp_freq)
        )
        self.assertEqual(_, 0)


if __name__ == "__main__":
    unittest.main()
