# import necessary libraries
import pygame
from game_constants import *  # Import all constants
from game_classes import *

# Initialise pygame
pygame.init()

# Screen dimensions
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(f"{GAME_TITLE} - Main Menu")




# define state
state_manager = StateManager()
main_menu = MainMenu(screen, state_manager)
main_game = MainGame(screen, state_manager)
#  shop_menu = ShopMenu(screen, font)


# Main loop
clock = pygame.time.Clock()

while True:
    events = pygame.event.get() # continuously grab all events

    # handling state manager transitions
    current_state = state_manager.get_state()
    if current_state == MAIN_MENU:
        main_menu_event_handler = main_menu.handle_events(events)
        main_menu.update()
        main_menu.render()
    elif current_state == GAME_RUNNING:
        main_game_event_handler = main_game.handle_events(events)
        main_game.update()
        main_game.render()

    clock.tick(FPS)  # Control game speed
