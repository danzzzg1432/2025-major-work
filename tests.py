# """Load user test"""
# from game_logic import User
# from save_loads import *

# user = SaveStates.load_user()
# print(isinstance(user, User))
# print(user.money)


# """Format large number test"""
# from utils import format_large_number

# print(format_large_number(1234567))


# """Buy generator success"""
# from game_logic import User

# # Create user with money 10
# user = User(money=10)
# print(f"Initial money: {user.money}")

# # Call user.buy_generator("g1") - g1 costs 3.738
# user.buy_generator("g1")

# # Check if user.generators["g1"].amount == 1 
# print(f"Generator g1 amount: {user.generators['g1'].amount}")
# print(f"Money after purchase: {user.money}")
# print(f"Expected money: {10 - 3}")
# expected_money = 10 - 3
# print("Buy generator success test passed!" if user.generators["g1"].amount == 1 and user.money == expected_money else "Buy generator success test failed!")


# """Buy generator insufficient funds"""
# from game_logic import User

# # Create user with money 100
# user = User(money=100)
# print(f"Initial money: {user.money}")

# # Call user.buy_generator("g0") - g0 costs around 25 billion
# user.buy_generator("g0")

# # Check if generator g0 amount = 0 and no money deducted
# print(f"Generator g0 amount: {user.generators['g0'].amount}")
# print(f"Money after failed purchase: {user.money}")
# print("Buy generator insufficient funds test passed!" if user.generators["g0"].amount == 0 and user.money == 100 else "Buy generator insufficient funds test failed!")


# """Manual Generate test"""
# from game_logic import User

# # Create user and ensure they own 1 generator g1
# user = User(money=10)
# user.buy_generator("g1")  # This will give them 1 g1 generator
# print(f"User has {user.generators['g1'].amount} g1 generators")
# print(f"g1.is_generating before manual generate: {user.generators['g1'].is_generating}")
# print(f"User money before manual generate: {user.money}")

# # Call user.manual_generate("g1")
# user.manual_generate("g1")

# # Verify g1.is_generating == True and g1.time_progress is set to base_time (0.6s)
# print(f"g1.is_generating after manual generate: {user.generators['g1'].is_generating}")
# print(f"g1.time_progress after manual generate: {user.generators['g1'].time_progress}")
# print(f"Expected time_progress: 0.6")
# print("Manual generate test passed!" if user.generators["g1"].is_generating == True and abs(user.generators["g1"].time_progress - 0.6) < 0.01 else "Manual generate test failed!")