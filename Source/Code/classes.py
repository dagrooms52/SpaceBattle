#Daniel Grooms
#Space Invader Classes
#Player, Laser, Alien


import pygame
import math
import random
from constants import *

"""
The player class defines the object the user plays as in the space invaders game.
"""
class Player(pygame.sprite.Sprite):

    # --- Player class variables ---
    height = 0
    width = 0
    speed = 8
    left_accel_speed = 2
    right_accel_speed = 2
    accel_rate = 1.09
    startX = SCREEN_SIZE['width'] / 2
    yPos = 0
    numLasers = 0
    numMissiles = 0
    laserMultiplier = 2

    # --- Player class methods ---
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("../Assets/Sprites/Spaceship.png").convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.width = self.rect.width
        self.height = self.rect.height
        self.yPos = SCREEN_SIZE['height'] - (self.height * 4)
        self.rect.y = self.yPos
        # Centered on passed position
        self.rect.x = position - (self.width / 2)

    def moveLeft(self):
        if not (self.rect.x <= 5):
            if self.left_accel_speed < self.speed:
                self.left_accel_speed *= self.accel_rate
                self.rect.x -= int(self.left_accel_speed)
            else:
                self.rect.x -= self.speed

    def moveRight(self):
        if not (self.rect.x + self.width + 4 >= SCREEN_SIZE['width']):
            if self.right_accel_speed < self.speed:
                self.right_accel_speed *= self.accel_rate
                self.rect.x += int(self.right_accel_speed)
            else:
                self.rect.x += self.speed

    def reset_left_accel(self):
        self.left_accel_speed = 2

    def reset_right_accel(self):
        self.right_accel_speed = 2

    def setNumLasers(self, numAliens):
        self.numLasers = numAliens * self.laserMultiplier


"""
The shield class defines the shield surrounding the player's spaceship.
This shield protects the player from a certain amount of alien laser hits.
"""
class Shield(pygame.sprite.Sprite):

    # --- Shield class variables ---
    radius = 0
    diameter = radius * 2
    thickness = 2
    center = []

    # --- Shield class methods ---
    def __init__(self, radius, center):
        self.radius = radius
        self.center = center

        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([radius * 2, radius * 2])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)

        #Draw circular shield
        pygame.draw.circle(self.image,
                           ELECTRICBLUE,
                           [radius, radius],
                           radius,
                           self.thickness)
        self.rect = self.image.get_rect()
        self.rect.center = center

    def update(self, center):
        self.rect.center = center

    def shrink(self):
        if(self.thickness > 1):
            self.thickness -= 1
        if self.thickness == 0:
            self.kill()

"""
The Laser class defines the main weapon used by the player in defending the
objective from enemy alien ships.
"""
class Laser(pygame.sprite.Sprite):

    # --- Laser class variables ---
    startX = 0
    startY = 0
    color = RED
    speed = 10
    width = 2
    height = 10

    # --- Laser class methods ---
    def __init__(self, width, height):

        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)

        #Draw line
        pygame.draw.line(self.image, self.color, [0, 0], [0, height], width)
        self.rect = self.image.get_rect()

    def update(self):

        if self.rect.y <= self.height * -1:
            self.kill()
        self.rect.y -= self.speed


"""
    The Alien class defines the opponent of the player in Space Invaders.
"""
class Alien(pygame.sprite.Sprite):

    # --- Alien class variables
    speed = 2
    width = 0
    height = 0

    # --- Alien class methods
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("../Assets/Sprites/Alien.png").convert()
        self.image.set_colorkey(WHITE)

        self.rect = self.image.get_rect()
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.rect.y = 0
        self.rect.x = 0

        self.laser_list = pygame.sprite.Group()

    def update(self):
        if self.rect.y >= SCREEN_SIZE['height'] + self.rect.height:
            self.kill()
        self.rect.y += self.speed

        if self.rect.y + self.height > 0:
            # Keep from calling this every update cycle unless needed
            if random.randrange(4500) <= 10:
                self.shoot()

    def shoot(self):
        shot = AlienLaser(3)
        start_x = self.rect.x + (self.rect.width / 2) - 1
        start_y = self.rect.y + self.rect.height
        shot.setStart(start_x, start_y)
        self.laser_list.add(shot)

    def getLaserList(self):
        return self.laser_list

    def moveToCoord(self, x, y):
        self.rect.x = x
        self.rect.y = y


class AlienLaser(pygame.sprite.Sprite):

    # --- Laser class variables ---
    startX = 0
    startY = 0
    color = CYAN
    speed = 5
    radius = 0

    # --- Laser class methods ---
    def __init__(self, radius):

        self.radius = radius
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([self.radius * 2, self.radius * 2])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)

        #Draw line
        pygame.draw.circle(self.image, self.color, [radius, radius], radius)
        self.rect = self.image.get_rect()

    def update(self):

        if self.rect.y > SCREEN_SIZE['height']:
            self.kill()
        self.rect.y += self.speed

    def setStart(self, xCoord, yCoord):
        self.rect.x = xCoord
        self.rect.y = yCoord

class Boss(Alien):

    def __init__(self):
        # Sprite -> Alien -> Boss
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("../Assets/Sprites/Boss.png").convert()
        self.image.set_colorkey(WHITE)

        self.rect = self.image.get_rect()
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.rect.y = 0
        self.rect.x = 0
        self.speed = 1
