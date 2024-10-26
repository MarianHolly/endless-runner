import pygame
from sys import exit

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    snail_surface = text.render("Score: " + str(current_time), False, (65, 65, 65))
    score_rect = snail_surface.get_rect(center = (400, 50))
    screen.blit(snail_surface, score_rect)

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Endless Runner")
clock = pygame.time.Clock()
text = pygame.font.Font('font/Pixeltype.ttf', 42)
game_active = True
start_time = 0 

# LOADING IMAGES

sky_surface = pygame.image.load("graphics/sky.png").convert()
ground_surface = pygame.image.load("graphics/ground.png").convert()

# score_surface = text.render("Score: 0", True, (255, 255, 255))
# score_rect = score_surface.get_rect(center = (400, 50))

snail_surface = pygame.image.load("graphics/snail/snail2.png").convert_alpha()
snail_rect = snail_surface.get_rect(bottomright = (600, 300))

player_surface = pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha()
player_rect = player_surface.get_rect(midbottom = (80,300))
player_gravity = 0

# GAME LOOP

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN and player_rect.bottom >= 300:
                if player_rect.collidepoint(event.pos): 
                    player_gravity = -22
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                    player_gravity = -22
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                snail_rect.left = 800
                start_time = int(pygame.time.get_ticks() / 1000)


    if game_active:
        screen.blit(sky_surface, (0,0))
        screen.blit(ground_surface, (0,300))
        # pygame.draw.rect(screen, '#c0e8ec', score_rect)
        # pygame.draw.rect(screen, '#c0e8ec', score_rect, 10)
        # screen.blit(score_surface, score_rect)
        display_score()

        snail_rect.x -= 4
        if snail_rect.right < 0: snail_rect.left = 800
        screen.blit(snail_surface, snail_rect)

        # Player
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300: player_rect.bottom = 300
        screen.blit(player_surface, player_rect)

        # End Game
        if snail_rect.colliderect(player_rect):
            game_active = False

    else:
        screen.fill('white')

        
    pygame.display.update()
    clock.tick(60)