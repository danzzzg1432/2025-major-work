import pygame
from game_constants import *  
from game_classes import *
import sys

# Initialise pygame and screen
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Screen set up
state_manager = StateManager(screen)
pygame.display.set_caption(f"hi")

# debugging stuff
DEBUG_MODE = True  # Set to False in release

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
    # if user input not detected for more than 2 minutes, drop fps down to 15
    else: # if no current screen is found, exit the game, easier debugging
        print("No current screen found, exiting game.")
        pygame.quit()
        sys.exit()
        
    clock.tick(FPS)  # Control game speed
