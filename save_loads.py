import os
import json
from game_logic import User
from game_constants import *
from date_time import *
from utils import Music

timecontroller = NTPTimer()  # Initialise the NTP timer to get the current time from an NTP server
class SaveStates:
    """
    This is the "class" that handles the writing and reading to disk.
    Organised here are the static methods (methods that arent inherently required to be in this class but make reasonable sense to be) for clarity.
    """
    @staticmethod
    def get_path():
        save_directory = os.path.dirname(SAVE_DIR)
        if save_directory and not os.path.exists(save_directory):
            os.makedirs(save_directory)
        return SAVE_DIR

    @staticmethod
    def save_all(user, music_player):
        path = SaveStates.get_path()
        print(f"\n (づ｡◕‿‿◕｡)づ Saving game state to {path} \n") if DEBUG_MODE else None
        save_data = {
            "user_data": user.to_dict(),
            "music_data": music_player.to_dict(),
            "save_time": timecontroller.get_current_time().isoformat(),
        }
        with open(path, "w") as f:
            json.dump(save_data, f, indent=4)

    @staticmethod
    def load_user():
        path = SaveStates.get_path()
        print(f"\n (づ｡◕‿‿◕｡)づ Loading user from file location {path} \n ") if DEBUG_MODE else None 
        with open(path) as f:
            data = json.load(f) # load the combined data from a file
        
        user_data = data["user_data"]

        return User.from_dict(user_data) # return the loaded user object
    
    @staticmethod
    def load_music():
        path = SaveStates.get_path()
        print(f"\n (づ｡◕‿‿◕｡)づ Loading music from file location {path} \n ") if DEBUG_MODE else None 
        with open(path) as f:
            data = json.load(f) # load the combined data from a file
        music_data = data["music_data"]
        return Music.from_dict(music_data)
    
    @staticmethod 
    def time_elapsed() -> float:
        path = SaveStates.get_path()
        if not os.path.exists(path):
            return 0.0

        try:
            with open(path) as f:
                data = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return 0.0

        save_time_str = data.get("save_time")
        if not save_time_str:
            return 0.0
        
        saved_datetime = datetime.fromisoformat(save_time_str)
        deltatime = timecontroller.get_current_time() - saved_datetime
        return deltatime.total_seconds() # return that difference in seconds as a float


        
 