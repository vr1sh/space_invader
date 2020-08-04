import pygame
from pygame import mixer
import math
import random

pygame.init()

# game screen
screen = pygame.display.set_mode((800, 600))

# icon and title
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("space_invaders.png")
pygame.display.set_icon(icon)

# background
background = pygame.image.load("background.png")
mixer.music.load("background.wav")
mixer.music.play(-1)

# player character
player_image = pygame.image.load("player.png")
player_x = 368
player_y = 500
player_x_change = 0

# enemy character
enemy_image = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
number_of_enemies = 7

for i in range(number_of_enemies):
    enemy_image.append(pygame.image.load("enemy.png"))
    enemy_x.append(random.randint(0, 735))
    enemy_y.append(random.randint(30, 175))
    enemy_x_change.append(8)
    enemy_y_change.append(40)

# enemy pew pew
laser = pygame.image.load("laser.png")
laser_x = 0
laser_y = 500
laser_x_change = 0
laser_y_change = 15
laser_state = "charged"

# score
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 30)
text_x = 12
text_y = 12

# game over
over_font = pygame.font.Font("freesansbold.ttf", 64)


def display_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(player_image, (x, y))


def enemy(x, y, i):
    screen.blit(enemy_image[i], (x, y))


def shoot(x, y):
    global laser_state
    laser_state = "shoot"
    screen.blit(laser, (x, y + 10))


def collision(enemy_x, enemy_y, laser_x, laser_y):
    distance = math.sqrt((math.pow(enemy_x - laser_x, 2)) + (math.pow((enemy_y - laser_y), 2)))
    if distance < 30:
        return True
    else:
        return False


# game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -6.7
            if event.key == pygame.K_RIGHT:
                player_x_change = 6.7
            if event.key == pygame.K_SPACE:
                if laser_state == "charged":
                    laser_sound = mixer.Sound("laser.wav")
                    laser_sound.play()
                    laser_x = player_x
                    shoot(laser_x, laser_y)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0

    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    # player movement
    player_x += player_x_change

    if player_x <= 0:
        player_x = 0
    elif player_x >= 736:
        player_x = 736

    # enemy movement
    for i in range(number_of_enemies):

        # Game over
        if enemy_y[i] > 430:
            for j in range(number_of_enemies):
                enemy_y[j] = 850
            game_over()
            break

        enemy_x[i] += enemy_x_change[i]
        if enemy_x[i] <= 0:
            enemy_x_change[i] = 7
            enemy_y[i] += enemy_y_change[i]
        elif enemy_x[i] >= 736:
            enemy_x_change[i] = -7
            enemy_y[i] += enemy_y_change[i]

        # collision
        collided = collision(enemy_x[i], enemy_y[i], laser_x, laser_y)
        if collided:
            collision_sound = mixer.Sound("explosion.wav")
            collision_sound.play()
            laser_y = 480
            laser_state = "charged"
            score_value += 1
            enemy_x[i] = random.randint(0, 735)
            enemy_y[i] = random.randint(30, 175)
        enemy(enemy_x[i], enemy_y[i], i)

    # laser movement
    if laser_y <= 25:
        laser_y = 480
        laser_state = "charged"

    if laser_state == "shoot":
        shoot(laser_x, laser_y)
        laser_y -= laser_y_change

    player(player_x, player_y)
    display_score(text_x, text_y)
    pygame.display.update()
