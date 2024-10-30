import pygame, sys


# Initialise Pygame
pygame.init()

# Initialise the screen
screen = pygame.display.set_mode((800, 600))

# Main loop:
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # Basically, if the red x is pressed it will exit out of the program
            sys.exit()

    
