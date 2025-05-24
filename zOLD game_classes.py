import sys
import os
import pygame
import json
from game_constants import *

"""
Other than user-touchable stuff, other things generally do not have error handling
"""

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
    suffixes = ["", "K", "MILLION", "BILLION", "TRILLION", "QUADRILLION", 
                "QUINTILLION", "SEXTILLION", "SEPTILLION", "OCTILLION", "NONILLION", "DECILLION", "UNDECILLION", 
                "DUODECILLION", "TREDECILLION", "QUATTUORDECILLION", "QUINDECILLION", "SEXDECILLION", "SEPTENDECILLION", 
                "OCTODECILLION", "NOVEMDECILLION", "VIGINTILLION"]
    
    if magnitude < len(suffixes):
        return f"{formatted_num} {suffixes[magnitude]}" # if the number has a pretty suffix, return it with the suffix
    else:
        return f"{formatted_num}e{magnitude*3}" # if the number is too large, return it in scientific notation


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
 
# Button Class
class Button: # global button class
    """
    This is the button class that handles the button creation and rendering.
    It is a simple class that takes in the x, y, width, height, text, colour, font, text_colour, callback and display callback functions and returns an object out of it.
    It handles its own rendering, clicking, hovering and any other events needed through callbacks and lambdas.
    """
    def __init__(self, x, y, width, height, text, colour, font, text_colour, callback=None, display_callback=None, button_id=str): # callback is a function that is called when the button is clicked
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.colour = colour
        self.initial_colour = colour
        self.font = font
        self.text_colour = text_colour
        self.callback = callback # calls a pre-defined function when a button is clicked, encapsulates button actions inside the button class itself
        self.display_callback = display_callback # for displays requiring dynamic updates
        self.id = button_id # unique identifier

    def draw(self, screen): # draws the button on the screen
        if self.display_callback: # if display_callback is set, use it to get the text.
            self.text = self.display_callback()
        pygame.draw.rect(screen, self.colour, self.rect, border_radius=30) # draw the button
        text_surf = self.font.render(self.text, True, self.text_colour) # render the text
        text_rect = text_surf.get_rect(center=self.rect.center) # get the rect of the text
        screen.blit(text_surf, text_rect) # blit the text on the button
    
    def is_hovered(self, pos): # checks if the mouse is hovering over the button
        return self.rect.collidepoint(pos) 
    
    def click(self): # calls the callback function when the button is clicked
        if self.callback:
            self.callback()
        
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



        
    
# Screens and Menus
class StateManager: # global state manager
    """
    Handles state transitions and current state of the game. 
    Initialises with the screen and user objects, and passes them onto the states.
    Analogous to central station in Sydney, but less cool.
    """
    def __init__(self, screen, user):
        self.state = MAIN_MENU
        self.states = {
            MAIN_MENU: MainMenu(screen, user, self),
            GAME_MENU: GameMenu(screen, user, self),
            # SETTINGS_MENU: SettingsMenu(screen, self),
            # SHOP_MENU: ShopMenu(screen, self),
            # LOGIN_MENU: LoginMenu(screen, self),
            # REGISTER_MENU: RegisterMenu(screen, self),
            # HELP_MENU: HelpMenu(screen, self),
            TESTING: Testing(screen, user, self)
            } 
        self.user = user

    def set_state(self, new_state): # set the state of the game
        self.state = new_state # changes the state to the new state. 
        pygame.display.set_caption(f"{GAME_TITLE} - {new_state.replace('_', ' ').title()}") # set the window title to the current state


    @property
    def current_state(self): # get the current state object
        return self.get_state_object(self.state)
    
    
    def get_state_object(self, state_name): # get the state object from the states dictionary
        return self.states.get(state_name, None)
    
    def __str__(self): # debugging line to print all states and their types
        state_names = {key: type(value).__name__ for key, value in self.states.items()}
        print(f"Current States: {self.state}, States: {state_names}") if DEBUG_MODE else None # debugging line 
        return ""
    
