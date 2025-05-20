import pygame

class Pig(pygame.sprite.Sprite):
    image=pygame.image.load("img/pig.webp")
    image=pygame.transform.scale(image,(40,40))
    
    def __init__(self, pos):
        super().__init__()
        self.image=Pig.image
        self.rect=self.image.get_rect()
        self.rect.midbottom=(pos)
        self.mask=pygame.mask.from_surface(self.image)
        self.vy=0
        self.stay=True
    def draw(self,surface):
        surface.blit(self.image,self.rect)
    def Fall(self):
        x,y=self.rect.midbottom
        y += self.vy
        self.rect.midbottom=x,y
        self.vy+=1
        if self.rect.midbottom[1]>350:self.image=None
