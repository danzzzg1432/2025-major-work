import pygame
from game_constants import *
import sys
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
    def __init__(self, name, rate, price, level=1, amount=0):
        self.rate = rate
        self.name = name
        self.price = price
        self.level = level
        self.amount = amount
        
    def increase_amount(self):
        self.amount += 1
        
    def generate_money(self):
        return (self.rate * self.amount * self.level)/60 # money per second as fps is 60, so divide by 60 to get per second as it runs 60 times a second

    
    
class User:
    def __init__(self, money=0):
        self.generators = {}
        self.money = money
    
    def add_generator(self, generator): # perhaps later include a feature to multiple-buy generators -> add button in the shop menu which switches from 1x, 10x, 100x, then buy that amount probably by passing through the amount in this class
        if generator.name not in self.generators: # check if generator already exists
            self.generators[generator.name] = generator
        generator.increase_amount()
        
    def get_money(self):
        return self.money
    
    def set_money(self, new_money):
        self.money = new_money
    
# Screens and Menus
class StateManager: # global state manager
    def __init__(self, screen):
        self.state = TESTING # set initial state to main menu (for now)
        self.states = {
            MAIN_MENU: MainMenu(screen, self),
            GAME_MENU: GameMenu(screen, self),
            SETTINGS_MENU: SettingsMenu(screen, self),
            SHOP_MENU: ShopMenu(screen, self),
            LOGIN_MENU: LoginMenu(screen, self),
            REGISTER_MENU: RegisterMenu(screen, self),
            HELP_MENU: HelpMenu(screen, self),
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
        return f"Current States: {self.state}, States: {state_names}" # debugging line
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
            Button(main_button_x, 600, BUTTON_WIDTH, BUTTON_HEIGHT, "go back", GRAY, self.button_font, BLACK,callback=lambda: self.state_manager.set_state(MAIN_MENU)) # lambda creates a temp anonymous function
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
class ShopMenu: # Shop menu class
    def __init__(self, screen, state_manager):
        self.screen = screen
        self.state_manager = state_manager

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def update(self):
        pass

    def render(self):
        self.screen.fill(GRAY)
        pygame.display.flip()    
class SettingsMenu: # Settings menu class
    def __init__(self, screen, state_manager):
        self.screen = screen
        self.state_manager = state_manager

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def update(self):
        pass

    def render(self):
        self.screen.fill(GRAY)
        pygame.display.flip()   
class LoginMenu: # Login menu class
    def __init__(self, screen, state_manager):
        self.screen = screen
        self.state_manager = state_manager

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def update(self):
        pass

    def render(self):
        self.screen.fill(GRAY)
        pygame.display.flip()
class RegisterMenu: # Register menu class
    def __init__(self, screen, state_manager):
        self.screen = screen
        self.state_manager = state_manager

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def update(self):
        pass

    def render(self):
        self.screen.fill(GRAY)
        pygame.display.flip()         
class HelpMenu: # Help menu class
    def __init__(self, screen, state_manager):
        self.screen = screen
        self.state_manager = state_manager

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def update(self):
        pass

    def render(self):
        self.screen.fill(GRAY)
        pygame.display.flip()

class CreateFrect: # include method for adding fonts.
    def __init__(self, x, y, width, height, bg_colour, display=None, font=None, font_colour=None, image_path=None, id=None):
        self.frect = pygame.FRect(x, y, width, height)
        self.bg_colour = bg_colour
        self.image = None
        self.id = id
        self.font = font
        self.font_colour = font_colour
        self.display = display

        if image_path:  # Load and scale image if provided
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (width, height))

    def render_text(self, display=None): # default is center
        # render text onto surface
        if self.font and self.font_colour:
            display = display if display is not None else self.display
            text_surface = self.font.render(str(display), True, self.font_colour)
            text_rect = text_surface.get_rect(center=self.frect.center)
            return text_surface, text_rect
        return None, None

    def draw(self, screen):
        # draw rect and render images
        if self.image:
            screen.blit(self.image, self.frect)
        else:
            pygame.draw.rect(screen, self.bg_colour, self.frect)

        # Render text if applicable
        text_surface, text_rect = self.render_text()
        if text_surface and text_rect:
            screen.blit(text_surface, text_rect)
            
            
# testing generator class with a temp menu + sort of randomly testing stuff too
user = User(1000) 
depression = Generator("Depressi")
class Testing:
    def __init__(self, screen, user, state_manager):
        self.screen = screen
        self.state_manager = state_manager
        self.font = pygame.font.Font(LOGO_FONT, MAIN_MENU_BUTTON_SIZE)
        self.buttons = self.create_buttons()
        self.user = user
        self.screen_elements = {
            "money_display": CreateFrect(200, 200, 200, 200, "Blue", id="money_display",)
        }
    
    def create_buttons(self):
        return [
            Button(500, 360, BUTTON_WIDTH, BUTTON_HEIGHT, "GENERATE MONEY!!!", GRAY, self.button_font, BLACK, callback=None),
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

    def render(self):
        self.screen.fill(WHITE)  # Set background colour
        self.screen.blit(main_menu_background) # load background image
        
        for button in self.buttons:
            button.draw(self.screen)
        for element in self.screen_elements.values():
            element.draw(self.screen)
        user_money = self.font.render(str(user.money), True, "Black")
        
        money_display_rect = self.screen_elements.get("money_display").frect # TODO FOR TOMORROW: get the rect of the money display and render the money in the middle of it, and create some method or function to update the money display rect in the screen_elements dict, so that it can be used in other menus too.
        user_money_rect = user_money.get_rect(center=money_display_rect.center)
        self.screen.blit(user_money, user_money_rect)  # render the money display centered in the rect
        
        
        pygame.display.flip()