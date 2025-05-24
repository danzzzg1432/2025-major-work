import os
import json
from game_logic import User
from game_constants import *
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
        with open(path, "w") as f:
            json.dump(user.to_dict(), f, indent=4) # save the user object to a file

    @staticmethod
    def load_user():
        path = SaveStates.get_path()
        print(f"\n (づ｡◕‿‿◕｡)づ Loading user from file location {path} \n ") if DEBUG_MODE else None 
        with open(path) as f:
            data = json.load(f) # load the user object from a file
        return User.from_dict(data) # return the loaded user object
 