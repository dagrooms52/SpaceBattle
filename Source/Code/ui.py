# User interface in pygame
# Just buttons and forms

import pygame

class Form(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos):
        pygame.sprite.Sprite.__init__(self)
        self.width = 20
        self.height = 20
        self.x = xpos
        self.y = ypos

        self.image = pygame.Surface([self.x, self.y])
        self.image.fill((34, 49, 63))

    def draw(self):
        pygame.draw.rect(self.image, (34, 49, 63),
                         pygame.Rect((self.x, self.y),
                                    (self.width, self.height)))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

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
