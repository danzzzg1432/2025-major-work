import pygame

from game_constants import *  # Import game constants
from game_logic import *  # Import game logic classes
from ui_elements import *  # Import UI classes
from game_states import *  # Import game states
from save_loads import *  # Import save/load functions
from utils import Music, simulate_offline_progress 

# Import sys and time
import sys 
import time

# Initialise PyGame, sound control and screen
pygame.init()
pygame.mixer.init()


try:
    if DEBUG_MODE:
        print("\n\n\n (づ｡◕‿‿◕｡)づ DEBUG MODE ACTIVE (づ｡◕‿‿◕｡)づ \n\n\n")
    user = SaveStates.load_user() # creates the current user object from saved data
except Exception as e:
        print("\n\n (≧ヘ≦ ) Error loading save file, creating new user. (≧ヘ≦ ) \n\n") if DEBUG_MODE else None
        print(Exception, e) if DEBUG_MODE else None
        if DEBUG_MODE:
            print(f" (≧ヘ≦ ) Error loading save file: {e} (≧ヘ≦ ) ")
        user = User(STARTING_MONEY) 
simulate_offline_progress(user)
try:
    print("\n\n (づ｡◕‿‿◕｡)づ Loading music... (づ｡◕‿‿◕｡)づ") if DEBUG_MODE else None
    music_player = SaveStates.load_music() # creates the current music object from saved data
    
except Exception as e:
    print("\n\n (≧ヘ≦ ) Error loading music, creating new music player. (≧ヘ≦ ) \n\n") if DEBUG_MODE else None
    print(Exception, e) if DEBUG_MODE else None
    music_player = Music(0.50) 

# Screen set up
state_manager = StateManager(screen, user, music_player) # Pass music_player
pygame.display.set_caption(f"Idle Tutor Tycoon - {GAME_TITLE}")
   
# Initialise debug variables
next_debug = 0 
count = 1

# Main loop
clock = pygame.time.Clock() # initialise clock 
last_time = pygame.time.get_ticks() / 1000
while True:
    events = pygame.event.get() 
    current_state = state_manager.current_state 
    try:
        now = pygame.time.get_ticks() / 1000 # moved this into main loop to ensure it updates every frame no matter what screen
        dt = now - last_time
        last_time = now
        user.update(dt)  
        
        current_state.handle_events(events) # type: ignore
        current_state.update() # type: ignore
        current_state.render() # type: ignore
    except Exception as e:
        print(e) if DEBUG_MODE else None
        print(f"\n\n(≧ヘ≦ ) No current screen found, exiting game. (≧ヘ≦ ) ") if DEBUG_MODE else None
        SaveStates.save_all(user, music_player)
        pygame.quit()
        sys.exit()

    music_player.update() # update music player

    if DEBUG_MODE:
        now = time.time()
        if now >= next_debug:
            print(f"\n\n (づ｡◕‿‿◕｡)づ #{count} New debug info: \n")
            user.debug_generators()
            next_debug = now + 10 # Use the initialised next_debug
            count += 1            # Use the initialised count
        
    clock.tick(FPS)
