import pygame
import sys

# australian english please.
pygame.init() # initialise pygame
screen = pygame.display.set_mode((1920, 1080))
clock=pygame.time.Clock()
pygame.display.set_caption("Idle Tutor Tycoon")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    pygame.display.update()
    