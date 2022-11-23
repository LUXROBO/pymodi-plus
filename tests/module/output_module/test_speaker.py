import unittest

from modi_plus.module.output_module.speaker import Speaker
from modi_plus.util.message_util import parse_set_property_message, parse_get_property_message
from modi_plus.util.unittest_util import MockConnection, MockSpeaker


class TestSpeaker(unittest.TestCase):
    """Tests for 'Speaker' class."""

    def setUp(self):
        """Set up test fixtures, if any."""

        self.connection = MockConnection()
        self.mock_kwargs = [-1, -1, self.connection]
        self.speaker = MockSpeaker(*self.mock_kwargs)

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
        while self.connection.send_list:
            sent_messages.append(self.connection.send_list.pop())
        self.assertTrue(set_message in sent_messages)

    def test_get_frequency(self):
        """Test get_frequency method with none input."""

        _ = self.speaker.frequency
        self.assertEqual(
            self.connection.send_list[0],
            parse_get_property_message(-1, Speaker.PROPERTY_SPEAKER_STATE, self.speaker.prop_samp_freq)
        )
        self.assertEqual(_, 0)

    def test_get_volume(self):
        """Test get_volume method with none input."""

        _ = self.speaker.volume
        self.assertEqual(
            self.connection.send_list[0],
            parse_get_property_message(-1, Speaker.PROPERTY_SPEAKER_STATE, self.speaker.prop_samp_freq)
        )
        self.assertEqual(_, 0)

    def test_reset(self):
        """Test reset method"""

        frequency, volume = 0, 0
        self.speaker.reset()
        set_message = parse_set_property_message(
            -1, Speaker.PROPERTY_SPEAKER_SET_TUNE,
            (("u16", frequency), ("u16", volume), )
        )
        sent_messages = []
        while self.connection.send_list:
            sent_messages.append(self.connection.send_list.pop())
        self.assertTrue(set_message in sent_messages)


if __name__ == "__main__":
    unittest.main()
