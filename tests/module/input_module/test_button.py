import unittest

from modi_plus.module.input_module.button import Button
from modi_plus.module.module import Module
from modi_plus.util.message_util import parse_get_property_message
from modi_plus.util.connection_util import MockConn


class TestButton(unittest.TestCase):
    """Tests for 'Button' class."""

    def setUp(self):
        """Set up test fixtures, if any."""

        self.conn = MockConn()
        mock_args = (-1, -1, self.conn)
        self.button = Button(*mock_args)

    def tearDown(self):
        """Tear down test fixtures, if any."""

        del self.button

    def test_get_clicked(self):
        """Test get_clicked method."""

        try:
            _ = self.button.clicked
        except Module.GetValueInitTimeout:
            pass

        self.assertEqual(
            self.conn.send_list[0],
            parse_get_property_message(-1, Button.PROPERTY_BUTTON_STATE, self.button.prop_samp_freq)
        )

    def test_get_double_clicked(self):
        """Test get_double_clicked method."""

        try:
            _ = self.button.double_clicked
        except Module.GetValueInitTimeout:
            pass

        self.assertEqual(
            self.conn.send_list[0],
            parse_get_property_message(-1, Button.PROPERTY_BUTTON_STATE, self.button.prop_samp_freq)
        )

    def test_get_pressed(self):
        """Test get_pressed method."""

        try:
            _ = self.button.pressed
        except Module.GetValueInitTimeout:
            pass

        self.assertEqual(
            self.conn.send_list[0],
            parse_get_property_message(-1, Button.PROPERTY_BUTTON_STATE, self.button.prop_samp_freq)
        )

    def test_get_toggled(self):
        """Test get_toggled method."""

        try:
            _ = self.button.toggled
        except Module.GetValueInitTimeout:
            pass

        self.assertEqual(
            self.conn.send_list[0],
            parse_get_property_message(-1, Button.PROPERTY_BUTTON_STATE, self.button.prop_samp_freq)
        )


if __name__ == "__main__":
    unittest.main()
