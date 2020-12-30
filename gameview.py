import arcade
import random
from gameparams import *
from pathlib import Path
from player import Player
from bot import Bot
from pauseview import PauseView



class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.power_up_sprites_list = None
        self.player_sprite = None
        self.bot_sprites_list = None
        self.foreground_sprites_list = None
        self.background_sprites_list = None
        self.touch_this_sprites_list = None

         # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        # Keep track of the score
        self.score = 0

        # Where is the right edge of the map?
        self.end_of_map = 0

    def setup(self):
        """ Set up the game """

        # Get current directory of this file
        mod_path = Path(__file__).parent

        # Get player avatar directory
        player_avatar_path = 'avatars/Nv1_2.png/'

        # Get map directory
        map_path = 'maps/map1_16pixel.tmx/'

         # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        # Keep track of the score
        self.score = 0

        # Generate random positions 
        positions = random.sample(range(5), 5)

        # Generate random speeds
        speeds = random.sample(range(50, 150, 5), 5)

        # Set up player sprite
        avatar_name = (mod_path / player_avatar_path).resolve()
        self.player_sprite = Player(avatar_name, CHARACTER_SCALING)
        self.player_sprite.setup(CHARACTER_START_X + self.player_sprite.right + 5, 
                                 CHARACTER_START_Y[positions[4]], 'Khai', 100, speeds[4])

        # Set up bot sprites
        self.bot_sprites_list = arcade.SpriteList()
        
        # Set up each bot sprite
        for i in range(4):
            bot_sprite = Bot(avatar_name, CHARACTER_SCALING)
            bot_sprite.setup(CHARACTER_START_X + bot_sprite.right + 5, 
                             CHARACTER_START_Y[positions[i]], speeds[i])
            self.bot_sprites_list.append(bot_sprite)

        # Name of the layer that has items for foreground
        foreground_layer_name = 'foreground'

        # Name of the layer that has items for background
        background_layer_name = 'background'

        # Name of the layer that has items for touch_this
        touch_this_layer_name = 'touch_this'

        # Map name
        map_name = (mod_path / map_path).resolve()

        # Read in the tiled map
        my_map = arcade.tilemap.read_tmx(map_name)

        # Calculate the right edge of the my_map in pixels
        self.end_of_map = my_map.map_size.width * GRID_PIXEL_SIZE

        # -- Foreground
        self.foreground_sprites_list = arcade.tilemap.process_layer(my_map,
                                                            foreground_layer_name,
                                                            TILE_SCALING)

        # -- Background
        self.background_sprites_list = arcade.tilemap.process_layer(my_map,
                                                            background_layer_name,
                                                            TILE_SCALING)

        # -- Touch_this
        self.touch_this_sprites_list = arcade.tilemap.process_layer(my_map,
                                                            touch_this_layer_name,
                                                            TILE_SCALING)

    def on_show(self):
        arcade.set_background_color(arcade.color.WHITE)                                                       

    def on_draw(self):
        """ Draw everything """                    

        arcade.start_render()
    
        # Draw all sprites
        self.background_sprites_list.draw()
        self.foreground_sprites_list.draw()
        self.touch_this_sprites_list.draw()
        self.player_sprite.draw()
        self.bot_sprites_list.draw()

        # Draw our score on the screen, scrolling it with the viewport
        score_text = f"Score: {self.score}"
        arcade.draw_text(score_text, 10 + self.view_left, 10 + self.view_bottom,
                         arcade.csscolor.BLACK, 18)

        arcade.draw_text(self.player_sprite.name, self.player_sprite.center_x - 30, 
                         self.player_sprite.center_y + 30,  
                         arcade.csscolor.BLACK, 18)

    def on_update(self, delta_time: float):
        """ Movement and game logic """

        # Update characters
        self.player_sprite.on_update(delta_time)
        self.bot_sprites_list.on_update(delta_time)

        # Track if we need to change the viewport
        changed_viewport = False

         # See if the user got to the end of the level
        if self.player_sprite.center_x >= self.end_of_map:
            # Load the next level
            self.setup()

            # Set the camera to the start
            self.view_left = 0
            self.view_bottom = 0
            changed_viewport = True
            self.paused = True

        # Scroll camera to follow player
        self.__scroll_camera(changed_viewport)

    def on_key_press(self, key, _modifier):
        if key == arcade.key.ESCAPE:
            # pass self, the current view, to preserve this view's state
            pause_view = PauseView()
            pause_view.save_state(self)
            self.window.show_view(pause_view)

    def __scroll_camera(self, changed_viewport):
        # Scroll left
        left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left
            changed_viewport = True

        # Scroll right
        right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_VIEWPORT_MARGIN
        if right_boundary <= self.end_of_map - RIGHT_VIEWPORT_MARGIN:
            if self.player_sprite.right > right_boundary:
                self.view_left += self.player_sprite.right - right_boundary
                changed_viewport = True

        if changed_viewport:
            # Only scroll to integers. Otherwise we end up with pixels that
            # don't line up on the screen
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

            # Do the scrolling
            arcade.set_viewport(self.view_left,
                                SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom)