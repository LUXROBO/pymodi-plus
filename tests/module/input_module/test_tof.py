import unittest

from modi_plus.module.input_module.tof import Tof
from modi_plus.util.message_util import parse_get_property_message
from modi_plus.util.connection_util import MockConn


class TestTof(unittest.TestCase):
    """Tests for 'Tof' class."""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.conn = MockConn()
        mock_args = (-1, -1, self.conn)
        self.tof = Tof(*mock_args)

    def tearDown(self):
        """Tear down test fixtures, if any."""
        del self.tof

    def test_get_distance(self):
        """Test get_distance method."""
        _ = self.tof.distance
        self.assertEqual(
            self.conn.send_list[0],
            parse_get_property_message(-1, Tof.PROPERTY_DISTANCE_STATE, self.tof.prop_samp_freq)
        )


if __name__ == "__main__":
    unittest.main()
