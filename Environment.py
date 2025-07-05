import pygame
from Bird import Bird
from Graphic import *
from Block import Block
from Pig import Pig
import random

class Environment:
    def __init__(self):
        self.bird = Bird()
        self.pigs = pygame.sprite.Group()
        self.blocks = pygame.sprite.Group()
        self.tries = 4
        self.level = 1
        self.screen = None

    def init_pigs (self,pos):
        pig=Pig(pos)
        self.pigs.add(pig)

    def init_blocks (self):
        block=Block((500,310))
        self.blocks.add(block)
        block=Block((300,310))
        self.blocks.add(block)

    def init_level(self, level_num):
        self.tries = 4
        self.pigs.empty()
        self.blocks.empty()

        num_pigs = random.randint(2, 3)
        num_blocks = random.randint(num_pigs, 4)  # לפחות בלוק אחד לכל חזיר

        # צור בלוקים רנדומליים
        block_positions = []
        for _ in range(num_blocks):
            x = random.randint(250, 600)
            y = 310
            block = Block((x, y))
            self.blocks.add(block)
            block_positions.append((x, y))

        # מיקום חזירים מעל בלוקים (אחד לכל בלוק)
        selected_blocks = random.sample(block_positions, num_pigs)
        for pos in selected_blocks:
            x, y = pos
            pig_y = y - 40  # גובה החזיר מעל הבלוק
            self.init_pigs((x, pig_y))

    def init_display(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Angry Birds")
        self.clock = pygame.time.Clock()
        self.background = pygame.image.load("img/background.webp")
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        self.rug = pygame.image.load("img/rug.png")
        self.rug = pygame.transform.scale(self.rug, (60, 60))
        self.init_level(self.level)
    def move (self, action):
        if action is not None:
            if self.bird.move==False:
                self.bird.vx=action[0]
                self.bird.vy=action[1]
                self.bird.move=True
                self.tries-=1
        if self.bird.move==True:
            self.bird.Move()
        bird_group=pygame.sprite.GroupSingle(self.bird)
        pygame.sprite.groupcollide(bird_group,self.pigs,False,True,pygame.sprite.collide_mask)
        for pig in self.pigs:
            if pig.stay==False:pig.Fall()
            pig.stay=False
            for block in self.blocks:
                if pygame.sprite.collide_mask(block,pig):
                    pig.stay=True
                if pygame.sprite.collide_mask(block,self.bird):
                    block.rect.midbottom=(block.rect.midbottom[0]+self.bird.vx*2+30,block.rect.midbottom[1])
                    self.bird.rect.midbottom=(45,315)
                    
                    self.bird.move=False
                    block.angle-=1
                    block.hit+=1
                if block.hit==2:
                    block.kill()
                if block.angle<360 and block.angle>270:
                    block.rotate()
                if pygame.sprite.collide_mask(pig,block):
                    if pig.vy>10:
                        pig.kill()
                    else: pig.stay=True
                if pig.rect.midbottom[1]>350:
                    if pig.vy>10: pig.kill()
                    else:pig.stay=True
        if self.bird.rect.midbottom[1]>400:
            self.bird.rect.midbottom=(45,315)
            
            self.bird.move=False
        if len(self.pigs)==0:
            for block in self.blocks:
                if block.angle<360 and block.angle>270:
                    block.rotate()
        if len(self.pigs) == 0:
            self.level += 1
            if self.level > 3:
                self.tries = 0  # סוף המשחק
            else:
                self.bird.rect.midbottom = (45, 315)
                self.bird.move = False
                self.init_level(self.level)
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
        if len(self.pigs)==0:return True
        if self.tries==0: return True
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
        