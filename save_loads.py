import os
import json
from game_logic import User
from game_constants import *
from date_time import *

timecontroller = NTPTimer()  # Initialise the NTP timer to get the current time from an NTP server
class SaveStates:
    """
    This is the "class" that handles the writing and reading to disk.
    Organised here are the static methods (methods that arent inherently required to be in this class but make reasonable sense to be) for clarity.
    """
    @staticmethod
    def get_path():
        return os.path.join(SAVE_DIR) # get the path to the save file

    @staticmethod
    def save_user(user):
        path = SaveStates.get_path()
        print(f"\n (づ｡◕‿‿◕｡)づ Saving user to file location {path} \n") if DEBUG_MODE else None
        print(f"Current time = {timecontroller.get_current_time()}")
        save_data = {
            "user_data": user.to_dict(),
            "save_time": timecontroller.get_current_time().isoformat()  # Convert datetime to ISO format string
        }
        with open(path, "w") as f:
            json.dump(save_data, f, indent=4) # save the combined data to a file

    @staticmethod
    def load_user():
        path = SaveStates.get_path()
        print(f"\n (づ｡◕‿‿◕｡)づ Loading user from file location {path} \n ") if DEBUG_MODE else None 
        with open(path) as f:
            global data
            data = json.load(f) # load the combined data from a file
        
        user_data = data["user_data"]

        return User.from_dict(user_data) # return the loaded user object
    
    
    @staticmethod 
    def time_elapsed() -> float:
        
        path = SaveStates.get_path()
        print(f"\n (づ｡◕‿‿◕｡)づ Loading time from file location {path} \n ") if DEBUG_MODE else None 
        save_time_str = data.get("save_time") # Get the save time string
        saved_datetime = datetime.fromisoformat(save_time_str) # convert it back to datetime format
        deltatime = timecontroller.get_current_time() - saved_datetime # get the current time and subtract previously saved time
        return deltatime.total_seconds() # return that difference in seconds as a float


        
 