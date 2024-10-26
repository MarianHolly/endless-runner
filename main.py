import pygame
from sys import exit

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    snail_surface = text.render("Score: " + str(current_time), False, (65, 65, 65))
    score_rect = snail_surface.get_rect(center = (400, 50))
    screen.blit(snail_surface, score_rect)
    return current_time

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Endless Runner")
clock = pygame.time.Clock()
text = pygame.font.Font('font/Pixeltype.ttf', 42)
game_active = False
start_time = 0 
score = 0

# LOADING IMAGES

sky_surface = pygame.image.load("graphics/sky.png").convert()
ground_surface = pygame.image.load("graphics/ground.png").convert()

# score_surface = text.render("Score: 0", True, (255, 255, 255))
# score_rect = score_surface.get_rect(center = (400, 50))

snail_surface = pygame.image.load("graphics/snail/snail2.png").convert_alpha()
snail_rect = snail_surface.get_rect(bottomright = (600, 300))

# PLAYER
player_surface = pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha()
player_rect = player_surface.get_rect(midbottom = (80,300))
player_gravity = 0

# Intro Screen
player_stand = pygame.image.load("graphics/Player/player_stand.png").convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center = (400,200))
game_name = text.render("Endless Runner", True, (111, 196, 169))
game_name_rect = game_name.get_rect(center = (400, 100))
game_message = text.render("Press Space to Start", False, (111, 196, 169))
game_message_rect = game_message.get_rect(center = (400, 360))

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
        score = display_score()

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
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)

        score_message = text.render(f"Your Score: {score}", False, (111, 196, 169))
        score_rect = score_message.get_rect(center = (400, 360))

        screen.blit(game_name, game_name_rect)
        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:    
            screen.blit(score_message, score_rect)
        

    
    pygame.display.update()
    clock.tick(60)