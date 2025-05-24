from game_constants import *

class Generator:
    # TODO: FIX 
    def __init__(self, id, name, base_rate, base_price, level=1, amount=0, growth_rate=1.07):
        self.id = id # unique identifier for the generator - constant generators are in game_constants.py
        self.base_rate = base_rate
        self.name = name
        self.base_price = base_price # base price of the generator
        self.level = level # multiplier level
        self.amount = amount # how many you own
        self.growth_rate = growth_rate # growth rate of the generator, how much the price increases each time you buy one
    
    def manual_generate(self, user): # manually generated money
        if self.amount == 0: # if you dont own any generators, return 0
            return 0
        elif self.id in user.managers: # if you own a manager for that generator, do not generate manually.
            return 0
        amount = self.base_rate * self.level * self.amount # base * level * amount
        user.money += amount
        return amount # returns the amount of money generated, ill see if I need this or not
    
    
    @property
    def rate(self): # rate of the generator, how much money it generates per second
        return self.base_rate * self.amount * self.level
    
    @property
    def next_price(self): # price of the next generator, increases by 15% each time you buy one. This one is the one shown to the user - the buy() method has this already inline
        return int(self.base_price * (self.growth_rate ** self.amount)) # price of the next generator, increases by 15% each time you buy one
    
    def buy(self, user, quantity=1): # buy a generator, quantity is the amount of generators to buy
        a = self.base_price * (self.growth_rate ** self.amount)
        n = quantity
        # Formula for sum of geometric series: a * (1 - r^n) / (1 - r), where r is the generator's growth rate. actual application of mathematics is crazy
        if self.growth_rate != 1:
            total_cost = int(a * (1 - (self.growth_rate)**n) / (1 - (self.growth_rate)))
        else:
            total_cost = int(a * n)
        if user.money >= total_cost:
            user.money -= total_cost
            self.amount += quantity # increase the amount of generators owned
    
    def to_dict(self): # returns a dictionary of the generator object
        return { 
                "id": self.id,
                "level": self.level,
                "amount": self.amount,
                }
    
    @classmethod
    def from_dict(cls, data): # creates a generator object from a dictionary, essentially encapsulates the generator object into a dictionary for saving/loading purposes
        proto = GENERATOR_PROTOTYPES[data["id"]]
        return cls(
            id=data["id"],
            name=proto["name"],
            base_rate=proto["base_rate"],
            base_price=proto["base_price"],
            level=data["level"],
            amount=data["amount"],
            growth_rate=proto["growth_rate"]
        )
        
class Manager: # global manager class
    def __init__(self, id, name, cost):
        self.id = id
        self.name = name
        self.cost = cost
        
    def buy(self, user):
        # attempts to hire this manager; deduct cost and register on user
        if user.money >= self.cost:
            user.money -= self.cost
            user.managers[self.id] = self
            return True
        return False

    def to_dict(self): # returns a dictionary of the manager object
        return { "id": self.id }
    
    
    @classmethod
    def from_dict(cls, data): # creates a manager object from a dictionary, essentially encapsulates the manager object into a dictionary for saving/loading purposes
        proto = MANAGER_PROTOTYPES[data["id"]]
        return cls(id=data["id"], name=proto["name"], cost=proto["cost"])
        
        
class User:
    def __init__(self, money=0):
        self.generators = {}
        self.money = money
        self.managers = {} 
        
    def manual_generate(self, generator_id): # manually generate money from a generator
        self.ensure_generator(generator_id) # ensure the generator exists in the user object
        return self.generators[generator_id].manual_generate(self) # call the manual_generate method of the generator
    
    def buy_generator(self, generator_id, quantity=1): # buy a generator, quantity is the amount of generators to buy
        self.ensure_generator(generator_id) # ensure the generator exists in the user object
        self.generators[generator_id].buy(self, quantity) # buy the generator(s)
        
    def ensure_generator(self, generator_id): # check if the generator exists in the user object, if not, create it
        if generator_id not in self.generators:
            prototype = GENERATOR_PROTOTYPES[generator_id] 
            self.generators[generator_id] = Generator( # append generator(s) to the user 
                id=generator_id,
                name=prototype["name"],
                base_rate=prototype["base_rate"],
                base_price=prototype["base_price"]
            )
        
    def buy_manager(self, manager_id): # buy a manager
        if manager_id in self.managers:
            return False
        if manager_id not in self.generators or self.generators[manager_id].amount == 0: # check if the generator exists in the user object and if you own it
            return False
        self.ensure_manager(manager_id)
        return self.managers[manager_id].buy(self)
    
    def ensure_manager(self, manager_id): # check if the manager exists in the user object, if not, create it
        if manager_id not in self.managers:
            proto = MANAGER_PROTOTYPES[manager_id]
            self.managers[manager_id] = Manager(manager_id, proto["name"], proto["cost"])

    def update(self, dt_seconds): # update the user object, called every frame
        for gen in self.generators.values():
            if gen.id in self.managers and gen.amount > 0: # 
                self.money += gen.rate * dt_seconds
    
    @property 
    def income_per_second(self): # returns the total income per second of all generators
        total_income = 0
        for gen_id, gen in self.generators.items():
            if gen_id in self.managers and gen.amount > 0:
                total_income += gen.rate # only add income per second if manager is purchased
        return total_income
    
    
    def to_dict(self): # returns a dictionary of all the users data
        return {
            "money": self.money,
            "generators": [generator.to_dict() for generator in self.generators.values()],
            "managers": [manager.to_dict() for manager in self.managers.values()],
        }
        
    def debug_generators(self):  # new debugging method
        print("---- Debug Generators Info ----")
        for gen_id, generator in self.generators.items():
            manager = self.managers.get(gen_id)
            manager_str = f"Manager: {manager.name}" if manager else "No Manager Assigned"
            print(f"Generator: {generator.name} | Owned: {generator.amount} | {manager_str}")
        print("-------------------------------")
    
    @classmethod
    def from_dict(cls, data): # creates a user object from a dictionary for saving/loading purposes
        user = cls(data["money"])
        for generator_data in data.get("generators", []):
            generator = Generator.from_dict(generator_data)
            user.generators[generator.id] = generator # add the generator to the user object
        for manager_data in data.get("managers", []):
            manager = Manager.from_dict(manager_data)
            user.managers[manager.id] = manager
        return user