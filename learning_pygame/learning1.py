import pygame, sys


pygame.init() # initialise pygame
screen = pygame.display.set_mode((1920, 1080)) # set the display surface 
clock=pygame.time.Clock() # capitalise the C, this initialises a clock. we do this to specify the FPS through clock.tick(60) (for 60fps)
pygame.display.set_caption("Idle Tutor Tycoon") # set name of the window
olivia_monkey_font = pygame.font.Font(None, 50) # initialise font


# test_surface = pygame.Surface((900,450)) # capitalise the S
# test_surface.fill('Green') # fill the test surface object green.

forest = pygame.image.load('learning_pygame\\1.jpg').convert_alpha() # load an image from a directory
forest = pygame.transform.smoothscale(forest, (1600,900)) # resize the image
olivia = pygame.image.load('learning_pygame\\Monkey-Selfie.png').convert_alpha()
olivia = pygame.transform.scale(olivia,(400,200))
text_surface = olivia_monkey_font.render("Credit: Olivia, my donkeymonkey sister, in her natural habitat", True, 'black') # initialise text object with (text, anti-aliasing, color)


while True:
    for event in pygame.event.get(): # for loop that runs over ALL user inputs. exits when X is pressed
        if event.type == pygame.QUIT:
            sys.exit()
    

    screen.blit(forest, (160,90)) # draws our test surface onto our display surface called screen, at a position of 200,100
    screen.blit(olivia, (1280, 360))
    screen.blit(text_surface, (500,280))
    pygame.display.update() # updates the frame
    clock.tick(60) # tells our game to only run at 60fps
    print('updated')
     