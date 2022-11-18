"""Display module."""

from modi_plus.module.output_module.output_module import OutputModule


class Display(OutputModule):

    PROPERTY_DISPLAY_WRITE_TEXT = 17
    PROPERTY_DISPLAY_DRAW_DOT = 18
    PROPERTY_DISPLAY_DRAW_PICTURE = 19
    PROPERTY_DISPLAY_RESET = 21
    PROPERTY_DISPLAY_WRITE_VARIABLE = 22
    PROPERTY_DISPLAY_SET_PROPERTY = 25
    PROPERTY_DISPLAY_MOVE_SCREEN = 26

    def __init__(self, id_, uuid, msg_send_q):
        super().__init__(id_, uuid, msg_send_q)
        self._text = ""

    @property
    def text(self):
        return self._text

    def write_text(self, text: str) -> None:
        """Clears the display and show the input string on the display.
        Returns the json serialized signal sent to the module
        to display the text

        :param text: Text to display.
        :type text: str
        :return: None
        """
        # self.clear()
        if self._text == text:
            return

        string_cursor = 0
        encoding_data = str.encode(text)
        if len(encoding_data) >= 24:
            for num in range(len(encoding_data) // 24):
                self._set_property(
                    self._id,
                    Display.PROPERTY_DISPLAY_WRITE_TEXT,
                    property_values=(("bytes", encoding_data[string_cursor:string_cursor + 24]), )
                )
                string_cursor += 24

        self._set_property(
            self._id,
            Display.PROPERTY_DISPLAY_WRITE_TEXT,
            property_values=(("bytes", encoding_data[string_cursor:] + bytes(0)),)
        )
        self._text = text

    def write_variable(self, position_x: int, position_y: int, variable: float) -> None:
        """Clears the display and show the input variable on the display.
        Returns the json serialized signal sent to
        the module to display the text

        :param position_x: x coordinate of the desired position
        :type position_x: int
        :param position_y: y coordinate of te desired position
        :type position_y: int
        :param variable: variable to display.
        :type variable: float
        :return: None
        """
        self._set_property(
            self._id,
            Display.PROPERTY_DISPLAY_WRITE_VARIABLE,
            property_values=(("u8", position_x),
                             ("u8", position_y),
                             ("float", variable), )
        )
        self._text += str(variable)

    def draw_picture(self, position_x: int, position_y: int, image_name: int) -> None:
        """Clears the display and show the input variable on the display.
        Returns the json serialized signal sent to
        the module to display the text

        :param position_x: x coordinate of the desired position
        :type position_x: int
        :param position_y: y coordinate of te desired position
        :type position_y: int
        :param variable: picture name to display.
        :type variable: float
        :return: None
        """
        self._set_property(
            self._id,
            Display.PROPERTY_DISPLAY_DRAW_PICTURE,
            property_values=(("u8", position_x),
                             ("u8", position_y),
                             ("u8", 96),
                             ("u8", 96),
                             ("string", "res/" + image_name))
        )

    def set_offset(self, position_x: int, position_y: int) -> None:
        """Set origin point on the screen

        :param position_x: Xaxis offset on screen
        :type position_x: int
        :param position_y: Yaxis offset on screen
        :type position_y: int
        :return: None
        """
        self._set_property(
            self.id,
            Display.PROPERTY_DISPLAY_SET_PROPERTY,
            property_values=(("s8", position_x),
                             ("s8", position_y), )
        )

    def move_screen(self, move_x: int, move_y: int) -> None:
        """Move the screen by move_x and move_y

        :param move_x: Xaxis movement value
        :type move_x: int
        :param move_y: Yaxis movement value
        :type move_y: int
        :return: None
        """
        self._set_property(
            self.id,
            Display.PROPERTY_DISPLAY_MOVE_SCREEN,
            property_values=(("s8", move_x),
                             ("s8", move_y), )
        )

    def reset(self) -> None:
        """Clear the screen.

        :return: None
        """
        self._set_property(
            self._id,
            Display.PROPERTY_DISPLAY_RESET,
            property_values=(("u8", 0),)
        )
        self._text = ""
