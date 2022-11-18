"""Speaker module."""

import struct
from modi_plus.module.output_module.output_module import OutputModule


class Speaker(OutputModule):

    PROPERTY_SPEAKER_STATE = 2

    PROPERTY_SPEAKER_SET_TUNE = 16
    PROPERTY_SPEAKER_RESET = 17
    PROPERTY_SPEAKER_MUSIC = 18
    PROPERTY_SPEAKER_MELODY = 19

    STOP = 0
    START = 1
    PAUSE = 2
    RESUME = 3

    PROPERTY_OFFSET_CURRENT_VOLUME = 0
    PROPERTY_OFFSET_CURRENT_FREQUENCY = 2

    SCALE_TABLE = {
        "FA5": 698,
        "SOL5": 783,
        "LA5": 880,
        "TI5": 988,
        "DO#5": 554,
        "RE#5": 622,
        "FA#5": 739,
        "SOL#5": 830,
        "LA#5": 932,
        "DO6": 1046,
        "RE6": 1174,
        "MI6": 1318,
        "FA6": 1397,
        "SOL6": 1567,
        "LA6": 1760,
        "TI6": 1975,
        "DO#6": 1108,
        "RE#6": 1244,
        "FA#6": 1479,
        "SOL#6": 1661,
        "LA#6": 1864,
        "DO7": 2093,
        "RE7": 2349,
        "MI7": 2637
    }

    def __init__(self, id_, uuid, connection_task):
        super().__init__(id_, uuid, connection_task)

    def set_tune(self, frequency, volume) -> None:
        """Set tune for the speaker

        :param tune_value: Value of frequency and volume
        :type tune_value: Tuple[int, int]
        :return: None
        """
        tune_value = (frequency, volume)
        if isinstance(frequency, str):
            tune_value = (
                Speaker.SCALE_TABLE.get(tune_value[0], -1),
                tune_value[1]
            )

        if tune_value == (self.frequency, self.volume):
            return

        if tune_value[0] < 0:
            raise ValueError("Not a supported frequency value")

        self._set_property(
            destination_id=self._id,
            property_num=Speaker.PROPERTY_SPEAKER_SET_TUNE,
            property_values=(("u16", tune_value[0]),
                             ("u16", tune_value[1]))
        )

    @property
    def frequency(self) -> int:
        """Returns current frequency

        :return: frequency value
        :rtype: int
        """
        offset = Speaker.PROPERTY_OFFSET_CURRENT_FREQUENCY
        raw = self._get_property(Speaker.PROPERTY_SPEAKER_STATE)
        data = struct.unpack("H", raw[offset:offset + 2])[0]
        return data

    @property
    def volume(self) -> int:
        """Returns current volume

        :return: Volume value
        :rtype: int
        """
        offset = Speaker.PROPERTY_OFFSET_CURRENT_VOLUME
        raw = self._get_property(Speaker.PROPERTY_SPEAKER_STATE)
        data = struct.unpack("H", raw[offset:offset + 2])[0]
        return data

    def play_melody(self, cmd: int, volume: int, melody_name: str = "") -> None:
        """Play mid file in speaker module

        :param cmd: cmd to play melody (Stop, Start, Pause, Resume).
        :type cmd: int
        :param volume: volume of speaker
        :type volume: int
        :param melody_name: melody file name for playing
        :type melody_name: str
        :return: None
        """

        if len(melody_name) != 0:
            self.playing_file_name = melody_name
        self._set_property(
            self._id,
            Speaker.PROPERTY_SPEAKER_MELODY,
            property_values=(("u8", cmd),
                             ("u8", volume),
                             ("string", "res/" + self.playing_file_name))
        )

    def play_music(self, cmd: int, volume: int, music_name: str = "") -> None:
        """Play wav file in speaker module

        :param cmd: cmd to play music (Stop, Start, Pause, Resume).
        :type cmd: int
        :param volume: volume of speaker
        :type volume: int
        :param melody_name: music file name for playing
        :type melody_name: str
        :return: None
        """

        if len(music_name) != 0:
            self.playing_file_name = music_name
        self._set_property(
            self._id,
            Speaker.PROPERTY_SPEAKER_MUSIC,
            property_values=(("u8", cmd),
                             ("u8", volume),
                             ("string", "res/" + self.playing_file_name))
        )

    def reset(self) -> None:
        """Turn off the sound

        :return: None
        """
        self.set_tune(0, 0)
