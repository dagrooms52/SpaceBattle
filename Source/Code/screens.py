# Daniel Grooms
# Different screens for the game

import pygame
from classes import *

class BaseScreen(object):
    def draw(self, instructions):
        pass

class StartMenu(BaseScreen):
    def draw(self, instructions):
        pass

class GameScreen(BaseScreen):

    def __init__(self):
        self.background_image = pygame.image.load("""../Assets/Sprites/SpaceInvaderBackground.png""").convert()

        # --- Sprite Lists ---
        self.laser_list = pygame.sprite.Group()
        self.alien_list = pygame.sprite.Group()
        self.all_sprites_list = pygame.sprite.Group()
        self.aliens_hit_list = pygame.sprite.Group()
        self.alien_overlap_list = pygame.sprite.Group()
        self.alien_laser_list = pygame.sprite.Group()

        # --- Initializations ---
        self.score = 0
        self.numAliens = 100

        # Initialize player
        self.player = Player()
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


        # Move overlapping aliens
        for i in range(0, self.numAliens):
            alien = Alien()
            alien.rect.x = random.randrange(10, sc_width - 40)
            alien.rect.y = -1 * (random.randrange(self.numAliens * 50))

            self.alien_list.add(alien)
            self.all_sprites_list.add(alien)

            for invader in self.alien_list:
                alien_overlap_list = pygame.sprite.spritecollide(alien, self.alien_list, False)

                for i in range(len(alien_overlap_list)):
                    alien_overlap_list[i].rect.y -= 40 * i

                    if alien_overlap_list[i].rect.x < sc_width / 2:
                        alien_overlap_list[i].rect.x += 40
                    else:
                        alien_overlap_list[i].rect.x -= 40


    # Drawing code, called from screen holder
    def draw(self, screen, instructions):

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
            print("moving")
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
                print("alien shot fired")

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
        screen.blit(self.background_image, [0, 0])
        self.all_sprites_list.draw(screen)

class PauseScreen(BaseScreen):
    def draw(self, instructions):
        pass

class OptionsScreen(BaseScreen):
    def draw(self, instructions):
        pass