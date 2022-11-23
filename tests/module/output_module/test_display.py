import unittest

from modi_plus.module.output_module.display import Display
from modi_plus.util.message_util import parse_set_property_message
from modi_plus.util.unittest_util import MockConnection, MockDisplay


class TestDisplay(unittest.TestCase):
    """Tests for 'Display' class."""

    def setUp(self):
        """Set up test fixtures, if any."""

        self.connection = MockConnection()
        self.mock_kwargs = [-1, -1, self.connection]
        self.display = MockDisplay(*self.mock_kwargs)

    def tearDown(self):
        """Tear down test fixtures, if any."""

        del self.display

    def test_write_text(self):
        """Test write_text method."""

        mock_text = "abcd"
        self.display.write_text(mock_text)
        set_message = parse_set_property_message(
            -1, Display.PROPERTY_DISPLAY_WRITE_TEXT,
            (("string", mock_text), )
        )
        sent_messages = []
        while self.connection.send_list:
            sent_messages.append(self.connection.send_list.pop())
        self.assertTrue(set_message in sent_messages)

    def test_write_variable(self):
        """Test write_variable method."""

        mock_variable = 123
        mock_position = 5
        self.display.write_variable(mock_position, mock_position, mock_variable)
        set_message = parse_set_property_message(
            -1, Display.PROPERTY_DISPLAY_WRITE_VARIABLE,
            (("u8", mock_position), ("u8", mock_position), ("float", mock_variable), )
        )
        sent_messages = []
        while self.connection.send_list:
            sent_messages.append(self.connection.send_list.pop())
        self.assertTrue(set_message in sent_messages)

    def test_reset(self):
        """Test reset method."""

        self.display.reset()
        set_message = parse_set_property_message(
            -1, Display.PROPERTY_DISPLAY_RESET,
            (("u8", 0), )
        )
        sent_messages = []
        while self.connection.send_list:
            sent_messages.append(self.connection.send_list.pop())
        self.assertTrue(set_message in sent_messages)


if __name__ == "__main__":
    unittest.main()