class MainMenu:  # —— Main menu screen, matching your sketch —— 
    def __init__(self, screen, user, state_manager):
        self.screen = screen
        self.state_manager = state_manager
        self.title_font = pygame.font.Font(LOGO_FONT, 100)
        self.button_font = DEFAULT_FONT
        self.user = user
        # two big center buttons
        self.buttons = self.create_buttons()

        # three round icons on the left
        self.icons = self.create_icons()


    def create_buttons(self):
        main_x = (SCREEN_WIDTH - BUTTON_WIDTH) // 2
        return [
            Button(
                main_x, 360, BUTTON_WIDTH, BUTTON_HEIGHT,
                "Enter Game", GRAY, self.button_font, BLACK,
                callback=self.start_game
            ),
            Button(
                main_x, 440, BUTTON_WIDTH, BUTTON_HEIGHT,
                "Settings", GRAY, self.button_font, BLACK,
                callback=self.open_settings
            ),
        ]

    def create_icons(self):
        icon_size = 60
        icon_x = 50
        y_start = 360
        spacing = 100

        return [
            CreateFrect(
                icon_x, y_start + i*spacing,
                icon_size, icon_size,
                WHITE,
                id=icon_id,
                display=char,
                font=self.button_font,
                font_colour=BLACK
            )
            for i, (icon_id, char) in enumerate([
                ("help", "?"),        # top: help
                ("settings", "√∆"),       # middle: stats (placeholder)
                ("quit", "∫xdx"),        # bottom: quit
            ])
        ]

    # callbacks ─────────────────────────────────────────────────────────
    def start_game(self):
        # self.state_manager.set_state(TESTING) if DEBUG_MODE else self.state_manager.set_state(GAME_MENU)
        self.state_manager.set_state(GAME_MENU)

    def open_settings(self):
        # TODO: swap to SettingsMenu state when it's implemented
        self.settings()

    def show_help(self):
        # TODO: implement help-screen transition here
        print("Help icon clicked") if DEBUG_MODE else None

    # event handling ────────────────────────────────────────────────────
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                if self.user:
                    SaveStates.save_user(self.user)
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                # icons
                for icon in self.icons:
                    if icon.frect.collidepoint(pos):
                        if icon.id == "help":
                            self.show_help()
                        elif icon.id == "quit":
                            # call existing quit_game (saves & sys.exit)
                            self.quit_game()
                        # elif icon.id == "stats":
                
                # big buttons
                for btn in self.buttons:
                    if btn.is_hovered(pos):
                        btn.click()

        return True

    # hover-state updates ─────────────────────────────────────────────────
    def update(self):
        pos = pygame.mouse.get_pos()
        for btn in self.buttons:
            btn.colour = DARK_GRAY if btn.is_hovered(pos) else btn.initial_colour

    # rendering ───────────────────────────────────────────────────────────
    def render(self):
        
        # # draw title
        # title_surf = self.title_font.render(GAME_TITLE, True, BLACK)
        # title_rect = title_surf.get_rect(center=(SCREEN_WIDTH//2, 200))
        # self.screen.blit(title_surf, title_rect)
        
        self.screen.blit(main_menu_background, (-200,0)) 
        
        # draw big buttons
        for btn in self.buttons:
            btn.draw(self.screen)

        # draw left-side icons
        for icon in self.icons:
            icon.draw(self.screen)

        pygame.display.flip()

   # unfinished stuff ──────────────────────────────────────────────────────────
    def settings(self):
        pass

    def quit_game(self):
        SaveStates.save_user(self.user)
        pygame.quit()
        sys.exit()


