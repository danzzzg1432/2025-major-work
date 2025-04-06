import pygame
from game_constants import *  
from game_classes import *
import sys

# Initialise pygame
pygame.init()

# Screen set up
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(f"{GAME_TITLE} - Main Menu")


# Initialise game states
state_manager = StateManager()
main_menu = MainMenu(screen, state_manager)
main_game = GameMenu(screen, state_manager)
settings_menu = SettingsMenu(screen, state_manager)
shop_menu = ShopMenu(screen, state_manager)
login_menu = LoginMenu(screen, state_manager)
register_menu = RegisterMenu(screen, state_manager)
help_menu = HelpMenu(screen, state_manager)

# Register game states
state_manager.register_state(MAIN_MENU, main_menu)
state_manager.register_state(GAME_MENU, main_game)
state_manager.register_state(SETTINGS_MENU, settings_menu)
state_manager.register_state(SHOP_MENU, shop_menu)
state_manager.register_state(LOGIN_MENU, login_menu)
state_manager.register_state(REGISTER_MENU, register_menu)
state_manager.register_state(HELP_MENU, help_menu)

# Other classes
test_generator = Generator("Test Generator", 1, 10) # test generator object
me = User("Test User", 0) # test user object


# debugging stuff
DEBUG_MODE = False  # Set to False in release

if DEBUG_MODE:
    print(state_manager)  # print all registered states

# Main loop
clock = pygame.time.Clock()
while True:
    events = pygame.event.get() # event handling
    
    current_screen = state_manager.get_state_object(state_manager.get_state()) # initial state is main menu for now
    if current_screen:
        current_screen.handle_events(events)
        current_screen.update()
        current_screen.render()
    else: # if no current screen is found, exit the game, easier debugging
        print("No current screen found, exiting game.")
        pygame.quit()
        sys.exit()

    # # State manager / Main game loops
    # current_state = state_manager.get_state()
    # if current_state == MAIN_MENU:
    #     main_menu_event_handler = main_menu.handle_events(events)
    #     main_menu.update()
    #     main_menu.render()
    # elif current_state == GAME_MENU:
    #     main_game_event_handler = main_game.handle_events(events)
    #     main_game.update()
    #     main_game.render()

    clock.tick(FPS)  # Control game speed
