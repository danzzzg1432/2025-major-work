import sys
import os
import pygame
import json
from game_constants import *


class SaveStates:
    @staticmethod
    def get_path():
        return os.path.join(SAVE_DIR)

    @staticmethod
    def save_user(user):
        path = SaveStates.get_path()
        with open(path, "w") as f:
            json.dump(user.to_dict(), f, indent=4) 

    @staticmethod
    def load_user():
        path = SaveStates.get_path()
        with open(path) as f:
            data = json.load(f)
        return User.from_dict(data)

# Button Class
class Button: # global button class
    def __init__(self, x, y, width, height, text, background_colour, font, text_colour, callback=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.colour = background_colour
        self.initial_colour = background_colour
        self.font = font
        self.text_colour = text_colour
        self.callback = callback # calls a pre-defined function when a button is clicked, encapsulates button actions inside the button class itself

    def draw(self, screen): # draws the button on the screen
        pygame.draw.rect(screen, self.colour, self.rect, border_radius=30) 
        text_surf = self.font.render(self.text, True, self.text_colour)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
    
    def is_hovered(self, pos): # checks if the mouse is hovering over the button
        return self.rect.collidepoint(pos) 
    
    def click(self): # calls the callback function when the button is clicked
        if self.callback:
            self.callback()
        
class Generator:
    def __init__(self, id, name, base_rate, base_price, level=1, amount=0):
        self.id = id # unique identifier for the generator - constant generators are in game_constants.py
        self.base_rate = base_rate
        self.name = name
        self.base_price = base_price # base price of the generator
        self.level = level # multiplier level
        self.amount = amount # how many you own
    
    def manual_generate(self, user, quantity=1): # manually generated money
        amount = self.base_rate * self.level * quantity
        user.money += amount
        return amount # returns the amount of money generated, ill see if I need this or not
    
    
    @property
    def rate(self): # rate of the generator, how much money it generates per second
        return self.base_rate * self.amount * self.level
    
    @property
    def next_price(self): # price of the next generator, increases by 15% each time you buy one. This one is the one shown to the user - the buy() method has this already inline
        return int(self.base_price * (1.07 ** self.amount)) # price of the next generator, increases by 15% each time you buy one
    
    def buy(self, user, quantity=1): # buy a generator, quantity is the amount of generators to buy
        total_cost = sum(
            int(self.base_price * (1.07 ** i)) 
            for i in range(self.amount, self.amount + quantity)) # total cost of the generators
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
            amount=data["amount"]
        )

class Manager: # global manager class
    def __init__(self, id, name, cost, owned):
        self.id = id
        self.name = name
        self.cost = cost
        
    def buy(self, user):
        # attempts to hire this manager; deduct cost and register on user
        if self.id in user.managers:
            return False
        elif user.money >= self.cost:
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
        self.ensure_manager(manager_id)
        return self.managers[manager_id].buy(self)
    
    def ensure_manager(self, manager_id): # check if the manager exists in the user object, if not, create it
        if manager_id not in self.managers:
            proto = MANAGER_PROTOTYPES[manager_id]
            self.managers[manager_id] = Manager(manager_id, proto["name"], proto["cost"])

    def update(self, dt_seconds): # update the user object, called every frame
        for gen in self.generators.values():
            if gen.id in self.managers:
                self.money += gen.rate * dt_seconds
    
    def to_dict(self): # returns a dictionary of all the users data
        return{ 
               "money": self.money,
               "generators": {generator.to_dict() for generator in self.generators.values()},
               "managers": {manager.to_dict() for manager in self.managers.values()},
               }
    
    @classmethod
    def from_dict(cls, data): # creates a user object from a dictionary, essentially encapsulates the user object into a dictionary for saving/loading purposes
        user = cls(data["money"])
        for generator_data in data["generators"]:
            generator = Generator.from_dict(generator_data)
            user.generators[generator.id] = generator # add the generator to the user object
        for manager_data in data["managers"]:
            manager = Manager.from_dict(manager_data)
            user.managers[manager.id] = manager
        
        return user #
        
    # old code
    # def add_generator(self, generator): # perhaps later include a feature to multiple-buy generators -> add button in the shop menu which switches from 1x, 10x, 100x, then buy that amount probably by passing through the amount in this class
    #     if generator.name not in self.generators: # check if generator already exists
    #         self.generators[generator.name] = generator
    #     generator.increase_amount()
     
    # def get_money(self):
    #     return round(self.money)
    
    # def set_money(self, new_money):
    #     self.money = new_money
        
    # def earn_money(self, generator):
    #     if generator.name in self.generators:
    #         self.money += generator.generate_money()
    
