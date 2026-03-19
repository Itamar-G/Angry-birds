import pygame

class Pig(pygame.sprite.Sprite):
    image=pygame.image.load("img/pig.webp")
    image=pygame.transform.scale(image,(40,40))
    
    def __init__(self, pos):
        super().__init__()
        self.image = Pig.image
        self.rect = self.image.get_rect()
        self.rect.midbottom = pos # המיקום שהתקבל מה-Environment
        self.mask = pygame.mask.from_surface(self.image)
        self.vy = 0
        self.stay = True # מתחיל במצב יציב
    def draw(self,surface):
        surface.blit(self.image,self.rect)
    def Fall(self):
        x,y=self.rect.midbottom
        y += self.vy
        self.rect.midbottom=x,y
        self.vy+=1
        if y > 1000: 
            self.vy = 0
            self.rect.midbottom = (x, 1000)
