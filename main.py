import pygame
import random

pygame.init()

# game screen
screen = pygame.display.set_mode((800, 600))

# icon and title
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("space_invaders.png")
pygame.display.set_icon(icon)

# player character
player_image = pygame.image.load("player.png")
player_x = 368
player_y = 500
player_x_change = 0

# enemy character
enemy_image = pygame.image.load("enemy.png")
enemy_x = random.randint(0, 800)
enemy_y = random.randint(30, 175)
enemy_x_change = 7
enemy_y_change = 40

# enemy pew pew
laser = pygame.image.load("laser.png")
laser_x = 0
laser_y = 500
laser_x_change = 0
laser_y_change = 15
laser_state = "charged"

# background
background = pygame.image.load("background.png")


def player(x, y):
    screen.blit(player_image, (x, y))


def enemy(x, y):
    screen.blit(enemy_image, (x, y))


def shoot(x, y):
    global laser_state
    laser_state = "shoot"
    screen.blit(laser, (x, y + 10))


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
                laser_x = player_x
                shoot(laser_x, laser_y)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0

    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    player_x += player_x_change
    if player_x <= 0:
        player_x = 0
    elif player_x >= 736:
        player_x = 736

    enemy_x += enemy_x_change
    if enemy_x <= 0:
        enemy_x_change = 7
        enemy_y += enemy_y_change
    elif enemy_x >= 736:
        enemy_x_change = -7
        enemy_y += enemy_y_change
    if laser_y <= 20:
        laser_y = 480
        laser_state = "charged"
    if laser_state == " shoot":
        shoot(laser_x, laser_y)
        laser_y -= laser_y_change

    player(player_x, player_y)
    enemy(enemy_x, enemy_y)
    pygame.display.update()
