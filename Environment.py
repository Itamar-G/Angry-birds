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
        block=Block((500,300))
        self.blocks.add(block)
        block=Block((300,300))
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
        self.init_pigs((500,300))
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
        pygame.sprite.groupcollide(bird_group,self.blocks,True,False,pygame.sprite.collide_mask)
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
        