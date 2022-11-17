import unittest

from modi_plus.module.output_module.speaker import Speaker
from modi_plus.util.message_util import parse_set_property_message, parse_get_property_message
from modi_plus.util.connection_util import MockConn


class TestSpeaker(unittest.TestCase):
    """Tests for 'Speaker' class."""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.conn = MockConn()
        self.mock_kwargs = [-1, -1, self.conn]
        self.speaker = Speaker(*self.mock_kwargs)

    def tearDown(self):
        """Tear down test fixtures, if any."""
        del self.speaker

    def test_set_tune(self):
        """Test set_tune method."""
        frequency, volume = 500, 30
        self.speaker.set_tune(frequency, volume)
        set_message = parse_set_property_message(
            -1, Speaker.PROPERTY_SPEAKER_SET_TUNE,
            (("u16", frequency), ("u16", volume), )
        )
        sent_messages = []
        while self.conn.send_list:
            sent_messages.append(self.conn.send_list.pop())
        self.assertTrue(set_message in sent_messages)

    def test_get_frequency(self):
        """Test get_frequency method with none input."""
        _ = self.speaker.frequency
        self.assertEqual(
            self.conn.send_list[0],
            parse_get_property_message(-1, Speaker.PROPERTY_SPEAKER_STATE, self.speaker.prop_samp_freq)
        )

    def test_get_volume(self):
        """Test get_volume method with none input."""
        _ = self.speaker.volume
        self.assertEqual(
            self.conn.send_list[0],
            parse_get_property_message(-1, Speaker.PROPERTY_SPEAKER_STATE, self.speaker.prop_samp_freq)
        )

    def test_set_off(self):
        """Test set_off method"""
        frequency, volume = 500, 0
        self.speaker.set_tune(frequency, volume)
        set_message = parse_set_property_message(
            -1, Speaker.PROPERTY_SPEAKER_SET_TUNE,
            (("u16", frequency), ("u16", volume), )
        )
        sent_messages = []
        while self.conn.send_list:
            sent_messages.append(self.conn.send_list.pop())
        self.assertTrue(set_message in sent_messages)


if __name__ == "__main__":
    unittest.main()
