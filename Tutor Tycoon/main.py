import pygame
from game_constants import *  # Import all constants
from game_classes import *

# Initialise pygame
pygame.init()

# Screen dimensions
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(f"{GAME_TITLE} - Main Menu")

# Importing fonts, none as of right now
font = pygame.font.Font(None, DEFAULT_FONT_SIZE)


# Define buttons based on storyboard layout


# define main menus
main_menu = MainMenu(screen, font)
#  shop_menu = ShopMenu(screen, font)


# Main loop
clock = pygame.time.Clock()

while True:
    events = pygame.event.get() # continuously grab all events
    # main menu screen
    main_menu_event_handler = main_menu.handle_events(events)
    main_menu.update()
    main_menu.render()
    
    clock.tick(FPS)  # Control game speed
