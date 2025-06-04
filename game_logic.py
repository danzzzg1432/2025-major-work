from game_constants import *

def apply_upgrades(user, generator_id_that_triggered_check):
    """
    Calculates and updates levels for ALL generators based on their specific
    and the current global upgrade tiers with stacking multipliers
    """

    highest_achieved_global_multiplier = 1  # Start with base multiplier of 1
    for thresh_global, mult_global in GENERATOR_UPGRADES.get("global", []):
        if all(g.amount >= thresh_global for g in user.generators.values()):
            highest_achieved_global_multiplier = max(highest_achieved_global_multiplier, mult_global)

    # Update each generator's level based on its specific upgrades and the global multiplier
    for gen_id, gen_obj in user.generators.items():
        # Determine the highest applicable specific multiplier for this generator
        specific_multiplier_for_this_gen = 1  
        for thresh_specific, mult_specific in GENERATOR_UPGRADES.get(gen_id, []):
            if gen_obj.amount >= thresh_specific:
                specific_multiplier_for_this_gen = max(specific_multiplier_for_this_gen, mult_specific)
        
        # The final level is the product of the specific and global multipliers.
        new_level = specific_multiplier_for_this_gen * highest_achieved_global_multiplier
        gen_obj.level = new_level


class Generator:
    """
    Represents the money-generating entity in the game. 
    
    """
    def __init__(self, id, name, base_rate, base_price, base_time, level=1, amount=0, growth_rate=1.07, time_progress=0.0, is_generating=False):
        self.id = id
        self.base_rate = base_rate # rate of money generation per cycle
        self.name = name
        self.base_price = base_price # price of one generator
        self.base_time = base_time  # Time in seconds for one cycle
        self.level = level # multiplier for base_rate
        self.amount = amount # number of generators owned
        self.growth_rate = growth_rate # multiplier for price
        self.time_progress = time_progress  # Remaining time for the current cycle
        self.is_generating = is_generating  # True if currently in a generation cycle

    def get_effective_time(self, all_user_generators):
        """Calculates the effective time for a generation cycle after milestone reductions."""
        effective_time = self.base_time
        
        # Apply individual generator milestones
        for milestone in GENERATOR_TIME_MILESTONES:
            if self.amount >= milestone:
                effective_time /= 2
        
        # Apply global milestones
        for milestone in GLOBAL_TIME_MILESTONES:
            if all(g.amount >= milestone for g in all_user_generators.values()):
                effective_time /= 2
                
        return max(MIN_GENERATION_TIME, effective_time) # Ensure time doesn't drop below a minimum for performance purposes
    
    def start_generation_cycle(self, all_user_generators):
        """Starts a new generation cycle if not already generating and has amount > 0."""
        if self.amount > 0 and not self.is_generating:
            self.time_progress = self.get_effective_time(all_user_generators)
            self.is_generating = True

    def update(self, dt_seconds, user):
        """Updates the generator's time progress and handles cycle completion."""
        if self.is_generating and self.amount > 0:
            self.time_progress -= dt_seconds
            if self.time_progress <= 0:
                money_generated = self.base_rate * self.level * self.amount
                user.money += money_generated
                self.is_generating = False # Cycle complete
                # If managed, automatically restart the cycle
                if self.id in user.managers:
                    self.start_generation_cycle(user.generators) # Pass all user generators for milestone checks
    
    def manual_generate(self, user):
        """Manually starts a generation cycle for this generator."""
        if self.amount == 0:
            return 0
        # Manual generation starts a cycle, it doesn't bypass the timer
        # If its already generating (e.g. by manager), manual click does nothing extra for this cycle
        if not self.is_generating:
            self.start_generation_cycle(user.generators)
        return self.base_rate * self.level * self.amount # Return potential amount if ever needed
    
    @property
    def cycle_output(self):
        """Money generated per completed cycle."""
        return self.base_rate * self.amount * self.level

    @property
    def rate(self):
        """Effective rate of money generation per second, considering cycle time."""
        if self.amount == 0:
            return 0
        effective_time = self.get_effective_time({}) # Pass empty dict if no access to all generators, or rethink
        if effective_time == 0: # Avoid division by zero
             return float('inf') # Or some large number, or handle as an error
        return self.cycle_output / effective_time
    
    @property
    def next_price(self):
        return int(self.base_price * (self.growth_rate ** self.amount))
    
    def buy(self, user, quantity=1):
        a = self.base_price * (self.growth_rate ** self.amount)
        n = quantity
        if self.growth_rate != 1:
            total_cost = int(a * (1 - (self.growth_rate)**n) / (1 - (self.growth_rate))) # geometric series sum formula. if you need me to prove this, ask me
        else:
            total_cost = int(a * n)
        if user.money >= total_cost:
            user.money -= total_cost
            self.amount += quantity
            if user:
                apply_upgrades(user, self.id)
            # If it's the first purchase and not managed, start the first cycle
            # if self.amount == quantity and not self.is_generating and self.id not in user.managers:
            #     self.start_generation_cycle(user.generators) 

    def to_dict(self):
        return { 
                "id": self.id,
                "level": self.level,
                "amount": self.amount,
                "time_progress": self.time_progress,
                "is_generating": self.is_generating,
                }
    
    @classmethod
    def from_dict(cls, data):
        proto = GENERATOR_PROTOTYPES[data["id"]]
        return cls(
            id=data["id"],
            name=proto["name"],
            base_rate=proto["base_rate"],
            base_price=proto["base_price"],
            base_time=proto["base_time"], 
            level=data.get("level", 1), # default to 1
            amount=data.get("amount", 0), # default to 0
            growth_rate=proto["growth_rate"],
            time_progress=data.get("time_progress", 0.0), # default to 0.0
            is_generating=data.get("is_generating", False) # default to False
        )
        
