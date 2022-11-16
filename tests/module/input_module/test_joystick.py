import unittest

from modi_plus.module.input_module.joystick import Joystick
from modi_plus.util.message_util import parse_get_property_message
from modi_plus.util.connection_util import MockConn


class TestJoystick(unittest.TestCase):
    """Tests for 'Joystick' package."""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.conn = MockConn()
        mock_args = (-1, -1, self.conn)
        self.joystick = Joystick(*mock_args)

    def tearDown(self):
        """Tear down test fixtures, if any."""
        del self.joystick

    def test_get_x(self):
        """Test get_x method."""
        _ = self.joystick.x
        self.assertEqual(
            self.conn.send_list[0],
            parse_get_property_message(-1, Joystick.PROPERTY_POSITION_STATE, self.joystick.prop_samp_freq)
        )

    def test_get_y(self):
        """Test get_y method."""
        _ = self.joystick.y
        self.assertEqual(
            self.conn.send_list[0],
            parse_get_property_message(-1, Joystick.PROPERTY_POSITION_STATE, self.joystick.prop_samp_freq)
        )

    def test_get_dirction(self):
        """Test get_dirction method."""
        _ = self.joystick.direction
        self.assertEqual(
            self.conn.send_list[0],
            parse_get_property_message(-1, Joystick.PROPERTY_DIRECTION_STATE, self.joystick.prop_samp_freq)
        )


if __name__ == "__main__":
    unittest.main()