class GameMenu:
    ROW_HEIGHT = 110
    LEFT_COL_X  = 180
    RIGHT_COL_X = 680        # two symmetrical columns
    ICON_SIZE   = 80
    BAR_W, BAR_H = 420, 60

    def __init__(self, screen, user, state_manager):
        self.screen         = screen
        self.state_manager  = state_manager
        self.user           = user

        self.title_font   = pygame.font.Font(LOGO_FONT, 60)
        self.subtitle_font= pygame.font.Font(LOGO_FONT, 28)
        self.row_font     = pygame.font.Font(LOGO_FONT, 22)
        self.last_time = pygame.time.get_ticks() / 1000  # track for dt

        # top-of-screen HUD ───────────────────────────────────────────────
        self.hud_elems = { # create the HUD elements
            # "money":   CreateFrect( 20, 20,  60, 60, WHITE,
            #                         font=self.subtitle_font, font_colour=BLACK,
            #                         display_callback=lambda:
            #                             f"{format_large_number(round(self.user.money))}"),
            # "income":  CreateFrect( 20, 80,  60, 60, WHITE,
            #                         font=self.subtitle_font, font_colour=BLACK,
            #                         display_callback=lambda:
            #                             f"{format_large_number(round(self.user.income_per_second))}/s"),
            "exit":    Button(SCREEN_WIDTH-80, 20, 60, 60, "EXIT", LIGHT_GRAY,
                              self.subtitle_font, BLACK,
                              callback=self.save_and_exit)
        }

        # setting generator rows ──────────────────────────────────────────────────
        self.rows = self.create_rows()

    # helper – builds the 2-column grid of generator rows ──────────────────────────────────────────────────────────
    
    # TODO: add outlines, background, colours, etc.
    # most stuff is copied from testing class lol
    """
    notes
    bugs ive noted:
    theres actually a error where the game still calculates generation even on main menu but that is actually an intended feature just not implemented correctly lol
    display errors exist too
    
    """
    
    def create_rows(self):
        rows, idx = [], 0
        for g_id, proto in GENERATOR_PROTOTYPES.items():
            col_x = self.LEFT_COL_X  if idx % 2 == 0 else self.RIGHT_COL_X
            row_y = 180 + (idx//2) * self.ROW_HEIGHT

            # icon (manual generate)
            icon = CreateFrect(col_x, row_y, self.ICON_SIZE, self.ICON_SIZE,
                               WHITE, id=f"icon_{g_id}",
                               font=self.row_font, font_colour=BLACK,
                               display=proto["name"][0]) 

            #‘owned’ pill – sits at icon’s bottom
            owned = CreateFrect(col_x+15, row_y+self.ICON_SIZE-10, 50, 24,
                                LIGHT_GRAY,
                                font=self.row_font, font_colour=BLACK,
                                display_callback=lambda gid=g_id:
                                    f"{self.user.generators.get(gid,Generator(gid,**proto)).amount}")

            # long bar that shows this generator’s/sec + BUY button 
            bar_x = col_x + self.ICON_SIZE + 30
            rev_bar = CreateFrect(bar_x, row_y+20, self.BAR_W, self.BAR_H,
                                  WHITE,
                                  font=self.row_font, font_colour=BLACK,
                                  display_callback=lambda gid=g_id:
                                      f"{format_large_number(self.user.generators.get(gid,Generator(gid,**proto)).rate)}/s")

            buy_btn = Button(bar_x+10, row_y+self.ICON_SIZE-14, 180, 32,
                             "",
                             GRAY, self.row_font, BLACK,
                             callback=lambda gid=g_id: (
                                 self.user.ensure_generator(gid),
                                 self.user.buy_generator(gid)),
                             display_callback=lambda gid=g_id, pr=proto:
                                 f"Buy ({format_large_number(self.user.generators.get(gid,Generator(gid,**pr)).next_price)})")

            rows.append(
                {"g_id": g_id,
                 "icon": icon, "owned": owned,
                 "rev": rev_bar, "buy": buy_btn}
            )
            idx += 1
        return rows

    # event handling ──────────────────────────────────────────────────────────
    def handle_events(self, events): 
        for e in events:
            if e.type == pygame.QUIT:
                SaveStates.save_user(self.user);  pygame.quit();  sys.exit()

            elif e.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                # a) HUD exit button
                if self.hud_elems["exit"].is_hovered(pos):
                    self.hud_elems["exit"].click()

                # b) generator rows
                for r in self.rows:
                    if r["icon"].frect.collidepoint(pos):
                        self.user.ensure_generator(r["g_id"])
                        self.user.generators[r["g_id"]].manual_generate(self.user)
                    if r["buy"].is_hovered(pos):
                        r["buy"].click()
        return True


    # update loop ──────────────────────────────────────────────────────────
    def update(self):
        now = pygame.time.get_ticks() / 1000
        dt  = now - self.last_time
        self.user.update(dt)
        self.last_time = now

        mouse = pygame.mouse.get_pos() # get mouse position
        self.hud_elems["exit"].colour = DARK_GRAY if self.hud_elems["exit"].is_hovered(mouse) else self.hud_elems["exit"].initial_colour
        for r in self.rows:
            r["buy"].colour = DARK_GRAY if r["buy"].is_hovered(mouse) else r["buy"].initial_colour




    # draw everything ──────────────────────────────────────────────────────────
    def render(self):
        # blit background image
        self.screen.blit(game_menu_background, (0,0)) # load background image

        # Centered Values
        money_val_str = format_large_number(round(self.user.money))
        income_val_str = f"{format_large_number(round(self.user.income_per_second))}/s"

        # ATAR POINTS value
        money_value_surf = self.title_font.render(money_val_str, True, WHITE) # Use title_font for larger display
        money_value_rect = money_value_surf.get_rect(midtop=(SCREEN_WIDTH//2,  20))
        self.screen.blit(money_value_surf, money_value_rect)

        # REVENUE PER SECOND value
        income_value_surf = self.subtitle_font.render(income_val_str, True, BLACK)
        income_value_rect = income_value_surf.get_rect(midtop=(SCREEN_WIDTH//2, money_value_rect.bottom + 10)) # Position below ATAR points
        self.screen.blit(income_value_surf, income_value_rect)
        # HUD widgets

        for elem in self.hud_elems.values():
            elem.draw(self.screen)

        # generator rows
        for r in self.rows:
            r["icon"].draw(self.screen)
            r["owned"].draw(self.screen)
            r["rev"].draw(self.screen)
            r["buy"].draw(self.screen)
        
        


        pygame.display.flip()
    # other functions ──────────────────────────────────────────────────────────
    def save_and_exit(self):
        SaveStates.save_user(self.user)
        print("\n (づ｡◕‿‿◕｡)づ Saving user! \n") if DEBUG_MODE else None
        self.state_manager.set_state(MAIN_MENU) # go back to main menu
        
    def save(self):
        SaveStates.save_user(self.user) # save the user object

        


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

    def render_text(self, position="center", display=None): # render text inside the frect
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


    def draw(self, screen, width=None):
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
        self.font = DEFAULT_FONT
        self.user = user
        self.buttons = self.create_buttons()
        self.screen_elements = {
            "money_display": CreateFrect(300, 60, 60, 60, "PINK", id="money_display", font=self.font, font_colour="Black", display_callback=lambda: f"ATAR POINTS: {format_large_number(round(self.user.money))}")
        }
        self.last_time = pygame.time.get_ticks() / 1000  # track for dt

    def create_buttons(self):
        buttons = []

        # dynamically create 3 columns: Buy Gen, Manual Gen, Hire Manager
        padding_x = 150
        padding_y = 200
        col_width = 450
        for idx, (generator_id, prototype) in enumerate(GENERATOR_PROTOTYPES.items()): # loop through all the generators
            x = padding_x + (idx * col_width)
            # 1) Purchase generators
            # Calculate the price string for the button text
            price = format_large_number(prototype['base_price'] * (prototype['growth_rate'] ** self.user.generators.get(generator_id, Generator(generator_id, prototype['name'], prototype['base_rate'], prototype['base_price'])).amount)) 
            buttons.append(Button(
                x, padding_y + 0*200, BUTTON_WIDTH, BUTTON_HEIGHT,
                f"Buy {prototype['name']} for {price}",
                GRAY, self.font, BLACK,
                callback=lambda generator_id=generator_id: ( self.user.ensure_generator(generator_id), self.user.buy_generator(generator_id) ),
                display_callback=lambda current_gid=generator_id, 
                current_proto=prototype: f"Buy {current_proto['name']} for {format_large_number(self.user.generators[current_gid].next_price) if current_gid in self.user.generators else format_large_number(current_proto['base_price'])}"
            ))
            # 2) Manual Generate
            buttons.append(Button(
                x, padding_y + 1*60, 100, BUTTON_HEIGHT,
                f"Gen {prototype['name']}", 
                YELLOW, self.font, BLACK, 
                callback=lambda generator_id=generator_id: ( self.user.ensure_generator(generator_id), self.user.generators[generator_id].manual_generate(self.user) )
            ))
            # 3) Hire Manager
            mproto = MANAGER_PROTOTYPES[generator_id]
            buttons.append(Button( 
                x, padding_y + 2*60, 100, BUTTON_HEIGHT, 
                f"Hire {mproto['name']}", YELLOW, self.font, BLACK, 
                callback=lambda generator_id=generator_id: ( self.user.buy_manager(generator_id) ),
                display_callback=lambda generator_id=generator_id, mproto=mproto: (
                    f"Buy {mproto['name']} for {format_large_number(mproto['cost'])}"
                    if generator_id in self.user.generators and self.user.generators[generator_id].amount > 0
                    else f"Buy {mproto['name']} for {format_large_number(mproto['cost'])} (Requires {generator_id})"
                )
            ))
        return buttons
       
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                SaveStates.save_user(self.user)
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
        self.screen.blit(main_menu_background, (-300, 0)) # load background image
        
        for button in self.buttons:
            button.draw(self.screen)
        for element in self.screen_elements.values():
            element.draw(self.screen)
        self.screen.blit(williamdu, (600, 600))
        
        
        pygame.display.flip()
       