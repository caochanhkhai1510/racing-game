import arcade
from gameparams import *
from gameview import GameView



def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game = GameView()
    game.setup()
    window.show_view(game)
    arcade.run()



if __name__ == "__main__":
    main()