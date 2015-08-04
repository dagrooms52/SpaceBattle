# Daniel Grooms
# Different screens for the game

import pygame
import ui
from classes import *
from constants import *

class BaseScreen(object):
    def draw(self, instructions):
        pass
    def getType(self):
        return "BaseScreen"

class StartMenu(BaseScreen):
    def __init__(self, screen):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.bgRGB = (34, 49, 63) #ebony
        self.spaceRGB = (3, 11, 30)
        self.buttonRGB = (218, 223, 225)
        self.highlightRGB = (25, 181, 254)

        self.form = ui.Form(screen, self.spaceRGB,
                    "Press Enter")

    def draw(self, instructions):
        self.form.draw()

    def getType(self):
        return "StartMenu"


class GameScreen(BaseScreen):

    def __init__(self, screen):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.background_image = pygame.image.load(
            "../Assets/Sprites/SpaceInvaderBackground.png"
            ).convert()

        # --- Sprite Lists ---
        self.laser_list = pygame.sprite.Group()
        self.alien_list = pygame.sprite.Group()
        self.all_sprites_list = pygame.sprite.Group()
        self.aliens_hit_list = pygame.sprite.Group()
        self.alien_overlap_list = pygame.sprite.Group()
        self.alien_laser_list = pygame.sprite.Group()

        # --- Initializations ---
        self.score = 0
        self.numAliens = 30
        self.bossyet = False

        # Initialize player
        self.player = Player(self.width / 2)
        self.player.setNumLasers(self.numAliens)
        self.moveLeft = False
        self.moveRight = False
        self.shoot = False
        self.all_sprites_list.add(self.player)

        #Initialize shield
        shield_radius = self.player.rect.height
        shield_center = [self.player.rect.x, self.player.rect.y]
        self.shield = Shield(shield_radius, shield_center)
        self.shield.rect.center = self.player.rect.center
        self.all_sprites_list.add(self.shield)


        # Create the round's aliens
        # For positioning, have 1-5 aliens per "row"
        # Spread evenly on the row
        swarm_width = self.width / 2
        aliens_left = self.numAliens
        row_count = 0
        while aliens_left > 0:
            row_count += 1
            numberInRow = random.randrange(2, 4)
            for j in range(numberInRow):
                alien = Alien()

                # Set alien position
                increment = swarm_width / numberInRow
                xpos = (j * increment) - (alien.width / 2) \
                        + (increment / 2) + ((self.width - swarm_width) / 2)
                ypos = -row_count * (alien.height * 15)
                alien.moveToCoord(xpos, ypos)
                aliens_left -= 1

                self.alien_list.add(alien)
                self.all_sprites_list.add(alien)


    # Drawing code, called from screen holder
    def draw(self, instructions):

        # Handle any input
        for event in instructions:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.moveLeft = True
                if event.key == pygame.K_RIGHT:
                    self.moveRight = True
                if event.key == pygame.K_SPACE:
                    self.shoot = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.moveLeft = False
                    self.player.reset_left_accel()
                if event.key == pygame.K_RIGHT:
                    self.moveRight = False
                    self.player.reset_right_accel()

        # Move player
        if self.moveLeft:
            self.player.moveLeft()
        elif self.moveRight:
            self.player.moveRight()

        # Firing lasers
        if self.shoot and \
           self.all_sprites_list.has(self.player) and \
           self.player.numLasers >= 1:

            laser = Laser(2, 10)
            laser.rect.x = self.player.rect.x + (self.player.width / 2)
            laser.rect.y = self.player.rect.y
            self.laser_list.add(laser)
            self.all_sprites_list.add(laser)
            self.shoot = False
            self.player.numLasers -= 1
            print("number of lasers: " + str(self.player.numLasers))

        # Send boss if all aliens are dead
        if len(self.alien_list.sprites()) == 0 and not self.bossyet:
            self.bossyet = True
            boss = Boss()
            boss.moveToCoord((self.width/2) - boss.width, -boss.height)
            self.alien_list.add(boss)
            self.all_sprites_list.add(boss)

        # Firing alien lasers
        aliens = self.alien_list.sprites()
        if len(aliens) > 0 :
            index = random.randrange(len(aliens))
            # 1.0% chance for on-screen ships, 0% off-screen
            if (random.randrange(1000) < 10) and (aliens[index].rect.y >= 0):
                shot = AlienLaser(3)
                start_x = aliens[index].rect.x + (aliens[index].rect.width / 2) - 1
                start_y = aliens[index].rect.y + aliens[index].rect.height
                shot.setStart(start_x, start_y)
                self.all_sprites_list.add(shot)
                self.alien_laser_list.add(shot)

        #Move aliens and lasers
        self.alien_laser_list.update()
        self.alien_list.update()
        self.laser_list.update()
        self.shield.update(self.player.rect.center)

        # Remove hit aliens
        alien_hit_list = []
        for laser in self.laser_list:
            alien_hit_list = pygame.sprite.spritecollide(laser, self.alien_list, True)
            for alien in alien_hit_list:
                self.laser_list.remove(laser)
                self.all_sprites_list.remove(laser)
                alien.kill()
                self.score += 1
                print(self.score)

        # Shrink hit shield
        if self.all_sprites_list.has(self.shield):
            for bullet in self.alien_laser_list:
                if(pygame.sprite.collide_circle(self.shield, bullet)):
                    self.shield.kill()
                    bullet.kill()
                    print("shield destroyed")
        else:
            for bullet in self.alien_laser_list:
                if(len(pygame.sprite.spritecollide(self.player, self.alien_laser_list, True)) > 0):
                    self.player.kill()
                    print("You Lose")

        # Clear screen and draw sprites
        self.screen.blit(self.background_image, [0, 0])
        self.all_sprites_list.draw(self.screen)

    def getType(self):
        return "GameScreen"

class PauseScreen(BaseScreen):
    def draw(self, instructions):
        pass
    def getType(self):
        return "PauseScreen"

class OptionsScreen(BaseScreen):
    def draw(self, instructions):
        pass
    def getType(self):
        return "OptionsScreen"
