import pygame

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Endless Runner")
clock = pygame.time.Clock()
text = pygame.font.Font('font/Pixeltype.ttf', 42)

# LOADING IMAGES

sky_surface = pygame.image.load("graphics/sky.png").convert()
ground_surface = pygame.image.load("graphics/ground.png").convert()

score_surface = text.render("Score: 0", True, (255, 255, 255))
score_rect = score_surface.get_rect(center = (300, 50))

snail_surface = pygame.image.load("graphics/snail/snail2.png").convert_alpha()
snail_rect = snail_surface.get_rect(bottomright = (600, 300))

player_surface = pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha()
player_rect = player_surface.get_rect(midbottom = (80,300))

# GAME LOOP

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    screen.blit(sky_surface, (0,0))
    screen.blit(ground_surface, (0,300))
    screen.blit(score_surface, score_rect)

    snail_rect.x -= 4
    if snail_rect.right < 0: snail_rect.left = 800
    screen.blit(snail_surface, snail_rect)
    screen.blit(player_surface, player_rect)

    pygame.display.update()
    clock.tick(90)