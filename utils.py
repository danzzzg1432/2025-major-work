from game_constants import *
from game_logic import User
from ui_elements import CreateFrect
import os
import random
import pygame

def format_large_number(num):  
    """
    The game has numbers in the vigintillions - aka 102 zeros (though reaching those values may take years, millions of years...). 
    Trying to display that on the screen is a bit too much,
    so this is a function that summarises the number.
    """
    if num < 1000:
        return str(int(num)) # if the number is less than 1000, return it as an integer as no change is needed
    
    magnitude = 0 # initialise the magnitude of the number
    while abs(num) >= 1000: 
        magnitude += 1 
        num /= 1000.0 # divide by 1000 to get the next major magnitude (thousands, millions, billions, etc.)
    
    # Format with 3 decimal places and remove trailing zeros
    formatted_num = f"{num:.3f}".rstrip('0').rstrip('.')
    
    # Return formatted number with appropriate suffix
    suffixes = [
            "",    "K",   "M",   "B",   "T",    "Qa",   "Qi",   "Sx",   "Sp",   "Oc",   # 10^0…10^27
            "No",  "Dc",  "Ud",  "Dd",  "Td",   "Qad",  "Qid",  "Sxd",  "Spd",  "Ocd",  # 10^30…10^57
            "Nod", "Vg",  "Vd",  "Tg",  "Qag",  "Qig",  "Sxg",  "Spg",  "Uvg",  "Dvg",  # 10^60…10^87
            "Tvg", "Qavg","Qivg","Sxvg","Spvg"                                            # 10^90…10^102
           ]
    
    if magnitude < len(suffixes):
        return f"{formatted_num} {suffixes[magnitude]}" # if the number has a pretty suffix, return it with the suffix
    else:
        return f"{formatted_num}e{magnitude*3}" # if the number is too large, return it in scientific notation
 
