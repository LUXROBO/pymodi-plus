"""Display module."""

from modi_plus.module.output_module.output_module import OutputModule


class Display(OutputModule):

    TEXT = 17
    CLEAR = 21
    DOT = 18
    IMAGE = 19
    VARIABLE = 22
    OFFSET = 25
    MOVE = 26

    def __init__(self, id_, uuid, msg_send_q):
        super().__init__(id_, uuid, msg_send_q)
        self._text = ""

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text: str) -> None:
        """Clears the display and show the input string on the display.
        Returns the json serialized signal sent to the module
        to display the text

        :param text: Text to display.
        :type text: str
        :return: None
        """
        # self.clear()
        string_cursor = 0
        if len(text) >= 24:
            for num in range(len(text)//24):
                self._set_property(
                    self._id,
                    Display.TEXT,
                    property_values=(("string", str(text)[string_cursor:string_cursor+24]),) # 24 characters can be sent per one packet
                )
                string_cursor += 24

        self._set_property(
            self._id,
            Display.TEXT,
            property_values=(("string", str(text)[string_cursor:] + "\0"),)
        )
        self._text = text

    def show_variable(self, variable: float, position_x: int,
                      position_y: int) -> None:
        """Clears the display and show the input variable on the display.
        Returns the json serialized signal sent to
        the module to display the text

        :param variable: variable to display.
        :type variable: float
        :param position_x: x coordinate of the desired position
        :type position_x: int
        :param position_y: y coordinate of te desired position
        :type position_y: int
        :return: A json serialized signal to module
        :rtype: string
        """
        self._set_property(
            self._id,
            Display.VARIABLE,
            property_values=(("u8", position_x), 
                             ("u8", position_y),
                             ("float",variable))
        )
        self._text += str(variable)

    def draw_image(self, position_x: int, position_y: int, image_name: int) -> None:
        """Clears the display and show the input variable on the display.
        Returns the json serialized signal sent to
        the module to display the text

        :param variable: variable to display.
        :type variable: float
        :param position_x: x coordinate of the desired position
        :type position_x: int
        :param position_y: y coordinate of te desired position
        :type position_y: int
        :return: A json serialized signal to module
        :rtype: string
        """
        self._set_property(
            self._id,
            Display.IMAGE,
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
            Display.OFFSET,
            property_values=(("s8", position_x),
                             ("s8", position_y) )
        )

    def set_move(self, move_x: int, move_y: int) -> None:
        """Move the screen by move_x and move_y

        :param move_x: Xaxis movement value
        :type move_x: int
        :param move_y: Yaxis movement value
        :type move_y: int
        :return: None
        """
        self._set_property(
            self.id,
            Display.MOVE,
            property_values=(("s8", move_x),
                             ("s8", move_y) )
        )

    def clear(self) -> None:
        """Clear the screen.

        :return: json serialized message to te module
        :rtype: string
        """
        self._set_property(
            self._id,
            Display.CLEAR,
            property_values=(("u8", 0),)
        )
        self._text = ""
