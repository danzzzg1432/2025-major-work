import pygame
from game_constants import *
import sys
# Button Class
class Button: # global button class
    def __init__(self, x, y, width, height, text, background_colour, font, text_colour):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.colour = background_colour
        self.initial_colour = background_colour
        self.font = font
        self.text_colour = text_colour

    def draw(self, screen):
        pygame.draw.rect(screen, self.colour, self.rect, border_radius=30)
        text_surf = self.font.render(self.text, True, self.text_colour)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
    
    def is_hovered(self, pos):
        return self.rect.collidepoint(pos) 
        
class Generator:
    def __init__(self, name, rate, price, level=1, amount=0):
        self.rate = rate
        self.name = name
        self.level = level
        self.amount = amount
        self.price = price
        
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
    
    def set_money(self, money):
        self.money = money
        
        
# Screens and Menus
class StateManager: # global state manager
    def __init__(self, screen):
        self.state = GAME_MENU # set initial state to main menu (for now)
        self.states = {
            MAIN_MENU: MainMenu(screen, self),
            GAME_MENU: GameMenu(screen, self),
            SETTINGS_MENU: SettingsMenu(screen, self),
            SHOP_MENU: ShopMenu(screen, self),
            LOGIN_MENU: LoginMenu(screen, self),
            REGISTER_MENU: RegisterMenu(screen, self),
            HELP_MENU: HelpMenu(screen, self),
            } 

        
    def set_state(self, new_state): # set the state of the game
        self.state = new_state
        pygame.display.set_caption(f"{GAME_TITLE} - {new_state.replace('_', ' ').title()}") # set the window title to the current state


    def get_state(self): # get the current state of the game
        return self.state
    
    # def register_state(self, state_name, state_object): # register a new state
    #     self.states[state_name] = state_object
        
    def get_state_object(self, state_name): # get the state object of a specific state (use case: returns current state object for the screen)
        return self.states.get(state_name, None)
    
    def __str__(self):
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


    def create_buttons(self):
        main_button_x = (SCREEN_WIDTH - BUTTON_WIDTH) // 2
        return [
            Button(main_button_x, 360, BUTTON_WIDTH, BUTTON_HEIGHT, "Start Game", GRAY, self.button_font, BLACK),
            Button(main_button_x, 440, BUTTON_WIDTH, BUTTON_HEIGHT, "Load Game", GRAY, self.button_font, BLACK),
            Button(main_button_x, 520, BUTTON_WIDTH, BUTTON_HEIGHT, "Settings", GRAY, self.button_font, BLACK),
            Button(main_button_x, 600, BUTTON_WIDTH, BUTTON_HEIGHT, "Quit", GRAY, self.button_font, BLACK)
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
                        if button.text == "Quit":
                            pygame.quit()
                            sys.exit()
                        elif button.text == "Start Game":
                            self.state_manager.set_state(GAME_MENU)  # Start the game
                        elif button.text == "Settings":
                            pass
                        elif button.text == "Load Game":
                            pass
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
            Button(main_button_x, 360, BUTTON_WIDTH, BUTTON_HEIGHT, "test test", "Red", self.button_font, BLACK),
            Button(main_button_x, 440, BUTTON_WIDTH, BUTTON_HEIGHT, "test test", GRAY, self.button_font, BLACK),
            Button(main_button_x, 520, BUTTON_WIDTH, BUTTON_HEIGHT, "test", GRAY, self.button_font, BLACK),
            Button(main_button_x, 600, BUTTON_WIDTH, BUTTON_HEIGHT, "go back", GRAY, self.button_font, BLACK)
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
                        if button.text == "go back": 
                            self.state_manager.set_state(MAIN_MENU)  # Go back to main menu
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

    
# class Testing:
#     def __init__(self):
#         self.buttons = self.create_buttons()
        
        
#     def create_buttons(self):
        