class Manager:
    def __init__(self, id, name, cost):
        self.id = id
        self.name = name
        self.cost = cost
        
    def buy(self, user):
        if user.money >= self.cost:
            user.money -= self.cost
            user.managers[self.id] = self
            # If the generator is now managed, ensure its cycle starts if it's not already running
            if self.id in user.generators and user.generators[self.id].amount > 0 and not user.generators[self.id].is_generating:
                user.generators[self.id].start_generation_cycle(user.generators)
            return True
        return False

    def to_dict(self):
        return { "id": self.id }
    
    @classmethod
    def from_dict(cls, data):
        proto = MANAGER_PROTOTYPES[data["id"]]
        return cls(id=data["id"], name=proto["name"], cost=proto["cost"])
        
        
class User:
    """
    The current user class. Handles the generators, managers and money owned.
    """
    def __init__(self, money=0.0):
        self.generators = {}
        self.money = float(money)
        self.managers = {} 
        
    def manual_generate(self, generator_id):
        self.ensure_generator(generator_id)
        return self.generators[generator_id].manual_generate(self)
    
    def buy_generator(self, generator_id, quantity=1):
        self.ensure_generator(generator_id)
        self.generators[generator_id].buy(self, quantity)
        
    def ensure_generator(self, generator_id):
        if generator_id not in self.generators:
            prototype = GENERATOR_PROTOTYPES[generator_id] 
            self.generators[generator_id] = Generator(
                id=generator_id,
                name=prototype["name"],
                base_rate=prototype["base_rate"],
                base_price=prototype["base_price"],
                base_time=prototype["base_time"]
            )
        
    def buy_manager(self, manager_id):
        if manager_id in self.managers:
            return False
        if manager_id not in self.generators or self.generators[manager_id].amount == 0:
            return False
        target_manager_proto = MANAGER_PROTOTYPES[manager_id]
        target_manager = Manager(manager_id, target_manager_proto["name"], target_manager_proto["cost"])
        if target_manager.buy(self):
            # If manager bought, and generator exists and has items, start its cycle if not already running
            # if manager_id in self.generators and self.generators[manager_id].amount > 0 and not self.generators[manager_id].is_generating:
            #      self.generators[manager_id].start_generation_cycle(self.generators)
            # print(f"purchase of {manager_id} was successful") if DEBUG_MODE else None
            return True
        else:
            print(f"purchase of {manager_id} was failed") if DEBUG_MODE else None
            return False
        
    def update(self, dt_seconds):
        for gen_id, gen in self.generators.items():
            gen.update(dt_seconds, self) # Call generator's own update method
            # Manager logic is now handled within Generator.update and Manager.buy
    
    @property 
    def income_per_second(self):
        total_income_rate = 0.0
        for gen_id, gen in self.generators.items():
            if gen_id in self.managers and gen.amount > 0: # Only count managed generators for passive income
                # Calculate rate based on cycle output and effective time
                effective_time = gen.get_effective_time(self.generators)
                if effective_time > 0: 
                    total_income_rate += (gen.base_rate * gen.level * gen.amount) / effective_time
        return total_income_rate
    
    def to_dict(self):
        return {
            "money": self.money,
            "generators": [generator.to_dict() for generator in self.generators.values()],
            "managers": [manager.to_dict() for manager in self.managers.values()],
        }
        
    def debug_generators(self):
        print("---- Debug Generators Info ----")
        for gen_id, generator in self.generators.items():
            manager = self.managers.get(gen_id)
            manager_str = f"Manager: {manager.name}" if manager else "No Manager Assigned"
            time_info = f"Time: {generator.time_progress:.2f}s / {generator.get_effective_time(self.generators):.2f}s" if generator.is_generating else f"Time: {generator.get_effective_time(self.generators):.2f}s (Idle)"
            print(f"Generator: {generator.name} | Owned: {generator.amount} | Level: {generator.level} | {manager_str} | {time_info}")
        print("-------------------------------")
    
    @classmethod
    def from_dict(cls, data):
        user = cls(data.get("money", 0.0))
        for generator_data in data.get("generators", []):
            generator = Generator.from_dict(generator_data)
            user.generators[generator.id] = generator
        for manager_data in data.get("managers", []):
            manager = Manager.from_dict(manager_data)
            user.managers[manager.id] = manager
            # After loading, if a generator is managed, ensure its cycle starts if it was saved as not generating
            # but should be (e.g. if it has amount and is managed)
            if manager.id in user.generators and user.generators[manager.id].amount > 0 and not user.generators[manager.id].is_generating:
                user.generators[manager.id].start_generation_cycle(user.generators)
        return user