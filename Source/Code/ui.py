# User interface in pygame
# Just buttons and forms

import pygame

class Form(pygame.sprite.Sprite):
    def __init__(self, screen, color, title="default"):
        pygame.sprite.Sprite.__init__(self)
        self.title = title
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.color = color

    def draw(self):
        pygame.draw.rect(self.screen, self.color,
                         pygame.Rect((0, 0),
                        (self.width, self.height)))

        myfont = pygame.font.SysFont("monospace", 50)
        label = myfont.render(self.title, 1, (255, 255, 255))
        self.screen.blit(label,
                        (self.width/2 - myfont.size(self.title)[0]/2,
                        self.height/2 - myfont.size(self.title)[1]/2))

class Label:
    def __init__(self):
        pass

class Button:
    def __init__(self, xpos, ypos,
                 size, text, color,
                 hovercolor):
        pass

    def draw(self):
        pass
