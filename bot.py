import arcade



class Bot(arcade.Sprite):
    def __init__(self, filename, sprite_scaling):
        super().__init__(filename, sprite_scaling)
        self.speed = 0

    def setup(self, start_x, start_y, speed):
        self.speed = speed
        self.change_x = self.speed
        self.center_x = start_x
        self.center_y = start_y

    def on_update(self, delta_time: float):
        self.center_x += self.change_x * delta_time