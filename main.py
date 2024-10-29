import pygame  # Main game development library
from sys import exit  # Used to exit the game cleanly
from random import randint, choice  # Used for random obstacle spawning

class Player(pygame.sprite.Sprite):
    '''Player class represents the character that the user controls'''
    def __init__(self):
        # Initialize the parent Sprite class
        super().__init__()
        
        # Load two images for walking animation
        # convert_alpha() makes the images more efficient to display
        player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]  # Store both walking frames in a list
        self.player_index = 0  # Used to keep track of which walking frame to show
        
        # Load jumping image
        self.player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()

        # Start with the first walking frame
        self.image = self.player_walk[self.player_index]
        # Create a rectangle for the player (used for position and collisions)
        # midbottom=(80,300) places the player 80 pixels from left, 300 pixels from top
        self.rect = self.image.get_rect(midbottom = (80,300))
        self.gravity = 0  # Used for jumping physics

        # Load jump sound and set its volume
        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.5)  # 50% volume

    def player_input(self):
        # Check what keys are being pressed
        keys = pygame.key.get_pressed()
        # If space is pressed AND player is on the ground (300 is ground level)
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20  # Negative gravity makes player go up
            self.jump_sound.play()  # Play jump sound effect

    def apply_gravity(self):
        # Gravity increases over time (makes jumping feel more realistic)
        self.gravity += 1
        # Move player based on gravity
        self.rect.y += self.gravity
        # If player hits the ground, stop them from falling further
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        # If player is in the air (below ground level)
        if self.rect.bottom < 300:
            self.image = self.player_jump  # Show jumping image
        else:
            # If on ground, cycle between walking frames
            self.player_index += 0.1  # Slowly increase the index
            # If we go past the end of our walking frames, start over
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        # Run all player updates each frame
        self.player_input()  # Check for player input
        self.apply_gravity()  # Apply gravity effects
        self.animation_state()  # Update animations

class Obstacle(pygame.sprite.Sprite):
    '''Obstacle class represents enemies (snails and flies) that the player must avoid'''
    def __init__(self, type):
        super().__init__()
        
        # Set up different obstacles based on type
        if type == 'fly':
            # Load fly animation frames
            fly_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
            fly_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 210  # Flies appear higher in the air
        else:
            # Load snail animation frames
            snail_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 300  # Snails appear on the ground

        # Set up initial animation state
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        # Place obstacle randomly between 900-1100 pixels from left
        self.rect = self.image.get_rect(midbottom = (randint(900,1100), y_pos))

    def animation_state(self):
        # Cycle through animation frames
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()  # Update animation
        self.rect.x -= 6  # Move obstacle to the left
        self.destroy()  # Check if obstacle should be destroyed

    def destroy(self):
        # Remove obstacle if it moves too far left (off screen)
        if self.rect.x <= -100:
            self.kill()

# Calculate and display the score (based on survival time)
def display_score():
    # Get time in seconds since game started
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    # Create text surface with score
    score_surf = test_font.render(f'Score: {current_time}', False, (64,64,64))
    score_rect = score_surf.get_rect(center = (400,50))
    # Draw score on screen
    screen.blit(score_surf, score_rect)
    return current_time

# Check if player has hit any obstacles
def collision_sprite():
    # spritecollide checks if player has hit any obstacle in obstacle_group
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()  # Remove all obstacles
        return False  # Game over
    return True  # Game continues

# Initialize Pygame and set up the game window
pygame.init()
screen = pygame.display.set_mode((800,400))  # Create 800x400 window
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()  # Used to control game speed
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)  # Load custom font
game_active = False  # Start at menu screen
start_time = 0
score = 0

# Load and start background music (loops forever)
bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.play(loops = -1)

# Create sprite groups (used for drawing and collision detection)
player = pygame.sprite.GroupSingle()  # Group for single player
player.add(Player())  # Add player to group
obstacle_group = pygame.sprite.Group()  # Group for multiple obstacles

# Load background images
sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

# Set up intro/menu screen
player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)  # Scale up by 2x
player_stand_rect = player_stand.get_rect(center = (400,200))

# Create text for menu screen
game_name = test_font.render('Pixel Runner', False, (111,196,169))
game_name_rect = game_name.get_rect(center = (400,80))
game_message = test_font.render('Press space to run', False, (111,196,169))
game_message_rect = game_message.get_rect(center = (400,330))

# Set up timer for spawning obstacles
obstacle_timer = pygame.USEREVENT + 1  # Create custom event
pygame.time.set_timer(obstacle_timer, 1500)  # Trigger every 1.5 seconds

# Main game loop
while True:
    # Event handling loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # If window is closed
            pygame.quit()
            exit()

        if game_active:
            # During gameplay, spawn obstacles on timer
            if event.type == obstacle_timer:
                # More likely to spawn snails than flies
                obstacle_group.add(Obstacle(choice(['fly','snail','snail','snail'])))
        
        else:
            # At menu, start game when space is pressed
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)

    # Game state handling
    if game_active:
        # Draw game screen
        screen.blit(sky_surface,(0,0))  # Draw sky
        screen.blit(ground_surface,(0,300))  # Draw ground
        score = display_score()  # Show and update score
        
        # Update and draw player
        player.draw(screen)
        player.update()

        # Update and draw obstacles
        obstacle_group.draw(screen)
        obstacle_group.update()

        # Check for collisions (ends game if collision occurs)
        game_active = collision_sprite()
        
    else:
        # Draw menu screen
        screen.fill((94,129,162))  # Blue background
        screen.blit(player_stand, player_stand_rect)  # Show player image

        # Show score if game ended, or start message if new game
        score_message = test_font.render(f'Your score: {score}', False, (111,196,169))
        score_message_rect = score_message.get_rect(center = (400,330))
        screen.blit(game_name, game_name_rect)

        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)

    # Update the display and maintain 60 FPS
    pygame.display.update()
    clock.tick(60)