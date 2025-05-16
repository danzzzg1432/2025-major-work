import pygame

pygame.init()

DEBUG_MODE = True

# Screen settings
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 800
GAME_TITLE = "Idle Tutor Tycoon"
FPS = 60

# Defining file paths
ASSETS_DIR = r"assets"
IMAGES_DIR = f"{ASSETS_DIR}/images"
SOUNDS_DIR = f"{ASSETS_DIR}/sounds"
FONTS_DIR = f"{ASSETS_DIR}/fonts"
SAVE_DIR = "savestates/save_data.json"

# Colours (RGB values)
# Colours (RGB values) - organized by color family and brightness

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
BROWN = (165, 42, 42)
DARK_BROWN = (101, 67, 33)

# Grayscale (light to dark)
WHITE = (255, 255, 255)
LIGHT_GRAY = (211, 211, 211)
GRAY = (200, 200, 200)
DARK_GRAY = (150, 150, 150)
BLACK = (0, 0, 0)


# UI settings
DEFAULT_FONT_SIZE = 40
BUTTON_WIDTH = 250
BUTTON_HEIGHT = 60
BUTTON_SPACING = 20
BUTTON_BORDER_RADIUS = 15
main_button_x = (SCREEN_WIDTH - BUTTON_WIDTH) // 2

# Game settings
STARTING_MONEY = 1000

# Font Settings
pygame.font.init()
MAIN_MENU_LOGO_SIZE = 90
MAIN_MENU_BUTTON_SIZE = 25
LOGO_FONT = f"{FONTS_DIR}/quicksand_variable.ttf"


# ---------- LOADING STUFF -----------
# Save/load settings
SAVE_FILE_NAME = "save_data.json"


MAIN_MENU = "main_menu"
GAME_MENU = "game_menu"
# SETTINGS_MENU = "settings_menu"
# SHOP_MENU = "shop_menu"
# LOGIN_MENU = "login_menu"
# REGISTER_MENU = "register_menu"
# HELP_MENU = "help_menu"
TESTING = "testing"
# Game states


# Load Images
def load_image(image_path, scale=None):
    image = pygame.image.load(image_path)
    if scale:
        image = pygame.transform.scale(image, scale)
    return image

williamdu = load_image(f"{IMAGES_DIR}/williamdu.png", (300, 300))
main_menu_background = load_image(f"{IMAGES_DIR}/dr_du_logo.png")
idle_tutor_tycoon_logo = load_image(f"{IMAGES_DIR}/itt_logo.png")

# Generator prototypes
GENERATOR_PROTOTYPES = {
    # id: { name, base_rate (points/sec), base_price (initial cost), growth_rate (cost multiplier) }
    "student":   { "name": "Student", "base_rate": 1,   "base_price": 10, "growth_rate": 1.07 },
    "high_performance_student": { "name": "High Performance Student", "base_rate": 5,   "base_price": 100, "growth_rate": 1.08  },
    "tutor":  { "name": "Professor", "base_rate": 500,  "base_price": 1000, "growth_rate": 1.09 },
    "anandhasundram_parameswaran": { "name": "The Math God Mr Param", "base_rate": 1000, "base_price": 10000, "growth_rate": 1.1 },
    
}

# Manager prototypes
MANAGER_PROTOTYPES = {
    # same keys as GENERATOR_PROTOTYPES 
    "student":  { "name": "Student Leader",  "cost":  100   },
    "high_performance_student":     { "name": "Rank 1 Committee",     "cost":  1000  },
    "tutor": { "name": "Tutor manager", "cost": 10000  },
    "anandhasundram_parameswaran": { "name": "His Kookaburra", "cost": 100000 },
}