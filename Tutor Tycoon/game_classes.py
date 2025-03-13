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
class Frect:
    def __init__(self, x, y , width, height, colour, border_radius=0, border_width=0, border_colour=None):
        self.frect = pygame.FRect(x, y, width, height)
        self.colour = colour
        self.border_radius = border_radius
        self.border_width = border_width
        self.border_colour = border_colour
        
        






class StateManager: # global state manager
    def __init__(self):
        self.state = MAIN_MENU

    def set_state(self, new_state):
        self.state = new_state

    def get_state(self):
        return self.state


# MAIN MENU 
class MainMenu:
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
            Button(main_button_x, 360, BUTTON_WIDTH, BUTTON_HEIGHT, "Start Game", "Red", self.button_font, BLACK),
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
                            self.state_manager.set_state(GAME_RUNNING)
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
        self.screen.blit(main_menu_background) # load background image, though will be replaced soon by the Frect and SurfFrect class
        self.render_title()
        for button in self.buttons:
            button.draw(self.screen)
        pygame.display.flip()



# MAIN GAME
class MainGame:
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

    def render(self):
        self.screen.fill(BLACK)  # Set background colour (Replace with actual background image later)
        self.screen.blit(idle_tutor_tycoon_logo) # render background, redundant very soon
        self.render_title()
        for button in self.buttons:
            button.draw(self.screen)
        pygame.display.flip()




class Shop:
    pass