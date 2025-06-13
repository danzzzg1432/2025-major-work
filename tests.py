"""Load user test"""
from game_logic import User
from save_loads import *

user = SaveStates.load_user()
print(isinstance(user, User))
print(user.money)


"""Format large number test"""
from utils import format_large_number

print(format_large_number(1234567))


"""Buy generator success"""







"""Buy generator failure"""





"""Manual Generate test"""