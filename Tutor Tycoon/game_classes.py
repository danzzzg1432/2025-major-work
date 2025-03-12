import pygame
from game_constants import *
import sys

# Colours (duplicated here for convenience when creating objects)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (150, 150, 150)

# Button Class
class Button:
    def __init__(self, x, y, width, height, text, colour, font, text_colour):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.colour = colour
        self.font = font
        self.text_colour = text_colour

    def draw(self, screen):
        pygame.draw.rect(screen, self.colour, self.rect, border_radius=10)
        text_surf = self.font.render(self.text, True, self.text_colour)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
    
    def is_hovered(self, pos):
        return self.rect.collidepoint(pos)

# # Login Screen Class
# class LoginScreen:
#     def __init__(self, screen, font):
#         self.screen = screen
#         self.font = font
#         self.title_font = pygame.font.Font(None, MAIN_MENU_LOGO_SIZE)
#         self.buttons = self.create_buttons()
#     pass


# Main Menu Class
class MainMenu:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.title_font = pygame.font.Font(None, MAIN_MENU_LOGO_SIZE)
        self.buttons = self.create_buttons()

    def render_title(self):
        title_surf = self.title_font.render(GAME_TITLE.upper(), True, BLACK)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 200))
        self.screen.blit(title_surf, title_rect)


    def create_buttons(self):
        main_button_x = (SCREEN_WIDTH - BUTTON_WIDTH) // 2
        return [
            Button(main_button_x, 360, BUTTON_WIDTH, BUTTON_HEIGHT, "Start Game", GRAY, self.font, BLACK),
            Button(main_button_x, 440, BUTTON_WIDTH, BUTTON_HEIGHT, "Load Game", GRAY, self.font, BLACK),
            Button(main_button_x, 520, BUTTON_WIDTH, BUTTON_HEIGHT, "Settings", GRAY, self.font, BLACK),
            Button(main_button_x, 600, BUTTON_WIDTH, BUTTON_HEIGHT, "Quit", GRAY, self.font, BLACK)
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
        return True

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            if button.is_hovered(mouse_pos):
                button.colour = DARK_GRAY
            else:
                button.colour = GRAY

    def render(self):
        self.screen.fill(WHITE)  # Set background colour (Replace with actual background image later)
        self.screen.blit(background)
        self.render_title()
        for button in self.buttons:
            button.draw(self.screen)
        pygame.display.flip()

# Shop Class

# class ShopMenu:
#     def __init__(self, screen, font):
#         self.screen = screen
#         self.font = font
#         self.title_font = pygame.font.Font(None, MAIN_MENU_LOGO_SIZE)
#         self.buttons = self.create_buttons()
#     pass

