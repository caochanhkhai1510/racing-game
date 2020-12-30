from collections import namedtuple
import arcade



class Player(arcade.Sprite):
    def __init__(self, filename, sprite_scaling):
        super().__init__(filename, sprite_scaling)
        self.name = None
        self.money = 0
        self.speed = 0

    def setup(self, start_x, start_y, name, money, speed):
        self.name = name
        self.money = money
        self.speed = speed
        self.change_x = self.speed
        self.center_x = start_x
        self.center_y = start_y

    def on_update(self, delta_time: float):
        self.center_x += self.change_x * delta_time