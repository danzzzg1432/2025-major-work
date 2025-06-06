import pygame

pygame.init()
pygame.font.init()

DEBUG_MODE = True

# Screen settings
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
GAME_TITLE = "Idle Tutor Tycoon"
FPS = 60

# Defining file paths
ASSETS_DIR = r"assets"
IMAGES_DIR = f"{ASSETS_DIR}/images"
SOUNDS_DIR = f"{ASSETS_DIR}/sounds"
FONTS_DIR = f"{ASSETS_DIR}/fonts"
SOUNDS_DIR = f"{ASSETS_DIR}/sounds"
SAVE_DIR = "savestates/save_data.json"

# Colours (RGB values)

# Blues (light to dark)
LIGHT_BLUE = (173, 216, 230)
SKY_BLUE = (135, 206, 235) 
BLUE = (0, 0, 255)
NAVY = (0, 0, 128)

# Reds/Pinks (light to dark)
LIGHT_PINK = (255, 182, 193)
PINK = (255, 105, 180)
RED = (255, 0, 0)
DARK_RED = (139, 0, 0)

# Greens (light to dark)
LIGHT_GREEN = (144, 238, 144)
GREEN = (0, 255, 0)
FOREST_GREEN = (34, 139, 34)
DARK_GREEN = (0, 100, 0)

# Yellows/Oranges (light to dark)
LIGHT_YELLOW = (255, 255, 224)
YELLOW = (255, 255, 0)
GOLD = (255, 215, 0)
ORANGE = (255, 165, 0)
DARK_ORANGE = (255, 140, 0)

# Purples (light to dark)
LAVENDER = (230, 230, 250)
LIGHT_PURPLE = (218, 112, 214)
PURPLE = (128, 0, 128)
DARK_PURPLE = (75, 0, 130)

# Browns (light to dark)
BEIGE = (245, 245, 220)
TAN = (210, 180, 140)
BROWN = (150, 75, 0)
DARK_BROWN = (101, 67, 33)

# Grayscale (light to dark)
WHITE = (255, 255, 255)
LIGHT_GRAY = (211, 211, 211)
GRAY = (200, 200, 200)
DARK_GRAY = (150, 150, 150)
BLACK = (0, 0, 0)


# UI settings 
DEFAULT_FONT_SIZE = 20
BUTTON_WIDTH = 250
BUTTON_HEIGHT = 60
BUTTON_SPACING = 20
BUTTON_BORDER_RADIUS = 15
main_button_x = (SCREEN_WIDTH - BUTTON_WIDTH) // 2

# Game settings
STARTING_MONEY = 10

# Font Settings
MAIN_MENU_LOGO_SIZE = 90
MAIN_MENU_BUTTON_SIZE = 25
LOGO_FONT = f"{FONTS_DIR}/tabitha.ttf"
DEFAULT_FONT = pygame.font.Font(LOGO_FONT, MAIN_MENU_BUTTON_SIZE)


# ---------- LOADING STUFF -----------
# Save/load settings
SAVE_FILE_NAME = "save_data.json"


MAIN_MENU = "main_menu"
GAME_MENU = "game_menu"
SETTINGS_MENU = "settings_menu"
# LOGIN_MENU = "login_menu"
# REGISTER_MENU = "register_menu"
HELP_MENU = "help_menu"
TESTING = "testing"
# Game states


# Load Images
def load_image(image_path, scale=None):
    image = pygame.image.load(image_path)
    if scale:
        image = pygame.transform.scale(image, scale)
    return image

williamdu = load_image(f"{IMAGES_DIR}/williamdu.png", (165, 165))
main_menu_background = load_image(f"{IMAGES_DIR}/ittmainmenu.png")
idle_tutor_tycoon_logo = load_image(f"{IMAGES_DIR}/itt_logo.png")
game_menu_background = load_image(f"{IMAGES_DIR}/ittgamebackground.png")

# Load UI sounds
BUTTON_PRESS_SOUND = pygame.mixer.Sound(f"{SOUNDS_DIR}/button_press.wav")
BUTTON_PRESS_SOUND.set_volume(0.1)

