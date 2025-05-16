import pygame

class Bird(pygame.sprite.Sprite):

    rbird_img=pygame.image.load("img/Red.png")
    rbird_img=pygame.transform.scale(rbird_img,(30,30))

    def __init__(self, bird="red"):
        super().__init__()
        self.image=Bird.rbird_img
        self.rect=self.image.get_rect()
        self.rect.midbottom=(45,315)
        self.mask=pygame.mask.from_surface(self.image)
        self.vx = 0
        self.vy = 0
        self.move=False
    def Move(self):
        x,y=self.rect.midbottom
        x += self.vx
        y += self.vy
        self.rect.midbottom=x,y
        if self.rect.midbottom!= (45,315):
            self.vy+=1
    
    def update(self,x,y):
        self.Move(x,y)
    
    def draw(self,surface):
        surface.blit(self.image,self.rect)
    
    def Shoot(self,p):
        self.vx=(self.rect.midbottom[0]-p[0])/2
        self.vy=(self.rect.midbottom[1]-p[1])/2
        self.move=True
        #להעביר לhuman agent