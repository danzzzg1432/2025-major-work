import pygame
import sys

# Initialize Pygame
pygame.init()
print("Pygame initialized")

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Isometric Grid")
print("Screen initialized")

# Colors
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)

# Grid parameters
GRID_WIDTH, GRID_HEIGHT = 100, 100
TILE_WIDTH, TILE_HEIGHT = 64, 32

def to_isometric(x, y):
    iso_x = (x - y) * (TILE_WIDTH // 2)
    iso_y = (x + y) * (TILE_HEIGHT // 2)
    return iso_x, iso_y

def draw_grid():
    print("Drawing grid")
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            iso_x, iso_y = to_isometric(x, y)
            pygame.draw.polygon(screen, GRAY, [
                (iso_x + WIDTH // 2, iso_y + HEIGHT // 4),
                (iso_x + WIDTH // 2 + TILE_WIDTH // 2, iso_y + HEIGHT // 4 + TILE_HEIGHT // 2),
                (iso_x + WIDTH // 2, iso_y + HEIGHT // 4 + TILE_HEIGHT),
                (iso_x + WIDTH // 2 - TILE_WIDTH // 2, iso_y + HEIGHT // 4 + TILE_HEIGHT // 2)
            ], 1)

def main():
    print("Starting main loop")
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Quitting")
                pygame.quit()
                sys.exit()

        screen.fill(WHITE)
        draw_grid()
        pygame.display.flip()
        clock.tick(60)
        print("Frame updated")

if __name__ == "__main__":
    print("Calling main()")
    main()