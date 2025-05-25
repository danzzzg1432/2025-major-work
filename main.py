import pygame

from game_constants import *  
from game_logic import *  # Import game logic classes
from ui_elements import *  # Import UI classes
from game_states import *  # Import game states
from save_loads import *  # Import save/load functions



import sys
import time

# Initialise pygame and screen
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
 
try: # Load user data from save file
    if DEBUG_MODE:
        print("\n\n\n (づ｡◕‿‿◕｡)づ DEBUG MODE ACTIVE (づ｡◕‿‿◕｡)づ \n\n\n")
        print("Loaded user data from save file.")
    user = SaveStates.load_user() # creates the currentuser object from saved data
    
    
    """offline generation function"""
    
    print(f"\nTime elapsed when loading user {SaveStates.time_elapsed()}") if DEBUG_MODE else None
    offline_generated_money = user.income_per_second * SaveStates.time_elapsed()
    print(f"\nOffline generated money = ${offline_generated_money} ")
    user.money += offline_generated_money # add money to user
    
    
    
except Exception as e:
    if DEBUG_MODE:
        print(f" (≧ヘ≦ ) Error loading save file: {e} (≧ヘ≦ ) ")
    user = User(STARTING_MONEY) 

''' IDEA FOR BACKGROUND GENERATION:
    when saving, grab current system time
    when loading, grab current system time
    calculate difference in seconds
    multiply by user's generation rate per second
    add to users money
    if difference is greater than 10% of users money, blit a box telling the user how much money they have generated while they were away
    and click anywhere to continue

'''
# Screen set up
state_manager = StateManager(screen, user) # -> creates state manager and accepts the universal user
pygame.display.set_caption(f"Idle Tutor Tycoon - {GAME_TITLE}")
   
if DEBUG_MODE:
    print(state_manager)  # print all registered states
    next_debug = 0
    count = 1


# Main loop
clock = pygame.time.Clock()
while True:
    events = pygame.event.get() # event handling
    current_screen = state_manager.current_state # initial state is main menu for now
    if current_screen:
        current_screen.handle_events(events)
        current_screen.update()
        current_screen.render()
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
