import unittest

from modi_plus.module.input_module.dial import Dial
from modi_plus.util.message_util import parse_get_property_message
from modi_plus.util.connection_util import MockConn


class TestDial(unittest.TestCase):
    """Tests for 'Dial' class."""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.conn = MockConn()
        mock_args = (-1, -1, self.conn)
        self.dial = Dial(*mock_args)

    def tearDown(self):
        """Tear down test fixtures, if any."""
        del self.dial

    def test_get_degree(self):
        """Test get_degree method."""
        _ = self.dial.turn
        self.assertEqual(
            self.conn.send_list[0],
            parse_get_property_message(-1, Dial.PROPERTY_DIAL_STATE, self.dial.prop_samp_freq)
        )

    def test_get_speed(self):
        """Test get_speed method."""
        _ = self.dial.speed
        self.assertEqual(
            self.conn.send_list[0],
            parse_get_property_message(-1, Dial.PROPERTY_DIAL_STATE, self.dial.prop_samp_freq)
        )


if __name__ == "__main__":
    unittest.main()
