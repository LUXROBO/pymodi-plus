import modi_plus
from playscii import GameManager, GameObject
from math import sin, radians


class BrushManager(GameManager):
    def __init__(self, size, imu, button):
        super().__init__(size)
        self.cursor = Brush(pos=(size[0] // 2, size[1] // 2), render="o")
        self.imu = imu
        self.button = button

    def setup(self):
        self.add_object(self.cursor)

    def update(self):
        h, w = self.height // 2, self.width // 2
        self.cursor.y = h - h * sin(radians(-self.imu.roll))
        self.cursor.x = w - w * sin(radians(-self.imu.pitch))
        if self.button.pressed:
            self.add_object(Brush((self.cursor.x, self.cursor.y), "x"))


class Brush(GameObject):
    def update(self):
        pass


if __name__ == "__main__":
    bundle = modi_plus.MODIPlus()
    canvas = BrushManager((100, 20), bundle.imus[0], bundle.buttons[0])
    canvas.start()
