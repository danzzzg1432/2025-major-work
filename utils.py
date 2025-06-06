from game_constants import *
from game_logic import User
import os
import random
import pygame
import datetime

def format_large_number(num):  
    """
    The game has numbers in the vigintillions - aka 102 zeros (though reaching those values may take years). Trying to display that on the screen is a bit too much,
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
    from save_loads import SaveStates
    try: # Load user data from save file
        
        time_elapsed_offline = SaveStates.time_elapsed()
        print(f"\nTime elapsed when loading user {time_elapsed_offline}") if DEBUG_MODE else None
        lets_see = 0
        for gen_id, gen in user.generators.items():
            if gen.amount > 0 and (gen.is_generating or gen.id in user.managers):
                remaining_offline_time_for_gen = time_elapsed_offline
                effective_time_for_cycle = gen.get_effective_time(user.generators)

                if gen.is_generating: # Cycle was in progress
                    if gen.time_progress <= remaining_offline_time_for_gen:
                        user.money += gen.cycle_output # Add money for this completed cycle
                        lets_see += gen.cycle_output
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
                            lets_see += gen.cycle_output * num_full_cycles_offline
                            remaining_offline_time_for_gen -= num_full_cycles_offline * effective_time_for_cycle
                        
                        # Update progress of the current (potentially new) cycle
                        if remaining_offline_time_for_gen > 0:
                            gen.time_progress -= remaining_offline_time_for_gen
                        else: # All time used up by full cycles
                            gen.is_generating = False # Reset if it perfectly finished
                            if gen.id in user.managers: # And restart if managed
                                gen.start_generation_cycle(user.generators)
        print(f"\nOffline progress added: ${lets_see} (simulated) ") if DEBUG_MODE else None

    except Exception as e:
        print(f"\n\n (≧ヘ≦ ) Error simulating offline progress: {e} (≧ヘ≦ ) \n\n") if DEBUG_MODE else None
        
class Music:
    """
    Music playback with volume, shuffling, playback controls and other stuff
    """
    def __init__(self, volume=0.05):
        self.playlist = self.load_playlist()
        self.current_song_index = 0
        self.volume = volume
        pygame.mixer.music.set_volume(self.volume)  # Set initial volume
        self.is_paused = False # Track pause state

        if self.playlist:
            random.shuffle(self.playlist)
            self.play_current_song()
        else:
            if DEBUG_MODE:
                print("Warning: No music files found in assets/sounds or directory missing.")

    def load_playlist(self):
        """
        Loads music files from the specified music directory
        """
        music_dir = os.path.join(ASSETS_DIR, "sounds")
        supported_formats = ('.mp3') # Add other supported formats if needed
        playlist_files = []
        for f_name in os.listdir(music_dir):
            if f_name.lower().endswith(supported_formats):
                playlist_files.append(os.path.join(music_dir, f_name))
        
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
        instance = cls()
        instance.volume = data.get("volume", 0.50)
        instance.is_paused = data.get("is_paused", False)
        return instance


