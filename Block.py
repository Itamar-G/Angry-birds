import pygame
from Graphic import *

class Block(pygame.sprite.Sprite):
    def __init__(self, start_pos, width=20, height=100, color=BROWN):
        super().__init__()
        self.start_pos = start_pos
        self.width = width
        self.height = height
        self.color = color
        
        self.angle=0
        self.original_image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.original_image.fill(color)
        
        self.image = self.original_image
        self.rect = self.image.get_rect(center=start_pos)
                
        self.mask = pygame.mask.from_surface(self.image)
        
                
        self.hit = 0


    def update(self):
        pass
    
    def Move(self):
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.angle+=1
    
    def rotate(self, angle):
        """ Rotate the block by a given angle (in degrees). """
        self.angle = angle
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        
        # Keep the center consistent
        old_center = self.rect.center
        self.rect = self.image.get_rect(center=old_center)
        
        # Update mask for collisions
        self.mask = pygame.mask.from_surface(self.image)