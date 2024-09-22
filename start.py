import pygame
import pygame_gui
import random
import sys

pygame.init()

#General Variables
window_size = (600, 400)
background_img = pygame.image.load("assets/starsbg.png")
pygame.display.set_caption("$pace Tycoon!")
screen = pygame.display.set_mode(window_size)
manager = pygame_gui.UIManager(window_size)

# Define colors (R, G, B) - space background and asteroid colors
BLACK = (0, 0, 0)
GRAY = (169, 169, 169)
RED = (255, 255, 0)

#Start Button
start_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((screen.get_width()//2-75, 150), (150, 100)),
    text='Press to START',
    manager=manager, 
)


#create characters
players = {
            "player1": [
                pygame.image.load("assets/player1.png"),
                pygame.transform.scale_by(pygame.image.load("assets/player1.png"), (2))],
            "player2": [
                pygame.image.load("assets/player2.png"),
                pygame.transform.scale_by(pygame.image.load("assets/player2.png"), (2))],
            "player3": [
                pygame.image.load("assets/player3.png"),
                pygame.transform.scale_by(pygame.image.load("assets/player3.png"), (2))],
            "player4": [
                pygame.image.load("assets/player4.png"),
                pygame.transform.scale_by(pygame.image.load("assets/player4.png"), (2))],
            }

#Rocket Management
# Set player properties (spaceship)
player_width = 70
player_height = 100
player_x = window_size[0] // 2 - player_width // 2
player_y = window_size[1] - player_height - 10
player_speed = 7

# Load spaceship image
spaceship_img = pygame.image.load("assets/rocket.png")  # You need to have this image
spaceship_img = pygame.transform.scale(spaceship_img, (player_width, player_height))

asteroid_img = pygame.image.load("assets/asteroid-.png")
star_img = pygame.image.load("assets/star2.png")
jupiter_img = pygame.image.load("assets/jupiter.png")

jupiter_appears = False
jupiter_x = window_size[0] // 2 - 100
jupiter_y = -150 # so that we offscreen

# Set initial obstacle properties (asteroids)
asteroid_min_size = 70
asteroid_max_size = 100
asteroid_speed = 5
asteroid_list = []
initial_spawn_time = 1000  # in milliseconds

star_min_size = 40
star_max_size = 80
star_speed = 5
star_list = []
spawn_time = 1000
spawn_time_dec = 30
min_spawn = 30

# Speed and spawn timing variables for increasing difficulty
asteroid_speed_increment = 0.1
asteroid_spawn_time = initial_spawn_time
spawn_time_decrement = 20  # Reduce spawn time gradually
min_spawn_time = 300  # Minimum possible spawn time


# Game clock and asteroid timer
clock = pygame.time.Clock()
pygame.time.set_timer(pygame.USEREVENT, asteroid_spawn_time)
pygame.time.set_timer(pygame.USEREVENT, spawn_time)

def spawn_star():
    star_width = random.randint(star_min_size, star_max_size)
    star_height = random.randint(star_min_size, star_max_size)
    star_x = random.randint(0, window_size[0] - star_max_size)
    star_y = -star_height
    star_list.append([star_x, star_y, star_width, star_height])

# Function to spawn a new asteroid with random size
def spawn_asteroid():
    asteroid_width = random.randint(asteroid_min_size, asteroid_max_size)
    asteroid_height = random.randint(asteroid_min_size, asteroid_max_size)
    asteroid_x = random.randint(0, window_size[0] - asteroid_width)
    asteroid_y = -asteroid_height
    asteroid_list.append([asteroid_x, asteroid_y, asteroid_width, asteroid_height])

# Function to update asteroid positions and remove those that go off-screen
def update_asteroids():
    global asteroid_speed
    for asteroid in asteroid_list:
        asteroid[1] += asteroid_speed
        if asteroid[1] > window_size[1]:
            asteroid_list.remove(asteroid)

def update_stars():
    global star_speed
    for star in star_list:
        star[1] += star_speed
        if star[1] > window_size[1]:
            star_list.remove(star)

# Function to detect collision
def check_collision(player_rect, asteroid_list):
    for asteroid in asteroid_list:
        asteroid_rect = pygame.Rect(asteroid[0], asteroid[1], asteroid[2], asteroid[3])
        if player_rect.colliderect(asteroid_rect):
            return True
    return False

def check_star(player_rect, star_list):
    for star in star_list:
        star_rect = pygame.Rect(star[0], star[1], star[2], star[3])
        if player_rect.colliderect(star_rect):
            return True
    return False

score = 10000000
font = pygame.font.Font(None, 28)
game_over = False
ai_score_calculated = False

#Game Management
running = True
current_screen = "start_screen"

while running:
    time_delta = clock.tick(60) / 1000.0 
    keys = pygame.key.get_pressed()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.USEREVENT:
            spawn_asteroid()
            spawn_star()
            # Speed up asteroid movement gradually
            asteroid_speed += asteroid_speed_increment
            # Decrease time between asteroid spawns (with a minimum limit)
            if asteroid_spawn_time > min_spawn_time:
                asteroid_spawn_time -= spawn_time_decrement
                pygame.time.set_timer(pygame.USEREVENT, asteroid_spawn_time)
        
        if event.type == pygame.KEYDOWN:
        # Check space key press only once per event
            if event.key == pygame.K_SPACE:
                if current_screen == "story_screen":
                    current_screen = "instructions_screen"
                elif current_screen == "instructions_screen":
                    current_screen = "gameplay"


        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == start_button:
                start_button.hide()
                current_screen = "choose_player_screen"
        
        manager.process_events(event)

    if pygame.mouse.get_pressed()[0] and current_screen == "choose_player_screen":
        current_screen = "story_screen"

    manager.update(time_delta)
    if current_screen == "gameplay":
        # Movement control (spaceship movement)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_x -= player_speed
        if keys[pygame.K_RIGHT]:
            player_x += player_speed
        if keys[pygame.K_UP]:
            player_y -= player_speed
        if keys[pygame.K_DOWN]:
            player_y += player_speed

        # Ensure player stays within the window boundaries
        if player_x < 0:
            player_x = 0
        if player_x > window_size[0] - player_width:
            player_x = window_size[0] - player_width
        if player_y < 0:
            player_y = 0
        if player_y > window_size[1] - player_height:
            player_y = window_size[1] - player_height

        # Update asteroid positions
        update_asteroids()
        update_stars()

        # Check for collisions (game over if spaceship hits an asteroid)
        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
        if check_collision(player_rect, asteroid_list) and not game_over:
            score -= 10

        if check_star(player_rect, star_list) and not game_over:
            score += 100

        if score > 10100000 and not jupiter_appears:
            jupiter_appears = True

        if jupiter_appears and player_y > 0:
            player_y -= player_speed / 2

    # Draw Screens
    if current_screen == "start_screen":
        screen.blit(background_img, (0, 0))
        manager.draw_ui(screen)
    elif current_screen == "choose_player_screen":
        screen.blit(background_img, (0, 0))
        choose_player_x = 5
        choose_player_y = 50
        for player in players.values():
             screen.blit(player[0], (choose_player_x, choose_player_y))
             choose_player_x += 125
        manager.draw_ui(screen)
    elif current_screen == "story_screen":
        screen.blit(background_img, (0, 0))
        story = pygame.image.load("assets/story.png")
        story = pygame.transform.scale_by(pygame.image.load("assets/story.png"), 1/3)
        screen.blit(story, (75, 75))
        manager.draw_ui(screen)

    elif current_screen == "instructions_screen":
        screen.blit(background_img, (0, 0))
        instructions = pygame.image.load("assets/instructions.png")
        instructions = pygame.transform.scale_by(pygame.image.load("assets/instructions.png"), 1/2)
        screen.blit(instructions, (100, 100))
        manager.draw_ui(screen)

    elif current_screen == "gameplay":
        screen.blit(background_img, (0, 0))
        screen.blit(spaceship_img, (player_x, player_y))
        # Draw the asteroids (gray rectangles)
        for asteroid in asteroid_list:
            asteroid_resized = pygame.transform.scale(asteroid_img, (asteroid[2], asteroid[2]))  # Scale asteroid to random size
            screen.blit(asteroid_resized, (asteroid[0], asteroid[1]))

        for star in star_list:
            star_resized = pygame.transform.scale(star_img, (star[2], star[2]))  # Scale star to random size
            screen.blit(star_resized, (star[0], star[1]))

        if jupiter_appears:
            screen.blit(jupiter_img, (jupiter_x, jupiter_y))

        if jupiter_appears and player_y <- jupiter_y + 150:
            game_over = True

    if game_over:
        screen.blit(jupiter_img, (jupiter_x, jupiter_y))
        FINAL_SCORE = str(score)
        if not ai_score_calculated:
            AI_score = random.randrange(10100000,10100090)
            ai_score_calculated = True
        AI_text = font.render(str(AI_score), True, RED)
        if AI_score > int(FINAL_SCORE):
            winner = font.render("Unfortunately, the AI Pilot beat you. No money for you :(", True, RED)
        else:
            winner = font.render("You beat the AI Pilot! You just became a multi-millionaire!", True, RED)
        screen.blit(winner, (window_size[0] // 2 - 265, window_size[1] // 2 + 100))
        end_text = font.render("Welcome to Jupiter!", True, GRAY)
        display_score = font.render(FINAL_SCORE, True, GRAY)
        screen.blit(end_text, (window_size[0] // 2 - 80, window_size[1] // 2))
        screen.blit(display_score, (window_size[0] // 2 - 40, window_size[1] // 3) )  


    # Update the display
    pygame.display.update()

    score_text = font.render(f"Score: {score}", True, GRAY)
    screen.blit(score_text, (600 - 175, 10))

    pygame.display.flip()

    # Frame rate control
    clock.tick(30)