# Screens and Menus
user = User(1000000) # test user lol
class StateManager: # global state manager
    def __init__(self, screen):
        self.state = TESTING # set initial state to main menu (for now)
        self.states = {
            MAIN_MENU: MainMenu(screen, self),
            GAME_MENU: GameMenu(screen, self),
            # SETTINGS_MENU: SettingsMenu(screen, self),
            # SHOP_MENU: ShopMenu(screen, self),
            # LOGIN_MENU: LoginMenu(screen, self),
            # REGISTER_MENU: RegisterMenu(screen, self),
            # HELP_MENU: HelpMenu(screen, self),
            TESTING: Testing(screen, user, self)
            } 

    def set_state(self, new_state): # set the state of the game
        self.state = new_state
        pygame.display.set_caption(f"{GAME_TITLE} - {new_state.replace('_', ' ').title()}") # set the window title to the current state


    def get_state(self): # get the current state of the game as a string.
        return self.state
        
    def get_state_object(self, state_name): # get the actual state OBJECT of a specific state 
        return self.states.get(state_name, None)
    
    def __str__(self): # debugging line to print all states and their types
        state_names = {key: type(value).__name__ for key, value in self.states.items()}
        print(f"Current States: {self.state}, States: {state_names}") if DEBUG_MODE else None # debugging line 
        return ""
class MainMenu: # Main menu class
    def __init__(self, screen, state_manager):
        self.screen = screen
        self.state_manager = state_manager
        self.button_font = pygame.font.Font(LOGO_FONT, MAIN_MENU_BUTTON_SIZE)
        self.title_font = pygame.font.Font(LOGO_FONT, MAIN_MENU_LOGO_SIZE)
        self.buttons = self.create_buttons()

    def render_title(self):
        title_surf = self.title_font.render(GAME_TITLE.upper(), True, BLACK)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 200))
        self.screen.blit(title_surf, title_rect)


    def create_buttons(self): # probably not the most optimised way to carry about this but its ok
        return [
            Button(main_button_x, 360, BUTTON_WIDTH, BUTTON_HEIGHT, "Start Game", GRAY, self.button_font, BLACK, callback=lambda: self.state_manager.set_state(GAME_MENU)),
            Button(main_button_x, 440, BUTTON_WIDTH, BUTTON_HEIGHT, "Load Game", GRAY, self.button_font, BLACK, callback=self.load_game),
            Button(main_button_x, 520, BUTTON_WIDTH, BUTTON_HEIGHT, "Settings", GRAY, self.button_font, BLACK, callback=self.settings),
            Button(main_button_x, 600, BUTTON_WIDTH, BUTTON_HEIGHT, "Quit", GRAY, self.button_font, BLACK, callback=self.quit_game)
        ]

    def handle_events(self, events): # handle events for the main menu
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for button in self.buttons:
                    if button.is_hovered(mouse_pos):
                        button.click()
        return True

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            if button.is_hovered(mouse_pos):
                button.colour = DARK_GRAY
            else:
                button.colour = button.initial_colour

    def render(self):
        self.screen.fill(WHITE)  # Set background colour
        self.screen.blit(main_menu_background) # load background image
        self.render_title()
        for button in self.buttons:
            button.draw(self.screen)
        pygame.display.flip()
        
    def load_game(self):
        # self.state_manager.set_state(GAME_MENU) -> Placeholder for load game functionality
        pass
    
    def settings(self):
        pass
    
    def quit_game(self):
        pygame.quit()
        sys.exit()
    
