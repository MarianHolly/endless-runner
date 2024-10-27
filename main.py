import pygame
from sys import exit
from random import randint

# function to display the score
def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    snail_surface = text.render("Score: " + str(current_time), False, (65, 65, 65))
    score_rect = snail_surface.get_rect(center = (400, 50))
    screen.blit(snail_surface, score_rect)
    return current_time

# function to move the obstacles
def obstacle_movement(obstacle_list):
    if obstacle_rect_list:
        for obstacle_rect in obstacle_rect_list:
            obstacle_rect.x -= 5

            if obstacle_rect.bottom == 300: screen.blit(snail_surface, obstacle_rect)
            else: screen.blit(fly_surface, obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return obstacle_rect_list
    else: return []

# function to check for collisions
def collisions(player,obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect): return False
    return True

# function to animate the player
def player_animation():
    global player_index, player_surface
    if player_rect.bottom < 300:
        player_surface = player_jump
    else:
        player_index += 0.1
        if player_index > len(player_walk): player_index = 0
        player_surface = player_walk[int(player_index)]
    # walk animation - if player is on floor
    # jump surface when player is not on floor

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Endless Runner")
clock = pygame.time.Clock()
text = pygame.font.Font('font/Pixeltype.ttf', 42)
game_active = False
start_time = 0 
score = 0

# IMAGES
sky_surface = pygame.image.load("graphics/sky.png").convert()
ground_surface = pygame.image.load("graphics/ground.png").convert()

# OBSTACLES
snail_frame_1 = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
snail_frame_2 = pygame.image.load("graphics/snail/snail2.png").convert_alpha()
snail_framer = [snail_frame_1, snail_frame_2]
snail_index = 0
snail_surface = snail_framer[snail_index]

fly_frame_1 = pygame.image.load("graphics/fly/fly1.png").convert_alpha()
fly_frame_2 = pygame.image.load("graphics/fly/fly2.png").convert_alpha()
fly_frames = [fly_frame_1, fly_frame_2]
fly_index = 0
fly_surface = fly_frames[fly_index]

obstacle_rect_list = []

# PLAYER
player_walk_1 = pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha()
player_walk_2 = pygame.image.load("graphics/Player/player_walk_2.png").convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player_jump = pygame.image.load("graphics/Player/jump.png").convert_alpha()

player_surface = player_walk[player_index]
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

# Timers
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)


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

            if event.type == obstacle_timer:
                if randint(0,2):
                    obstacle_rect_list.append(snail_surface.get_rect(bottomright = (randint(900, 1100), 300)))
                else:
                    obstacle_rect_list.append(fly_surface.get_rect(bottomright = (randint(900, 1100), 210)))

            if event.type == snail_animation_timer:
              if snail_index == 0: snail_index = 1
              else: snail_index = 0
              snail_surface = snail_framer[snail_index]

            if event.type == fly_animation_timer:
                if fly_index == len(fly_frames) - 1: fly_index = 0
                else: fly_index += 1
                fly_surface = fly_frames[fly_index]

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)

    if game_active:
        screen.blit(sky_surface, (0,0))
        screen.blit(ground_surface, (0,300))
        score = display_score()

        # Player
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300: player_rect.bottom = 300
        player_animation()
        screen.blit(player_surface, player_rect)

        # Obstacle Movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # End Game
        game_active = collisions(player_rect, obstacle_rect_list)

    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)
        obstacle_rect_list.clear()
        # player_rect.bottom = (80,300)
        player_gravity = 0

        score_message = text.render(f"Your Score: {score}", False, (111, 196, 169))
        score_rect = score_message.get_rect(center = (400, 360))

        screen.blit(game_name, game_name_rect)
        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:    
            screen.blit(score_message, score_rect)

    
    pygame.display.update()
    clock.tick(60)