def simulate_offline_progress(user): # simulate offline progress for the user
    """
    Simulates the progress of the user's generators when the game is offline.
    """
    from save_loads import SaveStates
    try: # Load user data from save file
        
        time_elapsed_offline = SaveStates.time_elapsed()
        print(f"\nTime elapsed when offline:  {time_elapsed_offline}s") if DEBUG_MODE else None
        lets_see = 0
        for gen_id, gen in user.generators.items():
            if gen.amount > 0 and (gen.is_generating or gen.id in user.managers): # if the generator is owned and is generating or has a manager
                remaining_offline_time_for_gen = time_elapsed_offline # the time elapsed since the last save
                effective_time_for_cycle = gen.get_effective_time(user.generators) # the effective time for a cycle

                if gen.is_generating: # Cycle was in progress
                    if gen.time_progress <= remaining_offline_time_for_gen: # if the cycle was in progress and the time elapsed is greater than the time progress
                        user.money += gen.cycle_output # Add money for this completed cycle
                        lets_see += gen.cycle_output # for debugging
                        remaining_offline_time_for_gen -= gen.time_progress # subtract the time progress from the remaining time
                        gen.is_generating = False # reset the generating state
                    else:
                        gen.time_progress -= remaining_offline_time_for_gen # subtract the remaining time from the time progress
                        remaining_offline_time_for_gen = 0 # reset the remaining time
                
                # If managed, or if a cycle just finished, and there's time left, run subsequent cycles
                if (gen.id in user.managers or not gen.is_generating) and remaining_offline_time_for_gen > 0: # if the generator is managed or not generating and there is time left
                    if not gen.is_generating and gen.id in user.managers: # if the generator is not generating and is managed
                        gen.start_generation_cycle(user.generators) # start a new cycle
                    
                    if gen.is_generating: # if the generator is generating
                        num_full_cycles_offline = int(remaining_offline_time_for_gen // effective_time_for_cycle) # the number of full cycles that can be completed
                        if num_full_cycles_offline > 0: # if there are full cycles
                            user.money += gen.cycle_output * num_full_cycles_offline # add money for the full cycles
                            lets_see += gen.cycle_output * num_full_cycles_offline # for debugging
                            remaining_offline_time_for_gen -= num_full_cycles_offline * effective_time_for_cycle # subtract the effective time for the full cycles from the remaining time
                        
                        # Update progress of the current (potentially new) cycle
                        if remaining_offline_time_for_gen > 0: # if there is time left
                            gen.time_progress -= remaining_offline_time_for_gen # subtract the remaining time from the time progress
                        else: # if all time used up by full cycles
                            gen.is_generating = False # reset the generating state
                            if gen.id in user.managers: # if the generator is managed   
                                gen.start_generation_cycle(user.generators) # restart the cycle
        print(f"\nOffline progress added: ${lets_see}") if DEBUG_MODE else None

    except Exception as e:
        print(f"\n\n (≧ヘ≦ ) Error simulating offline progress: {e} (≧ヘ≦ ) \n\n") if DEBUG_MODE else None
        
class Music:
    """
    Music playback with volume, shuffling, playback controls and other stuff
    """
    def __init__(self, volume=0.05, start_playing=True):
        self.playlist = self.load_playlist()
        self.current_song_index = 0
        self.volume = volume
        pygame.mixer.music.set_volume(self.volume)  # Set initial volume
        self.is_paused = False # Track pause state

        if self.playlist:
            random.shuffle(self.playlist)
            if start_playing:
                self.play_current_song()
        else:
            if DEBUG_MODE:
                print("Warning: No music files found in assets/sounds or directory missing.")

    def load_playlist(self):
        """
        Loads music files from the specified music directory
        """
        music_dir = resource_path(os.path.join(ASSETS_DIR, "sounds"))
        supported_formats = ('.mp3') # Add other supported formats if needed
        playlist_files = []
        try:
            for f_name in os.listdir(music_dir):
                if f_name.lower().endswith(supported_formats):
                    playlist_files.append(os.path.join(music_dir, f_name))
        except FileNotFoundError:
            if DEBUG_MODE:
                print(f"Music directory not found: {music_dir}")
            return []
        
        if not playlist_files and DEBUG_MODE:
            print(f"No music files with supported formats found in {music_dir}")
            
        return playlist_files

    def play_current_song(self):
        try:
            pygame.mixer.music.load(self.playlist[self.current_song_index])
            pygame.mixer.music.play(loops=0)  # Play once; update() will handle the next song
            self.is_paused = False # Reset pause state when a new song plays
            print(f"Playing {self.playlist[self.current_song_index]}") if DEBUG_MODE else None
        except pygame.error as e:
            if DEBUG_MODE:
                print(f"Error loading/playing music {self.playlist[self.current_song_index]}: {e}")

    def update(self):
        if not pygame.mixer.music.get_busy() and not self.is_paused:
            self.current_song_index += 1 # increment the current song index to avoid playing the same song twice (when choosing a random song)
            if self.current_song_index >= len(self.playlist):
                self.current_song_index = 0
                random.shuffle(self.playlist)  # Reshuffle when the playlist completes
            self.play_current_song()

    def set_volume(self, volume_level):
        self.volume = max(0.0, min(1.0, volume_level))
        pygame.mixer.music.set_volume(self.volume)

    def get_current_volume(self): # Added to get current volume for display
        return self.volume

    def play(self):
        if not pygame.mixer.music.get_busy(): # Not playing
            self.play_current_song()
        elif self.is_paused: # if paused, unpause
            pygame.mixer.music.unpause()
            self.is_paused = False

    def pause(self):
        if pygame.mixer.music.get_busy() and not self.is_paused:
            pygame.mixer.music.pause()
            self.is_paused = True

    def toggle_pause(self): # Added to toggle play/pause
        if self.is_paused:
            self.play() # unpauses
        else:
            self.pause()

    def skip_song(self): # Added to skip to the next song
        self.current_song_index = (self.current_song_index + 1) % len(self.playlist)
        self.play_current_song()

    def rewind_song(self): # Added to go to the previous song or restart current
        if pygame.mixer.music.get_pos() > 3000: # more than 3 seconds played
            self.play_current_song() # Restart current song
        else:
            self.current_song_index = (self.current_song_index - 1 + len(self.playlist)) % len(self.playlist)
            self.play_current_song()

    def get_current_song_display_name(self): # Added to get a displayable song name
        full_path = self.playlist[self.current_song_index]
        file_name = os.path.basename(full_path)
        name_without_extension, _ = os.path.splitext(file_name)
        return name_without_extension.replace("_", " ").title() # Basic formatting

    def stop(self):
        pygame.mixer.music.stop()
        self.is_paused = False # Reset pause state
        
    def to_dict(self):
        return {
            "volume": self.volume,
            "is_paused": self.is_paused,
        }
    
    @classmethod
    def from_dict(cls, data):
        instance = cls(volume=data.get("volume", 0.50), start_playing=False)
        instance.is_paused = data.get("is_paused", False)

        if instance.playlist:
            if not instance.is_paused:
                instance.play_current_song()
            else:
                # If paused, just load the song so it's ready to play
                try:
                    pygame.mixer.music.load(instance.playlist[instance.current_song_index])
                except pygame.error as e:
                    if DEBUG_MODE:
                        print(f"Error loading music {instance.playlist[instance.current_song_index]}: {e}")
        return instance


def tutorial_progress(user, screen, game_menu):
    """
    Handles the display of contextual tutorial hints to guide new players.

    This function checks the user's tutorial progress state and displays arrows
    and text to point them towards the next key action, such as buying their
    first generator, generating manually, hiring a manager, or purchasing an upgrade.
    
    """
    def draw_tutorial_hint(screen, target_rect, text, arrow_pos='left'):
        """
        Draws a tutorial arrow and text hint pointing to a specific UI element.
        This is a helper function to keep the main tutorial logic cleaner.
        """
        arrow_img = tutorial_arrow # the arrow image
        text_font = pygame.font.Font(LOGO_FONT, 22) 
        text_surf_temp = text_font.render(text, True, WHITE) # render the text
        text_rect_temp = text_surf_temp.get_rect() # get the rectangle of the text

        hint_frect = CreateFrect(
            x=0, y=0, width=text_rect_temp.width + 40,
            height=text_rect_temp.height + 40, 
            bg_colour=BLACK,
            font=text_font,
            font_colour=WHITE,
            display=text
            )
        hint_frect.shadow_colour = None # no shadow for tutorial hints

        # base arrow points right '->'
        if arrow_pos == 'right':
            # needs to point left '<-'
            arrow_img = pygame.transform.flip(arrow_img, True, False)
        elif arrow_pos == 'top':
            # needs to point down 'v'
            arrow_img = pygame.transform.rotate(arrow_img, -90)
        elif arrow_pos == 'bottom':
            # needs to point up '^'
            arrow_img = pygame.transform.rotate(arrow_img, 90)

        arrow_rect = arrow_img.get_rect() # get the rectangle of the arrow

            # position hint and arrow
        if arrow_pos == 'left': # if the arrow is pointing left
            arrow_rect.right = target_rect.left - 10
            arrow_rect.centery = target_rect.centery
            hint_frect.frect.right = arrow_rect.left - 10
            hint_frect.frect.centery = arrow_rect.centery
        elif arrow_pos == 'right': # if the arrow is pointing right
            arrow_rect.left = target_rect.right + 10
            arrow_rect.centery = target_rect.centery
            hint_frect.frect.left = arrow_rect.right + 10
            hint_frect.frect.centery = arrow_rect.centery
        
        hint_frect.draw(screen)
        screen.blit(arrow_img, arrow_rect)


    # Stage 1: Guide the player to buy their first generator.
    if not user.tutorial_state.get('first_generator'):
        first_gen_proto = GENERATOR_PROTOTYPES['g1']
        if user.money >= first_gen_proto['base_price'] and len(game_menu.rows) > 0:
            if game_menu.active_panel is None:
                first_gen_row = game_menu.rows[0]
                buy_button_rect = first_gen_row['buy'].rect
                # The first generator is on the left side, so point from the right.
                draw_tutorial_hint(screen, buy_button_rect, "Buy, and keep buying your first generator!", 'right')
        return

    # Stage 1.5: After buying the first generator, teach manual generation and tell them to keep buying generators and keep clicking
    if user.tutorial_state.get('first_generator') and not user.tutorial_state.get('first_manual_generation'):
        if game_menu.active_panel is None: # 
            first_gen_row = game_menu.rows[0]
            icon_rect = first_gen_row['icon'].frect
            draw_tutorial_hint(screen, icon_rect, "Keep on clicking on me to generate!", 'right')
        return

    # Stage 2: Once manual generation is understood, introduce managers for automation.
    if user.tutorial_state.get('first_manual_generation') and not user.tutorial_state.get('first_manager'):
        first_manager_proto = MANAGER_PROTOTYPES['g1']
        # Check if the first generator is owned and the player can afford the manager.
        if 'g1' in user.generators and user.generators['g1'].amount > 0 and user.money >= first_manager_proto['cost']:
            if game_menu.active_panel != 'shop':
                # If not in the shop, point to the 'Managers' navigation button.
                manager_button = game_menu.nav_buttons[0] # 'Managers' button
                draw_tutorial_hint(screen, manager_button.rect, "Automatically generate with a manager!", 'right')
            else:
                # If in the shop, point to the buy button for the first manager.
                first_manager_row = game_menu.shop_rows[0]
                buy_button_rect = first_manager_row['btn'].rect
                draw_tutorial_hint(screen, buy_button_rect, "Buy me! I will click for you!", 'left')
        return
    
    # Stage 2.5: Introduce the help menu
    if not user.tutorial_state.get('help_menu_opened'):
        if user.tutorial_state.get('first_manager'):
            if game_menu.active_panel is None: 
                help_menu_btn_rect = game_menu.nav_buttons[3]
                draw_tutorial_hint(screen, help_menu_btn_rect.rect, "Click here if you need help!", "right")
        return   

    # Stage 3: After the first manager, introduce upgrades to boost income.
    if not user.tutorial_state.get('first_upgrade'):
        if 'g1' in user.generators and user.generators['g1'].amount > 0:
            first_upgrade_cost = user.generators['g1'].get_next_revenue_multiplier_price()
            if user.money >= first_upgrade_cost:
                if game_menu.active_panel != 'upgrades':
                    # If not in the upgrades panel, point to the 'Upgrades' navigation button.
                    upgrades_button = game_menu.nav_buttons[1] # 'Upgrades' button
                    draw_tutorial_hint(screen, upgrades_button.rect, "Time to upgrade!", 'right')
                else:
                    # If in the upgrades panel, point to the first upgrade's buy button.
                    first_upgrade_row = game_menu.upgrades_rows[0]
                    buy_button_rect = first_upgrade_row['btn'].rect
                    draw_tutorial_hint(screen, buy_button_rect, "Boost your income!", 'left')
    

