import pygame
from Graphic import *

class Block(pygame.sprite.Sprite):
    def __init__(self, start_pos, width=20, height=60, color=BROWN):
        super().__init__()
        self.width = width
        self.height = height
        self.color = color

        self.angle = 360
        self.original_image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.original_image.fill(color)

        self.image = self.original_image
        self.rect = self.image.get_rect(midbottom=start_pos)

        self.mask = pygame.mask.from_surface(self.image)
        self.hit = 0
        self.vy = 0
        self.falling = True  # במצב ברירת מחדל - כולם נופלים

    def update(self):
        pass

    def rotate(self):
        self.angle -= 3
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        old_midbottom = self.rect.midbottom
        self.rect = self.image.get_rect(midbottom=old_midbottom)
        self.mask = pygame.mask.from_surface(self.image)

    def fall(self):
        if self.falling:
            x, y = self.rect.midbottom
            y += self.vy
            self.rect.midbottom = (x, y)
            self.vy += 1
        else:
            self.vy = 0