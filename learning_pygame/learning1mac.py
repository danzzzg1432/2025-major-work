import pygame, sys, random


pygame.init() # initialise pygame
screen = pygame.display.set_mode((800, 600)) # set the display surface 
clock=pygame.time.Clock() # capitalise the C, this initialises a clock. we do this to specify the FPS through clock.tick(60) (for 60fps)
pygame.display.set_caption("Idle Tutor Tycoon") # set name of the window
olivia_monkey_font = pygame.font.Font(None, 50) # initialise font


# test_surface = pygame.Surface((900,450)) # capitalise the S
# test_surface.fill('Green') # fill the test surface object green.

forest = pygame.image.load('learning_pygame/1.jpg').convert_alpha() # load an image from a directory
forest = pygame.transform.smoothscale(forest, (1920,1080)) # resize the image
olivia = pygame.image.load('learning_pygame/Monkey-Selfie.png').convert_alpha()
olivia = pygame.transform.scale(olivia,(400,200))
text_surface = olivia_monkey_font.render("Credit: Olivia, my donkeymonkey sister, in her natural habitat", True, 'black') # initialise text object with (text, anti-aliasing, color)

olivia_surf = pygame.image.load('learning_pygame/Monkey-Selfie.png').convert_alpha() # initialise the surface again
olivia_moveable_rect = olivia.get_rect(bottomleft = (5,10))
olivia_rect = olivia_surf.get_rect() #(position, (x,y)) # initialise a float rectangle (Frect instead of rect, so you can specify coordinates in terms of a) that encompasses the surface 
while True:
    for event in pygame.event.get(): # for loop that runs over ALL user inputs. exits when X is pressed
        if event.type == pygame.QUIT:
            sys.exit()
        # if event.type == pygame.MOUSE -> checks for mouse inputs.
        # if event.type == pygame.K => checks for the input key.
    mousepos = pygame.mouse.get_pos()

    screen.blit(forest) # draws our test surface onto our display surfa ce called screen, at a position of 200,100
    screen.blit(olivia, mousepos)
    screen.blit(text_surface, (500,280))
    # screen.blit(olivia_surf, olivia_rect) # initialise our surface inside the rectangle
    # olivia_rect.right += 1
    # if olivia_rect.right > 1920: # simple logic to move rect back to original position after it exits the screen.
    #     olivia_rect.left = 0

    # olivia_rect.colliderect(other rect ) checks for rectangle collision with other rectangle. returns 0 and 1 respectively for true and false
        # use scenario: mousepos = pygame.mouse.get_pos()  
        #               if rect1.collidepoint(mousepos):
                           # etc
    # rectangleobject.collidepoint((x,y)) -> checks for a rectangle collision at (x,y)



    clock.tick(60) # instructs our game to only run at 60fps, or essentially "refresh" the game at 60 times a second
    pygame.display.flip() # updates the frame
    print('updated')
     