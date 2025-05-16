import pygame
from Bird import Bird
from Graphic import *
from Block import Block
from Pig import Pig

class Environment:
    def __init__(self):
        self.bird = Bird()
        self.pigs = pygame.sprite.Group()
        self.blocks = pygame.sprite.Group()

    def init_pigs (self,pos):
        pig=Pig(pos)
        self.pigs.add(pig)

    def init_blocks (self):
        block=Block((500,260))
        self.blocks.add(block)
        block=Block((300,260))
        self.blocks.add(block)
        

    def init_display (self):
        pygame.init()
        self.screen=pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption("Angry birds")
        self.clock=pygame.time.Clock()
        self.background=pygame.image.load("img/background.webp")
        self.background=pygame.transform.scale(self.background,(WIDTH,HEIGHT))
        self.rug=pygame.image.load("img/rug.png")
        self.rug=pygame.transform.scale(self.rug,(60,60))
        self.init_blocks()
        self.init_pigs((510,260))
        # update bird vx, vy
        # bird.move()
    def move (self, action):
        if action is not None:
            if self.bird.move==False:
                self.bird.Shoot(action)
                self.bird.move=True
        if self.bird.move==True:
            self.bird.Move()
        bird_group=pygame.sprite.GroupSingle(self.bird)
        pygame.sprite.groupcollide(bird_group,self.pigs,False,True,pygame.sprite.collide_mask)
        for block in self.blocks:
            if pygame.sprite.collide_mask(block,self.bird):
                self.bird.rect.midbottom=(45,315)
                self.bird.move=False
                block.angle+=1
                block.hit+=1
            if block.hit==2:
                block.kill()
            if block.angle>0 and block.angle<90:
                block.Move()
        if self.bird.rect.midbottom[1]>450:
            self.bird.rect.midbottom=(45,315)
            self.bird.move=False
    def render (self):
        # draw background to clear
        # draw rugs on screen
        # draw blocks on screen
        # draw pigs on screen
        # draw bird on screen
                
        self.screen.blit(self.background,(0,0))
        self.screen.blit(self.rug,(10,296))
        self.bird.draw(self.screen)
        self.blocks.draw(self.screen)
        self.pigs.draw(self.screen)
        
        pygame.display.update()
        self.clock.tick(FPS)

    def end_of_game (self):
        return False
    def state(self):
        state_list=[]
        index=0
        for sprite in self.pigs:
            state_list.append(sprite.rect.centerx)
            state_list.append(sprite.rect.centery)
            state_list.append(sprite.vx)
            state_list.append(sprite.vy)
            index+=4
        