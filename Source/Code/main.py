import pygame
import math
import random
from classes import *
from screens import *

pygame.init()

# --- Screen Setup ---
size = (sc_width, sc_height)
screen = pygame.display.set_mode(size)
font = pygame.font.SysFont('Calibri', 25, True, False)

pygame.display.set_caption("Space Invaders")
pause = False
done = False
clock = pygame.time.Clock()

# Create and push screens to drawing list
screenstack = []
gameScreen = GameScreen()
screenstack.append(gameScreen)

# --- Main Loop ---
while not done:
    instructList = pygame.event.get()
    for event in instructList:
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

# --- Drawing Code ---
    screenstack[len(screenstack)-1].draw(screen, instructList)

# --- End Drawing Code ---
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
