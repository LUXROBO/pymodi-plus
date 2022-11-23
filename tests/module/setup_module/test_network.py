import unittest

from modi_plus.module.setup_module.network import Network
from modi_plus.util.message_util import parse_set_property_message, parse_get_property_message
from modi_plus.util.unittest_util import MockConnection, MockNetwork


class TestNetwork(unittest.TestCase):
    """Tests for 'Network' class."""

    def setUp(self):
        """Set up test fixtures, if any."""

        self.connection = MockConnection()
        self.mock_kwargs = [-1, -1, self.connection]
        self.network = MockNetwork(*self.mock_kwargs)

    def tearDown(self):
        """Tear down test fixtures, if any."""

        del self.network

    def test_received_data(self):
        """Test received_data method."""

        _ = self.network.received_data(0)
        self.assertEqual(
            self.connection.send_list[0],
            parse_get_property_message(-1, Network.PROPERTY_NETWORK_RECEIVE_DATA, self.network.prop_samp_freq)
        )
        self.assertEqual(_, 0.0)

    def test_button_clicked(self):
        """Test button_clicked method."""

        _ = self.network.button_clicked(0)
        self.assertEqual(
            self.connection.send_list[0],
            parse_get_property_message(-1, Network.PROPERTY_NETWORK_BUTTON, self.network.prop_samp_freq)
        )
        self.assertEqual(_, False)

    def test_send_data(self):
        """Test send_data method."""

        data = 123
        self.network.send_data(0, data)
        set_message = parse_set_property_message(
            -1, Network.PROPERTY_NETWORK_SEND_DATA,
            (("s32", data),)
        )
        sent_messages = []
        while self.connection.send_list:
            sent_messages.append(self.connection.send_list.pop())
        self.assertTrue(set_message in sent_messages)

    def test_send_text(self):
        """Test send_text method."""

        text = "MODI+"
        self.network.send_text(text)
        set_message = parse_set_property_message(
            -1, Network.PROPERTY_NETWORK_SEND_TEXT,
            (("string", text), )
        )
        sent_messages = []
        while self.connection.send_list:
            sent_messages.append(self.connection.send_list.pop())
        self.assertTrue(set_message in sent_messages)


if __name__ == "__main__":
    unittest.main()
