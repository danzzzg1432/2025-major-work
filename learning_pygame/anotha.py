import pygame, sys, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
pygame.init()

# -------
fps = pygame.time.Clock()
player_gravity = 0

# initialising images
screen = pygame.display.set_mode((800,400))
background_img = pygame.image.load('1.jpg').convert_alpha()
background_img = pygame.transform.smoothscale(background_img, (800,400))
ground = pygame.image.load('graphics/ground.png').convert_alpha()
player1 = pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha()
snail = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
font = pygame.font.Font("font/Pixeltype.ttf", 50)
score_surf = font.render("Score: 0", False, 'Black')
# player2 = pygame.image.load("graphics/Player/player_walk_2.png")



# initialising variables
ground_rect = ground.get_frect(topleft = (0,300))
player_rect = player1.get_frect(midbottom = (100,300))
snail_rect = snail.get_frect(bottomleft = (800, 300))
score_rect = score_surf.get_rect(center = (400, 50))

# game loop
while True:
    for i in pygame.event.get():
        if i.type == pygame.QUIT: sys.exit()
        # if i.type == pygame.K_ESCAPE: sys.exit()
        if i.type == pygame.KEYDOWN and i.key == pygame.K_ESCAPE: sys.exit()
        if i.type == pygame.KEYDOWN and i.key == pygame.K_SPACE: player_gravity = -20
        


    
    screen.blit(background_img,(0,-100))
    screen.blit(ground, ground_rect)

    player_gravity += 1
    screen.blit(player1, player_rect)
    player_rect.y += player_gravity
    if player_rect.bottom >= 300: player_rect.bottom = 300
        

    screen.blit(snail, snail_rect)
    pygame.draw.rect(screen, "Pink", score_rect)
    pygame.draw.rect(screen, 'Pink', score_rect, 15, 4)
    screen.blit(score_surf, score_rect)
    
    snail_rect.x -= 8.88888
    if snail_rect.right < 0: snail_rect.left = 800

    pygame.key.get_pressed() # essentially an object that checks over ALL the keys and sees if any are being pressed
    # however, to actually use it, you must create a dictionary first and you can sorta "call" the key.
    # keys = pygame.key.get_pressed()
    # if keys[pygame.K_SPACE]:

    # if snail_rect.colliderect(player_rect): sys.exit()
    pygame.display.flip()
    fps.tick(60)