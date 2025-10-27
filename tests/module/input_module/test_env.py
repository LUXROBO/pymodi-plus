import unittest
import struct

from modi_plus.module.input_module.env import Env
from modi_plus.util.message_util import parse_get_property_message
from modi_plus.util.unittest_util import MockConnection, MockEnv


class TestEnv(unittest.TestCase):
    """Tests for 'Env' class."""

    def setUp(self):
        """Set up test fixtures, if any."""

        self.connection = MockConnection()
        mock_args = (-1, -1, self.connection)
        self.env = MockEnv(*mock_args)

    def tearDown(self):
        """Tear down test fixtures, if any."""

        del self.env

    def test_get_temperature(self):
        """Test get_temperature method."""

        _ = self.env.temperature
        self.assertEqual(
            self.connection.send_list[0],
            parse_get_property_message(-1, Env.PROPERTY_ENV_STATE, self.env.prop_samp_freq)
        )
        self.assertEqual(_, 0)

    def test_get_humidity(self):
        """Test get_humidity method."""

        _ = self.env.humidity
        self.assertEqual(
            self.connection.send_list[0],
            parse_get_property_message(-1, Env.PROPERTY_ENV_STATE, self.env.prop_samp_freq)
        )
        self.assertEqual(_, 0)

    def test_get_illuminance(self):
        """Test get_illuminance method."""

        _ = self.env.illuminance
        self.assertEqual(
            self.connection.send_list[0],
            parse_get_property_message(-1, Env.PROPERTY_ENV_STATE, self.env.prop_samp_freq)
        )
        self.assertEqual(_, 0)

    def test_get_volume(self):
        """Test get_volume method."""

        _ = self.env.volume
        self.assertEqual(
            self.connection.send_list[0],
            parse_get_property_message(-1, Env.PROPERTY_ENV_STATE, self.env.prop_samp_freq)
        )
        self.assertEqual(_, 0)


class TestEnvRGBVersion1(unittest.TestCase):
    """Tests for RGB properties with app version 1.x (not supported)."""

    def setUp(self):
        """Set up test fixtures with version 1.x."""
        self.connection = MockConnection()
        mock_args = (-1, -1, self.connection)
        self.env = MockEnv(*mock_args)

        # Set app version to 1.5.0 (major version = 1)
        # Version format: major << 13 | minor << 8 | patch
        # 1.5.0 = (1 << 13) | (5 << 8) | 0 = 8192 + 1280 = 9472
        version_1_5_0 = (1 << 13) | (5 << 8) | 0
        self.env.app_version = version_1_5_0

    def tearDown(self):
        """Tear down test fixtures."""
        del self.env

    def test_rgb_not_supported_version_1(self):
        """Test that RGB properties raise AttributeError in version 1.x."""
        with self.assertRaises(AttributeError) as context:
            _ = self.env.red
        self.assertIn("not supported in Env module version 1.x", str(context.exception))

    def test_green_not_supported_version_1(self):
        """Test that green property raises AttributeError in version 1.x."""
        with self.assertRaises(AttributeError) as context:
            _ = self.env.green
        self.assertIn("not supported in Env module version 1.x", str(context.exception))

    def test_blue_not_supported_version_1(self):
        """Test that blue property raises AttributeError in version 1.x."""
        with self.assertRaises(AttributeError) as context:
            _ = self.env.blue
        self.assertIn("not supported in Env module version 1.x", str(context.exception))

    def test_rgb_tuple_not_supported_version_1(self):
        """Test that rgb tuple property raises AttributeError in version 1.x."""
        with self.assertRaises(AttributeError) as context:
            _ = self.env.rgb
        self.assertIn("not supported in Env module version 1.x", str(context.exception))

    def test_is_rgb_supported_version_1(self):
        """Test _is_rgb_supported returns False for version 1.x."""
        self.assertFalse(self.env._is_rgb_supported())


class TestEnvRGBVersion2(unittest.TestCase):
    """Tests for RGB properties with app version 2.x (supported)."""

    def setUp(self):
        """Set up test fixtures with version 2.x."""
        self.connection = MockConnection()
        mock_args = (-1, -1, self.connection)
        self.env = MockEnv(*mock_args)

        # Set app version to 2.0.0 (major version = 2)
        # Version format: major << 13 | minor << 8 | patch
        # 2.0.0 = (2 << 13) | (0 << 8) | 0 = 16384
        version_2_0_0 = (2 << 13) | (0 << 8) | 0
        self.env.app_version = version_2_0_0

    def tearDown(self):
        """Tear down test fixtures."""
        del self.env

    def test_get_red(self):
        """Test get_red method with version 2.x."""
        _ = self.env.red
        self.assertEqual(
            self.connection.send_list[0],
            parse_get_property_message(-1, Env.PROPERTY_ENV_STATE, self.env.prop_samp_freq)
        )
        self.assertEqual(_, 0)

    def test_get_green(self):
        """Test get_green method with version 2.x."""
        _ = self.env.green
        # Green is the second call (red was first in previous test setup)
        # But in isolated test, this is first
        self.assertEqual(
            self.connection.send_list[0],
            parse_get_property_message(-1, Env.PROPERTY_ENV_STATE, self.env.prop_samp_freq)
        )
        self.assertEqual(_, 0)

    def test_get_blue(self):
        """Test get_blue method with version 2.x."""
        _ = self.env.blue
        self.assertEqual(
            self.connection.send_list[0],
            parse_get_property_message(-1, Env.PROPERTY_ENV_STATE, self.env.prop_samp_freq)
        )
        self.assertEqual(_, 0)

    def test_get_rgb_tuple(self):
        """Test get_rgb tuple method with version 2.x."""
        result = self.env.rgb
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 3)
        self.assertEqual(result, (0, 0, 0))

    def test_is_rgb_supported_version_2(self):
        """Test _is_rgb_supported returns True for version 2.x."""
        self.assertTrue(self.env._is_rgb_supported())

    def test_rgb_property_offsets(self):
        """Test that RGB properties use correct offsets."""
        self.assertEqual(Env.PROPERTY_OFFSET_RED, 8)
        self.assertEqual(Env.PROPERTY_OFFSET_GREEN, 10)
        self.assertEqual(Env.PROPERTY_OFFSET_BLUE, 12)


class TestEnvRGBVersion3(unittest.TestCase):
    """Tests for RGB properties with app version 3.x (also supported)."""

    def setUp(self):
        """Set up test fixtures with version 3.x."""
        self.connection = MockConnection()
        mock_args = (-1, -1, self.connection)
        self.env = MockEnv(*mock_args)

        # Set app version to 3.2.1 (major version = 3)
        # Version format: major << 13 | minor << 8 | patch
        # 3.2.1 = (3 << 13) | (2 << 8) | 1 = 24576 + 512 + 1 = 25089
        version_3_2_1 = (3 << 13) | (2 << 8) | 1
        self.env.app_version = version_3_2_1

    def tearDown(self):
        """Tear down test fixtures."""
        del self.env

    def test_is_rgb_supported_version_3(self):
        """Test _is_rgb_supported returns True for version 3.x."""
        self.assertTrue(self.env._is_rgb_supported())

    def test_rgb_works_in_version_3(self):
        """Test that RGB properties work in version 3.x."""
        # Should not raise any exception
        _ = self.env.red
        _ = self.env.green
        _ = self.env.blue
        rgb = self.env.rgb
        self.assertEqual(rgb, (0, 0, 0))


class TestEnvRGBNoVersion(unittest.TestCase):
    """Tests for RGB properties when app version is not set."""

    def setUp(self):
        """Set up test fixtures without setting version."""
        self.connection = MockConnection()
        mock_args = (-1, -1, self.connection)
        self.env = MockEnv(*mock_args)
        # Don't set app_version - it should be None by default

    def tearDown(self):
        """Tear down test fixtures."""
        del self.env

    def test_rgb_not_supported_no_version(self):
        """Test that RGB properties raise AttributeError when version is not set."""
        with self.assertRaises(AttributeError):
            _ = self.env.red

    def test_is_rgb_supported_no_version(self):
        """Test _is_rgb_supported returns False when version is not set."""
        self.assertFalse(self.env._is_rgb_supported())


if __name__ == "__main__":
    unittest.main()
