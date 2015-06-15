import pygame
import math
import random
from classes import *

pygame.init()

# --- Screen Setup ---
size = (sc_width, sc_height)
screen = pygame.display.set_mode(size)
background_image = pygame.image.load("../Assets/Sprites/SpaceInvaderBackground.png").convert()
font = pygame.font.SysFont('Calibri', 25, True, False)

pygame.display.set_caption("Space Invaders")

done = False
clock = pygame.time.Clock()

# --- Sprite Lists ---
laser_list = pygame.sprite.Group()
alien_list = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()
aliens_hit_list = pygame.sprite.Group()
alien_overlap_list = pygame.sprite.Group()
alien_laser_list = pygame.sprite.Group()

# --- Initializations ---
score = 0
numAliens = 100

# Initialize player
player = Player()
player.setNumLasers(numAliens)
moveLeft = False
moveRight = False
shoot = False
all_sprites_list.add(player)

#Initialize shield
shield_radius = player.rect.height
shield_center = [player.rect.x, player.rect.y]
print(shield_center)
shield = Shield(shield_radius, shield_center)
shield.rect.center = player.rect.center
all_sprites_list.add(shield)


# Move overlapping aliens
for i in range(0, numAliens):
    alien = Alien()
    alien.rect.x = random.randrange(10, sc_width - 40)
    alien.rect.y = -1 * (random.randrange(numAliens * 50))

    for invader in alien_list:
        alien_overlap_list = pygame.sprite.spritecollide(alien, alien_list, False)

        for i in range(len(alien_overlap_list)):
            alien_overlap_list[i].rect.y -= 40 * i

            if alien_overlap_list[i].rect.x < sc_width / 2:
                alien_overlap_list[i].rect.x += 40
            else:
                alien_overlap_list[i].rect.x -= 40

    alien_list.add(alien)
    all_sprites_list.add(alien)


# --- Main Loop ---
while not done:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            done = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p: #pause game
                pause = True
                print('pause')
                while pause:
                    event = pygame.event.wait()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                        pause = False
            if event.key == pygame.K_LEFT:
                moveLeft = True
            if event.key == pygame.K_RIGHT:
                moveRight = True
            if event.key == pygame.K_SPACE:
                shoot = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                moveLeft = False
                player.reset_left_accel()
            if event.key == pygame.K_RIGHT:
                moveRight = False
                player.reset_right_accel()

    screen.blit(background_image, [0, 0])

# --- Drawing Code ---

    if moveLeft:
        player.moveLeft()
    elif moveRight:
        player.moveRight()

    # Firing lasers
    if shoot and all_sprites_list.has(player) and player.numLasers >= 1:
        laser = Laser(2, 10)
        laser.rect.x = player.rect.x + (player.width / 2)
        laser.rect.y = player.rect.y
        laser_list.add(laser)
        all_sprites_list.add(laser)
        print (all_sprites_list)
        shoot = False
        player.numLasers -= 1
        print("number of lasers: " + str(player.numLasers))

    # Firing alien lasers
    aliens = alien_list.sprites()
    if len(aliens) > 0 :
        index = random.randrange(len(aliens))
        # 1.0% chance for on-screen ships, 0% off-screen
        if (random.randrange(1000) < 10) and (aliens[index].rect.y >= 0):
            shot = AlienLaser(3)
            start_x = aliens[index].rect.x + (aliens[index].rect.width / 2) - 1
            start_y = aliens[index].rect.y + aliens[index].rect.height
            shot.setStart(start_x, start_y)
            all_sprites_list.add(shot)
            alien_laser_list.add(shot)
            print("alien shot fired")


    #Move aliens and lasers
    alien_laser_list.update()
    alien_list.update()
    laser_list.update()
    shield.update(player.rect.center)

    # Remove hit aliens
    for laser in laser_list:
        alien_hit_list = pygame.sprite.spritecollide(laser, alien_list, True)

        for alien in alien_hit_list:
            laser_list.remove(laser)
            all_sprites_list.remove(laser)
            score += 1
            print(score)

    # Shrink hit shield
    if all_sprites_list.has(shield):
        for bullet in alien_laser_list:
            if(pygame.sprite.collide_circle(shield, bullet)):
                shield.kill()
                bullet.kill()
                print("shield destroyed")
    else:
        for bullet in alien_laser_list:
            if(len(pygame.sprite.spritecollide(player, alien_laser_list, True)) > 0):
                player.kill()
                print("You Lose")

    #Draw all sprites
    all_sprites_list.draw(screen)

# --- End Drawing Code ---

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

