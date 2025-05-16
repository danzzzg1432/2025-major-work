import pygame

from game_constants import *  
from game_classes import *

import sys
import time

# Initialise pygame and screen
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

try: # Load user data from save file
    if DEBUG_MODE:
        print("\n\n\n (づ｡◕‿‿◕｡)づ DEBUG MODE ACTIVE (づ｡◕‿‿◕｡)づ \n\n\n")
        print("Loaded user data from save file.")
    user = SaveStates.load_user()
except Exception as e:
    if DEBUG_MODE:
        print(f" (≧ヘ≦ ) Error loading save file: {e}")
    user = User(STARTING_MONEY)

# Screen set up
state_manager = StateManager(screen, user)
pygame.display.set_caption(f"Idle Tutor Tycoon - {GAME_TITLE}")
   
if DEBUG_MODE:
    print(state_manager)  # print all registered states
    next_debug = 0
    count = 1


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
        print("\n\n (≧ヘ≦ ) No current screen found, exiting game. (≧ヘ≦ ) \n\n")
        SaveStates.save_user(user)
        
        pygame.quit()
        sys.exit()
    if DEBUG_MODE:
        now = time.time()
        if now >= next_debug:
            print(f"\n\n (づ｡◕‿‿◕｡)づ #{count} New debug info: \n")
            user.debug_generators()
            next_debug = now + 10
            count += 1
        
    clock.tick(FPS)  # Control game speed
