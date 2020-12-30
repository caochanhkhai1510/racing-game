# Constants used to initialize window
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = 'Platformer'

# Constants used to scale our sprites from their original size
TILE_SCALING = (float)(SCREEN_HEIGHT / 1152)
CHARACTER_SCALING = 0.1 * TILE_SCALING
SPRITE_PIXEL_SIZE = 16
GRID_PIXEL_SIZE = (SPRITE_PIXEL_SIZE * TILE_SCALING)

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
LEFT_VIEWPORT_MARGIN = 0
RIGHT_VIEWPORT_MARGIN = SCREEN_WIDTH / 2

# Character starting positions
CHARACTER_START_X = 0
CHARACTER_START_Y = [125, 245, 365, 485, 605]