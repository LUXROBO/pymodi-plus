import unittest

from modi_plus.module.output_module.led import Led
from modi_plus.util.message_util import parse_set_property_message, parse_get_property_message
from modi_plus.util.unittest_util import MockConnection, MockLed


class TestLed(unittest.TestCase):
    """Tests for 'Led' class."""

    def setUp(self):
        """Set up test fixtures, if any."""

        self.connection = MockConnection()
        self.mock_kwargs = -1, -1, self.connection
        self.led = MockLed(*self.mock_kwargs)

    def tearDown(self):
        """Tear down test fixtures, if any."""

        del self.led

    def test_set_rgb(self):
        """Test set_rgb method with user-defined inputs."""

        red = 10
        green = 20
        blue = 100
        self.led.set_rgb(red, green, blue)
        set_message = parse_set_property_message(
            -1, Led.PROPERTY_LED_SET_RGB,
            (("u16", red), ("u16", green), ("u16", blue), )
        )
        sent_messages = []
        while self.connection.send_list:
            sent_messages.append(self.connection.send_list.pop())
        self.assertTrue(set_message in sent_messages)

    def test_get_red(self):
        """Test get_red method with none input."""

        _ = self.led.red
        self.assertEqual(
            self.connection.send_list[0],
            parse_get_property_message(-1, Led.PROPERTY_LED_STATE, self.led.prop_samp_freq)
        )
        self.assertEqual(_, 0)

    def test_get_green(self):
        """Test set_green method with none input."""

        _ = self.led.green
        self.assertEqual(
            self.connection.send_list[0],
            parse_get_property_message(-1, Led.PROPERTY_LED_STATE, self.led.prop_samp_freq)
        )
        self.assertEqual(_, 0)

    def test_get_blue(self):
        """Test get blue method with none input."""

        _ = self.led.blue
        self.assertEqual(
            self.connection.send_list[0],
            parse_get_property_message(-1, Led.PROPERTY_LED_STATE, self.led.prop_samp_freq)
        )
        self.assertEqual(_, 0)

    def test_turn_on(self):
        """Test turn_on method."""

        red = 100
        green = 100
        blue = 100
        self.led.turn_on()
        set_message = parse_set_property_message(
            -1, Led.PROPERTY_LED_SET_RGB,
            (("u16", red), ("u16", green), ("u16", blue), )
        )
        sent_messages = []
        while self.connection.send_list:
            sent_messages.append(self.connection.send_list.pop())
        self.assertTrue(set_message in sent_messages)

    def test_turn_off(self):
        """Test turn_off method."""

        red = 0
        green = 0
        blue = 0
        self.led.turn_off()
        set_message = parse_set_property_message(
            -1, Led.PROPERTY_LED_SET_RGB,
            (("u16", red), ("u16", green), ("u16", blue), )
        )
        sent_messages = []
        while self.connection.send_list:
            sent_messages.append(self.connection.send_list.pop())
        self.assertTrue(set_message in sent_messages)


if __name__ == "__main__":
    unittest.main()
