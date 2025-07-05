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
        self.tries = 3
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
        self.tries = 3
        self.pigs.empty()
        self.blocks.empty()

        num_buildings = random.randint(2, 4)

        for _ in range(num_buildings):
            x = random.randint(250, 600)
            num_floors = random.randint(2, 4)

            for i in range(num_floors):
                is_horizontal = random.random() < 0.3  # 30% מהבלוקים יהיו שוכבים
                width = 60 if is_horizontal else 20
                height = 20 if is_horizontal else 60
                y = 310 - (i * height)
                block = Block((x, y), width=width, height=height)
                self.blocks.add(block)

            # שים חזיר על הקומה העליונה
            top_y = 310 - (num_floors * (20 if is_horizontal else 60)) - 40
            self.init_pigs((x, top_y))
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
    def move(self, action):
        if action is not None:
            if not self.bird.move:
                self.bird.vx = action[0]
                self.bird.vy = action[1]
                self.bird.move = True
                self.tries -= 1

        # תנועת הציפור
        if self.bird.move:
            self.bird.Move()

        # בדיקת פגיעות בציפורים מול חזירים
        bird_group = pygame.sprite.GroupSingle(self.bird)
        pygame.sprite.groupcollide(bird_group, self.pigs, False, True, pygame.sprite.collide_mask)

        # עדכון חזירים
        for pig in self.pigs:
            pig.stay = False

            for block in self.blocks:
                if pygame.sprite.collide_mask(pig, block):
                    pig.stay = True
                    break

            if not pig.stay:
                pig.Fall()

            if pig.rect.bottom >= 310:
                pig.stay = True

            if pig.vy > 10 and pig.rect.bottom > 350:
                pig.kill()

        # עדכון בלוקים
        for block in list(self.blocks):
            block.falling = True

            # אם על הקרקע – לא ליפול
            if block.rect.bottom >= 310:
                block.falling = False

            # בדיקת התנגשויות עם בלוקים אחרים
            for other in self.blocks:
                if block is not other:
                    if pygame.sprite.collide_mask(block, other):
                        # בלוק מונח על אחר
                        if abs(block.rect.bottom - other.rect.top) < 5:
                            block.falling = False

                        # בלוק פוגע מלמעלה בבלוק אחר – גורם לו ליפול
                        if block.vy > 0 and abs(block.rect.top - other.rect.bottom) < 5:
                            other.falling = True
                            other.vy += block.vy // 2

            # פגיעה בציפור
            if pygame.sprite.collide_mask(block, self.bird):
                block.rect.midbottom = (block.rect.midbottom[0] + self.bird.vx * 2 + 30, block.rect.midbottom[1])
                self.bird.rect.midbottom = (45, 315)
                self.bird.move = False
                block.angle -= 1
                block.hit += 1

            # השמדת בלוק לאחר 2 פגיעות
            if block.hit >= 2:
                block.kill()

            # סיבוב בלוק
            if 270 < block.angle < 360:
                block.rotate()

            # הפעלת נפילה אם צריך
            block.fall()

        # ציפור נופלת לקרקע – אפס אותה
        if self.bird.rect.midbottom[1] > 400:
            self.bird.rect.midbottom = (45, 315)
            self.bird.move = False

        # אם אין חזירים – סיים שלב או עלה שלב
        if len(self.pigs) == 0:
            for block in self.blocks:
                if 270 < block.angle < 360:
                    block.rotate()

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
        if self.bird.move:
            return False
        for block in self.blocks:
            if block.angle<360 and block.angle>270:
                return False
        if len(self.pigs)==0:return True
        if self.tries==0: 
            return True
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
        