# Generator prototypes
GENERATOR_PROTOTYPES = {
    # id: { name, base_rate (points/sec), base_price (initial cost), growth_rate (cost multiplier) }
    "g1":   { "name": "5.3 Math Student", "base_rate": 1,   "base_price": 3.738, "growth_rate": 1.07, "base_time": 0.6 },
    "g2": { "name": "4U Student", "base_rate": 60,   "base_price": 60, "growth_rate": 1.15, "base_time": 3.0 },
    "g3":  { "name": "Terry Bong", "base_rate": 720,  "base_price": 540, "growth_rate": 1.14, "base_time": 6.0 },
    "g4": { "name": "Math Messiah, Andy Param", "base_rate": 4320, "base_price": 8640, "growth_rate": 1.13, "base_time": 12.0 },
    "g5": { "name": "Eddie Wu", "base_rate": 51840, "base_price": 103680, "growth_rate": 1.12, "base_time": 24.0 },
    "g6": { "name": "SM", "base_rate": 622080, "base_price": 1244160, "growth_rate": 1.11, "base_time": 96.0},
    "g7": { "name": "Dilliam Wu", "base_rate": 7464960, "base_price": 14929920, "growth_rate": 1.10, "base_time": 384.0},
    "g8": { "name": "buSTATIONARY", "base_rate": 89579520, "base_price": 179159040, "growth_rate": 1.09, "base_time": 1536.0},
    "g9": { "name": "English Advanced", "base_rate": 2149908480, "base_price": 1074954240, "growth_rate": 1.08, "base_time": 6144.0},
    "g0": { "name": "SR 1", "base_rate": 29668737024, "base_price": 25798901760, "growth_rate": 1.07, "base_time": 36864.0},
    
}

# Manager prototypes
MANAGER_PROTOTYPES = {
    # same keys as GENERATOR_PROTOTYPES 
    "g1":  { "name": "Mr Booey",  "cost":  1000   },
    "g2":     { "name": "Question 16",     "cost":  15000  },
    "g3": { "name": "Germanic Baguette Guy", "cost": 100000  },
    "g4": { "name": "Non suspicious kookaburra", "cost": 500000 },
    "g5": { "name": "Wu's Dad", "cost": 1200000 },
    "g6": { "name" :"Hw Copier (not)", "cost": 10000000 },
    "g7": { "name" :"Dames Ju", "cost": 111111111 },
    "g8": { "name" :"Ko", "cost": 555555555 },
    "g9": { "name" :"Useless", "cost": 10000000000 },
    "g0": { "name" :"You", "cost": 100000000000 },
}

GENERATOR_UPGRADES = {
    "g1":   [(25, 2), (50, 4), (100, 8), (200, 16), (300, 32), (400, 64), (500, 128), (600, 256), (700, 512), (800, 1024), (900, 2048), (1000, 4096)],
    "g2": [(25, 2), (50, 4), (100, 8), (200, 16), (300, 32), (400, 64), (500, 128), (600, 256), (700, 512), (800, 1024), (900, 2048), (1000, 4096)],
    "g3": [(25, 2), (50, 4), (100, 8), (200, 16), (300, 32), (400, 64), (500, 128), (600, 256), (700, 512), (800, 1024), (900, 2048), (1000, 4096)],
    "g4": [(25, 2), (50, 4), (100, 8), (200, 16), (300, 32), (400, 64), (500, 128), (600, 256), (700, 512), (800, 1024), (900, 2048), (1000, 4096)],
    "g5": [(25, 2), (50, 4), (100, 8), (200, 16), (300, 32), (400, 64), (500, 128), (600, 256), (700, 512), (800, 1024), (900, 2048), (1000, 4096)],
    "g6": [(25, 2), (50, 4), (100, 8), (200, 16), (300, 32), (400, 64), (500, 128), (600, 256), (700, 512), (800, 1024), (900, 2048), (1000, 4096)],
    "g7": [(25, 2), (50, 4), (100, 8), (200, 16), (300, 32), (400, 64), (500, 128), (600, 256), (700, 512), (800, 1024), (900, 2048), (1000, 4096)],
    "g8": [(25, 2), (50, 4), (100, 8), (200, 16), (300, 32), (400, 64), (500, 128), (600, 256), (700, 512), (800, 1024), (900, 2048), (1000, 4096)],
    "g9": [(25, 2), (50, 4), (100, 8), (200, 16), (300, 32), (400, 64), (500, 128), (600, 256), (700, 512), (800, 1024), (900, 2048), (1000, 4096)],
    "g0": [(25, 2), (50, 4), (100, 8), (200, 16), (300, 32), (400, 64), (500, 128), (600, 256), (700, 512), (800, 1024), (900, 2048), (1000, 4096)],
    "global": [(25, 2), (50, 4), (100, 8), (200, 16), (300, 32), (400, 64), (500, 128), (600, 256), (700, 512), (800, 1024), (900, 2048), (1000, 4096)]
}

# Time-based generation milestones
GENERATOR_TIME_MILESTONES = [25, 50, 100, 200, 300, 400, 600, 1000] # Reduces time for specific generator
GLOBAL_TIME_MILESTONES = [25, 50, 100, 200, 300, 400, 600, 1000]    # Reduces time for ALL generators if all meet count
MIN_GENERATION_TIME = 0.01 # Minimum time a cycle can take after all reductions