class GameMenu: # Game menu class, mostly placeholder for now
    def __init__(self, screen, state_manager):
        self.screen = screen
        self.state_manager = state_manager
        self.button_font = pygame.font.Font(LOGO_FONT, MAIN_MENU_BUTTON_SIZE)
        self.title_font = pygame.font.Font(LOGO_FONT, MAIN_MENU_LOGO_SIZE)
        self.buttons = self.create_buttons()

    def render_title(self):
        title_surf = self.title_font.render(GAME_TITLE.upper(), True, BLACK)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 200))
        self.screen.blit(title_surf, title_rect)


    def create_buttons(self):
        main_button_x = (SCREEN_WIDTH - BUTTON_WIDTH) // 2
        return [
            Button(main_button_x, 360, BUTTON_WIDTH, BUTTON_HEIGHT, "test test", "Red", self.button_font, BLACK,callback=None),
            Button(main_button_x, 440, BUTTON_WIDTH, BUTTON_HEIGHT, "test test", GRAY, self.button_font, BLACK,callback=None),
            Button(main_button_x, 520, BUTTON_WIDTH, BUTTON_HEIGHT, "test", GRAY, self.button_font, BLACK,callback=None),
            Button(main_button_x, 600, BUTTON_WIDTH, BUTTON_HEIGHT, "go back", GRAY, self.button_font, BLACK,callback=lambda: self.state_manager.set_state(MAIN_MENU))
        ]

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for button in self.buttons:
                    if button.is_hovered(mouse_pos):
                        button.click()
        return True

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            if button.is_hovered(mouse_pos):
                button.colour = DARK_GRAY
            else:
                button.colour = button.initial_colour
        # for generators in the user object, generate the amount of money. 

    def render(self):
        self.screen.fill(BLACK)  # Set background colour (Replace with actual background image later)
        self.screen.blit(idle_tutor_tycoon_logo) # render background, redundant very soon
        self.render_title()
        for button in self.buttons:
            button.draw(self.screen)
        pygame.display.flip()

class CreateFrect:
    def __init__(self, x, y, width, height, bg_colour, id=None, display=None, font=None, font_colour=None, image_path=None, display_callback=None):
        self.frect = pygame.FRect(x, y, width, height)
        self.bg_colour = bg_colour
        self.image = None
        self.id = id
        self.font = font
        self.font_colour = font_colour
        self.display = display # thing we display inside the frect 
        self.display_callback = display_callback # for displays requiring dynamic updates

        if image_path:  # Load and scale image if provided
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (width, height))

    def render_text(self, position="center", display=None): # default is center
        position_bank = {
        "center": "center",
        "topleft": "topleft",
        "topright": "topright",
        "bottomleft": "bottomleft",
        "bottomright": "bottomright",
        "midleft": "midleft",
        "midright": "midright",
        "midtop": "midtop",
        "midbottom": "midbottom"
        }
            # render text onto surface
        if self.font and self.font_colour:
            if self.display_callback: # if true, it is a dynamically updating block
                display = self.display_callback()
            else:
                display = display if display is not None else self.display # if display is None, use the default display value
            text_surface = self.font.render(str(display), True, self.font_colour)
            text_surface_rect = text_surface.get_rect()
            
            if position in position_bank:
                setattr(text_surface_rect, position_bank[position], getattr(self.frect, position_bank[position])) # set the position of the text rect to the frect position
            else:
                text_surface_rect.center = self.frect.center
        
            return text_surface, text_surface_rect
        return None, None # returns a tuple



    def draw(self, screen):
        # draw rect and render images
        if self.image:
            screen.blit(self.image, self.frect)
        else:
            pygame.draw.rect(screen, self.bg_colour, self.frect)

        # render text if applicable
        text_surface, text_rect = self.render_text()
        if text_surface and text_rect:
            screen.blit(text_surface, text_rect)

        
