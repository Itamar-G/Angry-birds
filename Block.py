import pygame
from Graphic import *

class Block(pygame.sprite.Sprite):
    def __init__(self, start_pos, width=20, height=100, color=BROWN):
        super().__init__()
        self.start_pos = start_pos
        self.width = width
        self.height = height
        self.color = color
        
        self.image = pygame.Surface((width, height))
        self.image.fill(self.color)
        
        # Set rect to top-left corner of start_pos
        self.rect = self.image.get_rect()
        self.rect.topleft = start_pos
        self.mask=pygame.mask.from_surface(self.image)
        self.hit = 0


    def update(self):
        pass
    
    def rotate_90(self):
        # שמירה על המרכז או המיקום לפני הסיבוב (כדי שלא יקפוץ)
        center = self.rect.midbottom
        
        # החלפת רוחב וגובה (סיבוב של 90 מעלות)
        self.rect.width, self.rect.height = self.rect.height, self.rect.width
        
        # עדכון המלבנים מחדש לפי המרכז הישן
        self.rect = pygame.Rect(0, 0, self.rect.width, self.rect.height)
        self.rect.center = center
    
    def Hit(self):
        self.hit=self.hit+1
        if self.hit==3:
            self.rect=None