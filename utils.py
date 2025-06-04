from game_constants import *
import os
import random
import pygame

def format_large_number(num):  
    """
    The game has numbers in the vigintillions - aka 20 zeros. Trying to display that on the screen is a bit too much,
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

class Music:
    """
    Music playback with volume, shuffling, playback controls and other stuff
    """
    def __init__(self, volume=0.05):
        self.playlist = self.load_playlist()
        self.current_song_index = 0
        self.volume = volume
        pygame.mixer.music.set_volume(self.volume)  # Set initial volume

        if self.playlist:
            random.shuffle(self.playlist)
            self.play_current_song()
        else:
            if DEBUG_MODE:
                print("Warning: No music files found in assets/sounds or directory missing.")

    def load_playlist(self):
        """
        Loads music files from the specified music directory.
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
        """
        Loads and plays the current song in the playlist.
        """
        try:
            pygame.mixer.music.load(self.playlist[self.current_song_index])
            pygame.mixer.music.play(loops=0)  # Play once; update() will handle the next song
        except pygame.error as e:
            if DEBUG_MODE:
                print(f"Error loading/playing music {self.playlist[self.current_song_index]}: {e}")

    def update(self):
        """
        Checks if the current song has finished and plays the next one
        """
        if self.playlist and not pygame.mixer.music.get_busy():
            self.current_song_index += 1 # increment the current song index to avoid playing the same song twice (when choosing a random song)
            if self.current_song_index >= len(self.playlist):
                self.current_song_index = 0
                random.shuffle(self.playlist)  # Reshuffle when the playlist completes
            self.play_current_song()

    def set_volume(self, volume_level):
        self.volume = max(0.0, min(1.0, volume_level))
        pygame.mixer.music.set_volume(self.volume)

    def play(self):
        if self.playlist:
            if not pygame.mixer.music.get_busy(): # Not playing
                self.play_current_song()
            else: # if paused, unpause
                pygame.mixer.music.unpause()

    def pause(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()

    def stop(self):
        pygame.mixer.music.stop()