class Testing:
    def __init__(self, screen, user, state_manager):
        self.screen = screen
        self.state_manager = state_manager
        self.font = pygame.font.Font(LOGO_FONT, MAIN_MENU_BUTTON_SIZE)
        self.user = user
        self.buttons = self.create_buttons()
        self.screen_elements = {
            "money_display": CreateFrect(300, 60, 60, 60, "Pink", id="money_display", font=self.font, font_colour="Black", display_callback=lambda: f"ATAR POINTS: {round(self.user.money)}")
        }
        self.last_time = pygame.time.get_ticks() / 1000  # track for dt

    def create_buttons(self):
        buttons = []

        # dynamically create 3 columns: Buy Gen, Manual Gen, Hire Manager
        padding_x = 200
        padding_y = 200
        col_width = 220
        for idx, (generator_id, prototype) in enumerate(GENERATOR_PROTOTYPES.items()): # loop through all the generators
            x = padding_x + (idx * col_width)
            # 1) Buy Generator
            buttons.append(Button(
            x, padding_y + 0*60, BUTTON_WIDTH, BUTTON_HEIGHT,
            f"Buy {prototype['name']}",
            GRAY, self.font, BLACK,
            callback=lambda generator_id=generator_id: ( self.user.ensure_generator(generator_id), self.user.buy_generator(generator_id) )
            ))
            # 2) Manual Generate
            buttons.append(Button(x, padding_y + 1*60, BUTTON_WIDTH, BUTTON_HEIGHT, f"Gen {prototype['name']}", YELLOW, self.font, BLACK, callback=lambda generator_id=generator_id: ( self.user.ensure_generator(generator_id), self.user.generators[generator_id].manual_generate(self.user) )
            ))
            # 3) Hire Manager
            mproto = MANAGER_PROTOTYPES[generator_id]
            buttons.append(Button( x, padding_y + 2*60, BUTTON_WIDTH, BUTTON_HEIGHT, f"Hire {mproto['name']}", BLUE, self.font, BLACK, callback=lambda generator_id=generator_id: ( self.user.buy_manager(generator_id) )
            ))
        return buttons
       
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for button in self.buttons:
                    if button.is_hovered(mouse_pos):
                        button.click()
        return True
       
       
       
    def update(self):
        # 1) Auto‐production
        now = pygame.time.get_ticks() / 1000
        dt  = now - self.last_time
        self.user.update(dt)
        self.last_time = now

        # 2) Button hover coloring
        mouse_pos = pygame.mouse.get_pos()
        for btn in self.buttons:
            btn.colour = DARK_GRAY if btn.is_hovered(mouse_pos) else btn.initial_colour
       
       
    def render(self):
        self.screen.fill(WHITE)  # Set background colour
        self.screen.blit(main_menu_background) # load background image
        
        for button in self.buttons:
            button.draw(self.screen)
        for element in self.screen_elements.values():
            element.draw(self.screen)
        self.screen.blit(williamdu, (600, 600))
        
        
        pygame.display.flip()
       
       

       
       
       
       
       
       
        
# class ShopMenu: # Shop menu class
#     def __init__(self, screen, state_manager):
#         self.screen = screen
#         self.state_manager = state_manager

#     def handle_events(self, events):
#         for event in events:
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()

#     def update(self):
#         pass

#     def render(self):
#         self.screen.fill(GRAY)
#         pygame.display.flip()    
# class SettingsMenu: # Settings menu class
#     def __init__(self, screen, state_manager):
#         self.screen = screen
#         self.state_manager = state_manager

#     def handle_events(self, events):
#         for event in events:
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()

#     def update(self):
#         pass

#     def render(self):
#         self.screen.fill(GRAY)
#         pygame.display.flip()   
# class LoginMenu: # Login menu class
#     def __init__(self, screen, state_manager):
#         self.screen = screen
#         self.state_manager = state_manager

#     def handle_events(self, events):
#         for event in events:
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()

#     def update(self):
#         pass

#     def render(self):
#         self.screen.fill(GRAY)
#         pygame.display.flip()
# class RegisterMenu: # Register menu class
#     def __init__(self, screen, state_manager):
#         self.screen = screen
#         self.state_manager = state_manager

#     def handle_events(self, events):
#         for event in events:
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()

#     def update(self):
#         pass

#     def render(self):
#         self.screen.fill(GRAY)
#         pygame.display.flip()         
# class HelpMenu: # Help menu class
#     def __init__(self, screen, state_manager):
#         self.screen = screen
#         self.state_manager = state_manager

#     def handle_events(self, events):
#         for event in events:
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()

#     def update(self):
#         pass

#     def render(self):
#         self.screen.fill(GRAY)
#         pygame.display.flip()