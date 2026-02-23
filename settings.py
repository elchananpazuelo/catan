# הגדרות קבועות
TILE_SIZE = 48
GRID_WIDTH, GRID_HEIGHT = 32, 18
WINDOW_SIZE = (16 * TILE_SIZE, 9 * TILE_SIZE)

# צבעים
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
DARK_BG = (20, 20, 20)
FONT_SIZE = 25
FPS = 60

CLICK_SOUND = "sounds/click.wav"

SOUNDS = tile_sounds = {
    "00": "sounds/unreviled",
    "01": "sounds/reviled",
    "02": "sounds/house",
    "03": "sounds/water",
    "04": "sounds/grass",
    "05": "sounds/log",
    "06": "sounds/brick",
    "07": "sounds/iron",
    "08": "sounds/wheat" 
}