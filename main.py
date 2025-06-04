import pygame

from game_constants import *  
from game_logic import *  # Import game logic classes
from ui_elements import *  # Import UI classes
from game_states import *  # Import game states
from save_loads import *  # Import save/load functions

import sys
import time

# Initialise pygame, sound control and screen
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


try: # Load user data from save file
    if DEBUG_MODE:
        print("\n\n\n (づ｡◕‿‿◕｡)づ DEBUG MODE ACTIVE (づ｡◕‿‿◕｡)づ \n\n\n")
        print("Loaded user data from save file.")
    user = SaveStates.load_user() # creates the currentuser object from saved data
    
    time_elapsed_offline = SaveStates.time_elapsed()
    print(f"\nTime elapsed when loading user {time_elapsed_offline}") if DEBUG_MODE else None
    
    # First, give a lump sum based on the income_per_second at the moment of saving.
    # This is a quick approximation.
    offline_generated_money_estimate = user.income_per_second * time_elapsed_offline 
    user.money += offline_generated_money_estimate
    print(f"\nOffline generated money (estimated based on saved income/sec) = ${offline_generated_money_estimate} ") if DEBUG_MODE else None

    # More accurate offline progress: Simulate cycles for each generator.
    # This will add any additional money from completed cycles not covered by the estimate.
    # Note: The previous estimate might slightly overpay if income_per_second decreased due to milestone changes during offline time, 
    # but this simulation correctly processes cycles based on their state when saved.
    for gen_id, gen in user.generators.items():
        if gen.amount > 0 and (gen.is_generating or gen.id in user.managers):
            remaining_offline_time_for_gen = time_elapsed_offline
            effective_time_for_cycle = gen.get_effective_time(user.generators)

            if gen.is_generating: # Cycle was in progress
                if gen.time_progress <= remaining_offline_time_for_gen:
                    user.money += gen.cycle_output # Add money for this completed cycle
                    remaining_offline_time_for_gen -= gen.time_progress
                    gen.is_generating = False
                else:
                    gen.time_progress -= remaining_offline_time_for_gen
                    remaining_offline_time_for_gen = 0
            
            # If managed, or if a cycle just finished, and there's time left, run subsequent cycles
            if (gen.id in user.managers or not gen.is_generating) and remaining_offline_time_for_gen > 0:
                if not gen.is_generating and gen.id in user.managers: # Start new cycle if managed and idle
                     gen.start_generation_cycle(user.generators)
                
                if gen.is_generating: # Check if it started or was already running and finished
                    num_full_cycles_offline = int(remaining_offline_time_for_gen // effective_time_for_cycle)
                    if num_full_cycles_offline > 0:
                        user.money += gen.cycle_output * num_full_cycles_offline
                        remaining_offline_time_for_gen -= num_full_cycles_offline * effective_time_for_cycle
                    
                    # Update progress of the current (potentially new) cycle
                    if remaining_offline_time_for_gen > 0:
                        gen.time_progress -= remaining_offline_time_for_gen
                    else: # All time used up by full cycles
                        gen.is_generating = False # Reset if it perfectly finished
                        if gen.id in user.managers: # And restart if managed
                            gen.start_generation_cycle(user.generators)

except Exception as e:
    print("\n\n (≧ヘ≦ ) Error loading save file, creating new user. (≧ヘ≦ ) \n\n") if DEBUG_MODE else None
    print(Exception, e) if DEBUG_MODE else None
    if DEBUG_MODE:
        print(f" (≧ヘ≦ ) Error loading save file: {e} (≧ヘ≦ ) ")
    user = User(STARTING_MONEY) 

# Screen set up
state_manager = StateManager(screen, user)
pygame.display.set_caption(f"Idle Tutor Tycoon - {GAME_TITLE}")
   
# Initialise debug variables
next_debug = 0 
count = 1

# Start background music
BACKGROUND_MUSIC.play(loops=-1)
BACKGROUND_MUSIC.set_volume(0.05)
# Main loop
clock = pygame.time.Clock()
while True:
    events = pygame.event.get() 
    current_screen = state_manager.current_state 
    if current_screen:
        current_screen.handle_events(events)
        current_screen.update()
        current_screen.render()
    else: 
        print("\n\n (≧ヘ≦ ) No current screen found, exiting game. (≧ヘ≦ ) \n\n")
        SaveStates.save_user(user)
        pygame.quit()
        sys.exit()

    if DEBUG_MODE:
        now = time.time()
        if now >= next_debug:
            print(f"\n\n (づ｡◕‿‿◕｡)づ #{count} New debug info: \n")
            user.debug_generators()
            next_debug = now + 10 # Use the initialised next_debug
            count += 1            # Use the initialised count
        
    clock.tick(FPS)
