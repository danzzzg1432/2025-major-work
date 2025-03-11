import pygame
import sys
from game_constants import *  # Import all constants
from game_classes import *

# Initialise pygame
pygame.init()

# Screen dimensions
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(f"{GAME_TITLE} - Main Menu")

# Importing fonts, none as of right now
font = pygame.font.Font(None, DEFAULT_FONT_SIZE)

# Background (haven't designed yet)
# background = pygame.image.load(f"{IMAGES_DIR}/background.png")

# Define buttons based on storyboard layout

main_button_x = (SCREEN_WIDTH-BUTTON_WIDTH) // 2
buttons = [
    Button(main_button_x, 360, BUTTON_WIDTH, BUTTON_HEIGHT, "Start Game", GRAY, font, BLACK),
    Button(main_button_x, 440, BUTTON_WIDTH, BUTTON_HEIGHT, "Load Game", GRAY, font, BLACK),
    Button(main_button_x, 520, BUTTON_WIDTH, BUTTON_HEIGHT, "Settings", GRAY, font, BLACK),
    Button(main_button_x, 600, BUTTON_WIDTH, BUTTON_HEIGHT, "Quit", GRAY, font, BLACK)
]

# Main loop
game_state = MAIN_MENU
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(WHITE)  # Set background colour (Replace with actual background image later) 
    
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for button in buttons:
                if button.is_hovered(mouse_pos):
                    if button.text == "Quit":
                        running = False
                    # other buttons will be added later
    
    # Draw buttons and change colour on hover
    for button in buttons:
        if button.is_hovered(mouse_pos):
            button.color = DARK_GRAY
        else:
            button.color = GRAY
        button.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)  # Control game speed

pygame.quit()