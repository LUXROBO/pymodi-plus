import unittest

from modi_plus.module.input_module.env import Env
from modi_plus.util.message_util import parse_get_property_message
from modi_plus.util.connection_util import MockConn


class TestEnv(unittest.TestCase):
    """Tests for 'Env' class."""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.conn = MockConn()
        mock_args = (-1, -1, self.conn)
        self.env = Env(*mock_args)

    def tearDown(self):
        """Tear down test fixtures, if any."""
        del self.env

    def test_get_temperature(self):
        """Test get_temperature method."""
        _ = self.env.temperature
        self.assertEqual(
            self.conn.send_list[0],
            parse_get_property_message(-1, Env.PROPERTY_ENV_STATE, self.env.prop_samp_freq)
        )

    def test_get_humidity(self):
        """Test get_humidity method."""
        _ = self.env.humidity
        self.assertEqual(
            self.conn.send_list[0],
            parse_get_property_message(-1, Env.PROPERTY_ENV_STATE, self.env.prop_samp_freq)
        )

    def test_get_intensity(self):
        """Test get_intensity method."""
        _ = self.env.intensity
        self.assertEqual(
            self.conn.send_list[0],
            parse_get_property_message(-1, Env.PROPERTY_ENV_STATE, self.env.prop_samp_freq)
        )

    def test_get_volume(self):
        """Test get_volume method."""
        _ = self.env.volume
        self.assertEqual(
            self.conn.send_list[0],
            parse_get_property_message(-1, Env.PROPERTY_ENV_STATE, self.env.prop_samp_freq)
        )


if __name__ == "__main__":
    unittest.main()
