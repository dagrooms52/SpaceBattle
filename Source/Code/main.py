import pygame
import math
import random
import constants
from classes import *
from screens import *

pygame.init()

# --- Screen Setup ---
screen = pygame.display.set_mode((0,0), (pygame.FULLSCREEN|pygame.NOFRAME))
constants.SCREEN_SIZE['width'] = screen.get_width()
constants.SCREEN_SIZE['height'] = screen.get_height()

font = pygame.font.SysFont('Calibri', 25, True, False)

pygame.display.set_caption("Space Invaders")
pygame.mouse.set_visible(False)
pause = False
done = False
clock = pygame.time.Clock()

# Create and push screens to drawing list
screenstack = []
startScreen = StartMenu(screen)
gameScreen = GameScreen(screen)

screenstack.append(gameScreen)
screenstack.append(startScreen)

# --- Main Loop ---
while not done:
    instructList = pygame.event.get()
    for event in instructList:
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
            if event.key == pygame.K_p: #pause game
                pause = True
                print('pause')
                while pause:
                    event = pygame.event.wait()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                        pause = False
            if event.key == pygame.K_RETURN:
                # Check which screen is up
                if screenstack[-1].getType() == "StartMenu":
                    screenstack.pop()

    # --- Drawing Code ---

    # Draw the top screen on the stack
    # Certain events push or pop certain screens onto the stack
    screenstack[-1].draw(instructList)

    # --- End Drawing Code ---
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
