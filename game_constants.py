import pygame
import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller bundling purposes """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS # type: ignore 
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

pygame.init()
pygame.font.init()


DEBUG_MODE = False

# Screen settings
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
GAME_TITLE = "Idle Tutor Tycoon"
FPS = 60
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Defining file paths
ASSETS_DIR = "assets"
IMAGES_DIR = f"{ASSETS_DIR}/images"
SOUNDS_DIR = f"{ASSETS_DIR}/sounds"
FONTS_DIR = f"{ASSETS_DIR}/fonts"
SAVE_DIR = "savestates/save_data.json"

# Colours (RGB values)

# Blues (light to dark)
LIGHT_BLUE = (173, 216, 230)
SKY_BLUE = (135, 206, 235) 
BLUE = (0, 0, 255)
NAVY = (0, 0, 128)
ALICEBLUE = (240, 248, 255)

# Reds/Pinks (light to dark)
LIGHT_PINK = (255, 182, 193)
PINK = (255, 105, 180)
RED = (255, 0, 0)
DARK_RED = (139, 0, 0)
FOLLY = (255, 56, 100)

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
BEIGE = (220, 205, 185)
TAN = (251, 222, 160)
BROWN = (150, 75, 0)
DARK_BROWN = (101, 67, 33)

# Grayscale (light to dark)
WHITE = (255, 255, 255)
LIGHT_GRAY = (211, 211, 211)
GRAY = (200, 200, 200)
DARK_GRAY = (150, 150, 150)
BLACK = (0, 0, 0)

# OTHER MORE SPECIFIC COLOURS
BUTTON_UNPRESSED_COLOUR = (38,114,153)
BUTTON_PRESSED_COLOUR = (28,84,123)
BUTTON_SHADOW_COLOUR = (19,47,66)
BUTTON_HOVER_COLOUR = (28,84,123)

# UI settings 
DEFAULT_FONT_SIZE = 20
BUTTON_WIDTH = 250
BUTTON_HEIGHT = 60
BUTTON_SPACING = 20
BUTTON_BORDER_RADIUS = 15
main_button_x = (SCREEN_WIDTH - BUTTON_WIDTH) // 2

# Game settings
STARTING_MONEY = 5

# Font Settings
MAIN_MENU_LOGO_SIZE = 90
MAIN_MENU_BUTTON_SIZE = 25
LOGO_FONT = resource_path(f"{FONTS_DIR}/tabitha.ttf")
DEFAULT_FONT = pygame.font.Font(LOGO_FONT, MAIN_MENU_BUTTON_SIZE)


# ---------- LOADING STUFF -----------
# Save/load filepath
SAVE_FILE_NAME = "save_data.json"

# Game States
MAIN_MENU = "main_menu"
GAME_MENU = "game_menu"
SETTINGS_MENU = "settings_menu"
# LOGIN_MENU = "login_menu"
# REGISTER_MENU = "register_menu"
HELP_MENU = "help_menu"
HELP_DETAIL_MENU = "help_detail_menu"
TESTING = "testing"


# Load Images
def load_image(relative_image_path, scale=None):
    image = pygame.image.load(resource_path(relative_image_path)).convert_alpha()
    if scale:
        image = pygame.transform.scale(image, scale)
    return image

williamdu = load_image("assets/images/williamdu.png", (165, 165))
main_menu_background = load_image("assets/images/ittmainmenu.png")
idle_tutor_tycoon_logo = load_image("assets/images/itt_logo.png")
game_menu_background = load_image("assets/images/ittgamebackground.png")
settings_icon = load_image("assets/images/settings_icon.png", (50, 50))
help_icon = load_image("assets/images/help_icon.png", (50, 50))
exit_icon = load_image("assets/images/exit_icon.png", (50, 50))
tutorial_arrow = load_image("assets/images/tutorial_arrow.png", (100, 100))

# Load UI sounds
BUTTON_PRESS_SOUND = pygame.mixer.Sound(resource_path("assets/sounds/button_press.wav"))
BUTTON_PRESS_SOUND.set_volume(0.3)

# Generator prototypes
GENERATOR_PROTOTYPES = {
    # id: { name, base_rate (points/sec), base_price (initial cost), growth_rate (cost multiplier), base_time (time to complete cycle) }
    "g1":   { "name": "5.3 Math Student", "base_rate": 1,   "base_price": 3.738, "growth_rate": 1.07, "base_time": 0.6 },
    "g2": { "name": "Victor", "base_rate": 60,   "base_price": 60, "growth_rate": 1.15, "base_time": 3.0 },
    "g3":  { "name": "Terry Bong", "base_rate": 720,  "base_price": 540, "growth_rate": 1.14, "base_time": 6.0 },
    "g4": { "name": "Math Messiah, Andy Param", "base_rate": 4320, "base_price": 8640, "growth_rate": 1.13, "base_time": 12.0 },
    "g5": { "name": "Eddie Wu", "base_rate": 51840, "base_price": 103680, "growth_rate": 1.12, "base_time": 24.0 },
    "g6": { "name": "SM", "base_rate": 622080, "base_price": 1244160, "growth_rate": 1.11, "base_time": 96.0},
    "g7": { "name": "Dilliam Wu", "base_rate": 7464960, "base_price": 14929920, "growth_rate": 1.10, "base_time": 384.0},
    "g8": { "name": "Ko", "base_rate": 89579520, "base_price": 179159040, "growth_rate": 1.09, "base_time": 1536.0},
    "g9": { "name": "English Advanced", "base_rate": 2149908480, "base_price": 1074954240, "growth_rate": 1.08, "base_time": 6144.0},
    "g0": { "name": "SR 1", "base_rate": 29668737024, "base_price": 25798901760, "growth_rate": 1.07, "base_time": 36864.0},
    
}

# Manager prototypes
MANAGER_PROTOTYPES = {
    # same keys as GENERATOR_PROTOTYPES 
    "g1": { "name": "Mr Booey",  "cost":  1000   },
    "g2": { "name": "Teaches Math",     "cost":  15000  },
    "g3": { "name": "Germanic Baguette Guy", "cost": 100000  },
    "g4": { "name": "Non suspicious kookaburra", "cost": 500000 },
    "g5": { "name": "Wu's Dad", "cost": 1200000 },
    "g6": { "name" :"Hw Copier (not)", "cost": 10000000 },
    "g7": { "name" :"Dames Ju", "cost": 111111111 },
    "g8": { "name" :"buStationary", "cost": 555555555 },
    "g9": { "name" :"Useless", "cost": 10000000000 },
    "g0": { "name" :"You", "cost": 100000000000 },
}

GENERATOR_UPGRADES = {
    "g1":   [(25, 2), (50, 4), (100, 8), (200, 16), (300, 32), (400, 64), (500, 256), (600, 256), (700, 1024), (800, 4096), (900, 16384), (1000, 81920), (1100, 327680), (1200, 1310720), (1300, 5242880), (1400, 20971520), (1500, 83886080), (1600, 335544320), (1700, 1342177280), (1800, 5368709120), (1900, 21474836480), (2000, 85899345920)],
    "g2": [(25, 2), (50, 4), (100, 8), (200, 16), (300, 32), (400, 64), (500, 256), (600, 256), (700, 1024), (800, 4096), (900, 16384), (1000, 81920), (1100, 327680), (1200, 1310720), (1300, 5242880), (1400, 20971520), (1500, 83886080), (1600, 335544320), (1700, 1342177280), (1800, 5368709120), (1900, 21474836480), (2000, 85899345920)],
    "g3": [(25, 2), (50, 4), (100, 8), (200, 16), (300, 32), (400, 64), (500, 256), (600, 256), (700, 1024), (800, 4096), (900, 16384), (1000, 81920), (1100, 327680), (1200, 1310720), (1300, 5242880), (1400, 20971520), (1500, 83886080), (1600, 335544320), (1700, 1342177280), (1800, 5368709120), (1900, 21474836480), (2000, 85899345920)],
    "g4": [(25, 2), (50, 4), (100, 8), (200, 16), (300, 32), (400, 64), (500, 256), (600, 256), (700, 1024), (800, 4096), (900, 16384), (1000, 81920), (1100, 327680), (1200, 1310720), (1300, 5242880), (1400, 20971520), (1500, 83886080), (1600, 335544320), (1700, 1342177280), (1800, 5368709120), (1900, 21474836480), (2000, 85899345920)],
    "g5": [(25, 2), (50, 4), (100, 8), (200, 16), (300, 32), (400, 64), (500, 256), (600, 256), (700, 1024), (800, 4096), (900, 16384), (1000, 81920), (1100, 327680), (1200, 1310720), (1300, 5242880), (1400, 20971520), (1500, 83886080), (1600, 335544320), (1700, 1342177280), (1800, 5368709120), (1900, 21474836480), (2000, 85899345920)],
    "g6": [(25, 2), (50, 4), (100, 8), (200, 16), (300, 32), (400, 64), (500, 256), (600, 256), (700, 1024), (800, 4096), (900, 16384), (1000, 81920), (1100, 327680), (1200, 1310720), (1300, 5242880), (1400, 20971520), (1500, 83886080), (1600, 335544320), (1700, 1342177280), (1800, 5368709120), (1900, 21474836480), (2000, 85899345920)],
    "g7": [(25, 2), (50, 4), (100, 8), (200, 16), (300, 32), (400, 64), (500, 256), (600, 256), (700, 1024), (800, 4096), (900, 16384), (1000, 81920), (1100, 327680), (1200, 1310720), (1300, 5242880), (1400, 20971520), (1500, 83886080), (1600, 335544320), (1700, 1342177280), (1800, 5368709120), (1900, 21474836480), (2000, 85899345920)],
    "g8": [(25, 2), (50, 4), (100, 8), (200, 16), (300, 32), (400, 64), (500, 256), (600, 256), (700, 1024), (800, 4096), (900, 16384), (1000, 81920), (1100, 327680), (1200, 1310720), (1300, 5242880), (1400, 20971520), (1500, 83886080), (1600, 335544320), (1700, 1342177280), (1800, 5368709120), (1900, 21474836480), (2000, 85899345920)],
    "g9": [(25, 2), (50, 4), (100, 8), (200, 16), (300, 32), (400, 64), (500, 256), (600, 256), (700, 1024), (800, 4096), (900, 16384), (1000, 81920), (1100, 327680), (1200, 1310720), (1300, 5242880), (1400, 20971520), (1500, 83886080), (1600, 335544320), (1700, 1342177280), (1800, 5368709120), (1900, 21474836480), (2000, 85899345920)],
    "g0": [(25, 2), (50, 4), (100, 8), (200, 16), (300, 32), (400, 64), (500, 256), (600, 256), (700, 1024), (800, 4096), (900, 16384), (1000, 81920), (1100, 327680), (1200, 1310720), (1300, 5242880), (1400, 20971520), (1500, 83886080), (1600, 335544320), (1700, 1342177280), (1800, 5368709120), (1900, 21474836480), (2000, 85899345920)],
    "global": [(25, 2), (50, 4), (100, 8), (200, 16), (300, 32), (400, 64), (500, 256), (600, 256), (700, 1024), (800, 4096), (900, 16384), (1000, 81920), (1100, 327680), (1200, 1310720), (1300, 5242880), (1400, 20971520), (1500, 83886080), (1600, 335544320), (1700, 1342177280), (1800, 5368709120), (1900, 21474836480), (2000, 85899345920)]
}

# Time-based generation milestones
GENERATOR_TIME_MILESTONES = [25, 50, 100, 200, 300, 400, 500, 600, 1000] # Reduces time for specific generator
GLOBAL_TIME_MILESTONES = [25, 50, 100, 200, 300, 400, 500, 600, 1000, 1200, 1600, 2000]    # Reduces time for ALL generators if all meet count
MIN_GENERATION_TIME = 0.01 # Minimum time a cycle can take after all reductions

# Revenue multiplier upgrades (from the upgrades panel)
REVENUE_MULTIPLIER_BASE_PRICES = {
    "g1": 1000000,
    "g2": 2500000,
    "g3": 5000000,
    "g4": 10000000,
    "g5": 25000000,
    "g6": 50000000,
    "g7": 100000000,
    "g8": 250000000,
    "g9": 500000000,
    "g0": 1000000000,
}
REVENUE_MULTIPLIER_GROWTH_FACTOR = 2500
