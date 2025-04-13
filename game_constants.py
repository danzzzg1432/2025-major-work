import pygame

pygame.init()

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
SAVE_DIR = "savestates"

# Colours (RGB values)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (150, 150, 150)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# UI settings
DEFAULT_FONT_SIZE = 40
BUTTON_WIDTH = 250
BUTTON_HEIGHT = 60
BUTTON_SPACING = 20
BUTTON_BORDER_RADIUS = 15
main_button_x = (SCREEN_WIDTH - BUTTON_WIDTH) // 2

# Game settings
STARTING_MONEY = 1000
STARTING_LEVEL = 1
STARTING_REPUTATION = 0

# Font Settings
pygame.font.init()
MAIN_MENU_LOGO_SIZE = 90
MAIN_MENU_BUTTON_SIZE = 25
LOGO_FONT = f"{FONTS_DIR}/quicksand_variable.ttf"


# ---------- LOADING STUFF -----------
# Save/load settings
SAVE_FILE_NAME = "save_data.json"

# Game states
MAIN_MENU = "main_menu"
GAME_MENU = "game_menu"
SETTINGS_MENU = "settings_menu"
SHOP_MENU = "shop_menu"
LOGIN_MENU = "login_menu"
REGISTER_MENU = "register_menu"
HELP_MENU = "help_menu"
TESTING = "testing"


# Load Images
def load_image(image_path, scale=None):
    image = pygame.image.load(image_path)
    if scale:
        image = pygame.transform.scale(image, scale)
    return image

williamdu = load_image(f"{IMAGES_DIR}/williamdu.png", (300, 300))
main_menu_background = load_image(f"{IMAGES_DIR}/dr_du_logo.png")
idle_tutor_tycoon_logo = load_image(f"{IMAGES_DIR}/itt_logo.png")