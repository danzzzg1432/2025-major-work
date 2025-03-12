import pygame

# Screen settings
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 800
GAME_TITLE = "Idle Tutor Tycoon"
FPS = 30

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

# Game settings
STARTING_MONEY = 1000
STARTING_LEVEL = 1
STARTING_REPUTATION = 0

# File paths
ASSETS_DIR = r"Tutor Tycoon/assets"
IMAGES_DIR = f"{ASSETS_DIR}/images"
SOUNDS_DIR = f"{ASSETS_DIR}/sounds"
SAVE_DIR = "savestates"

# Save/load settings
SAVE_FILE_NAME = "save_data.json"

# Game states
MAIN_MENU = "main_menu"
GAME_RUNNING = "game_running"
SETTINGS_MENU = "settings_menu"
SHOP_MENU = "shop_menu"

# Font Settings
MAIN_MENU_LOGO_SIZE = 60

# Main Menu stuff
background = pygame.image.load(f"{IMAGES_DIR}/dr_du_logo.png")