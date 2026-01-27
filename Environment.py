import pygame
from Bird import Bird
from Graphic import *
from Block import Block
from Pig import Pig
import random
from State import State 

class Environment:
    def __init__(self,state: State = None):
        self.bird = Bird()
        self.pigs = pygame.sprite.Group()
        self.blocks = pygame.sprite.Group()
        self.tries = 3
        self.level = 1
        self.screen = None
        if state:
            self.state : State = state
        else:
            self.state = State()

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

        num_buildings = 1#random.randint(2, 4)

        for _ in range(num_buildings):
            x = random.randint(250, 600)
            num_floors = 2#random.randint(2, 4)

            for i in range(num_floors):
                is_horizontal = random.random() < 0.3  # 30% מהבלוקים יהיו שוכבים
                width = 60 if is_horizontal else 20
                height = 20 if is_horizontal else 60
                y = 360 - (i * height)
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
        # — אם יש פעולה (action לא None) — בצע ירייה / התחל תנועה
        if action is not None:
            if not self.bird.move:
                self.bird.vx = (action[0] + 1) * 5
                self.bird.vy = (action[1] - 1) * (-5)
                self.bird.move = True
                self.tries -= 1
        # תנועת הציפור
        if self.bird.move:
            self.bird.Move()

        # גיבוש קבוצות sprites לציפור / חזירים
        bird_group = pygame.sprite.GroupSingle(self.bird)

        # התנגשויות ציפור-חזירים
        killed = pygame.sprite.groupcollide(bird_group, self.pigs, False, True, pygame.sprite.collide_mask)
        # עדכון חזירים: נפילה, בדיקות קרקע וכו׳
        for pig in list(self.pigs):
            pig.stay = False
            for block in self.blocks:
                if pygame.sprite.collide_mask(pig, block):
                    pig.stay = True
                    break
            if not pig.stay:
                pig.Fall()
            if pig.rect.bottom >= 310:
                pig.stay = True
        # עדכון בלוקים: נפילה, התנגשות, סיבוב/הריסה
        for block in list(self.blocks):
            block.falling = True
            if block.rect.bottom >= 310:
                block.falling = False
            for other in self.blocks:
                if block is not other:
                    if pygame.sprite.collide_mask(block, other):
                        if abs(block.rect.bottom - other.rect.top) < 5:
                            block.falling = False
                        if block.vy > 0 and abs(block.rect.top - other.rect.bottom) < 5:
                            other.falling = True
                            other.vy += block.vy // 2
            if pygame.sprite.collide_mask(block, self.bird):
                block.rect.midbottom = (block.rect.midbottom[0] + self.bird.vx*2 + 30,
                                        block.rect.midbottom[1])
                self.bird.rect.midbottom = (45, 315)
                self.bird.move = False
                block.angle -= 1
                block.hit += 1
            if block.hit >= 2:
                block.kill()
            if 270 < block.angle < 360:
                block.rotate()
            block.fall()

        # ציפור נופלת לקרקע — אפס
        if self.bird.rect.midbottom[1] > 400:
            self.bird.rect.midbottom = (45, 315)
            self.bird.move = False
    
    def fast_move(self, action):
         # אתחול משתנים
        next_state = None
        reward = 0
        done = False

        # — אם יש פעולה (action לא None) — בצע ירייה / התחל תנועה
        if action is not None:
            if not self.bird.move:
                self.bird.vx = (action[0] + 1) * 5
                self.bird.vy = (action[1] - 1) * (-5)
                self.bird.move = True
                self.tries -= 1
                reward += -1

        # — בצע את שאר הלוגיקה של movement / פיזיקה / התנגשויות וכו׳
        # תנועת הציפור
        self.bird.Move()
        while self.bird.move:
            # גיבוש קבוצות sprites לציפור / חזירים
            bird_group = pygame.sprite.GroupSingle(self.bird)

            # התנגשויות ציפור-חזירים
            killed = pygame.sprite.groupcollide(bird_group, self.pigs, False, True, pygame.sprite.collide_mask)
            if killed:
                # אם פגעה בחזיר — תגמול חיובי
                reward += +50  # תתאים לפי טווח שלך

            # עדכון חזירים: נפילה, בדיקות קרקע וכו׳
            for pig in list(self.pigs):
                pig.stay = False
                for block in self.blocks:
                    if pygame.sprite.collide_mask(pig, block):
                        pig.stay = True
                        break
                if not pig.stay:
                    pig.Fall()
                if pig.rect.bottom >= 310:
                    pig.stay = True
                    reward += 50
                if self.bird.rect.midbottom[1] < pig.rect.midbottom[1]+20 and self.bird.rect.midbottom[1] > pig.rect.midbottom[1]-20:
                    reward+=50/(abs(self.bird.rect.midbottom[0]-pig.rect.midbottom[0]))


            # עדכון בלוקים: נפילה, התנגשות, סיבוב/הריסה
            for block in list(self.blocks):
                block.falling = True
                if block.rect.bottom >= 310:
                    block.falling = False
                for other in self.blocks:
                    if block is not other:
                        if pygame.sprite.collide_mask(block, other):
                            if abs(block.rect.bottom - other.rect.top) < 5:
                                block.falling = False
                            if block.vy > 0 and abs(block.rect.top - other.rect.bottom) < 5:
                                other.falling = True
                                other.vy += block.vy // 2
                if pygame.sprite.collide_mask(block, self.bird):
                    block.rect.midbottom = (block.rect.midbottom[0] + self.bird.vx*2 + 30,
                                            block.rect.midbottom[1])
                    self.bird.rect.midbottom = (45, 315)
                    self.bird.move = False
                    block.angle -= 1
                    block.hit += 1
                    reward+=5
                if block.hit >= 2:
                    block.kill()
                if 270 < block.angle < 360:
                    block.rotate()
                block.fall()

            # ציפור נופלת לקרקע — אפס
            if self.bird.rect.midbottom[1] > 400:
                self.bird.rect.midbottom = (45, 315)
                self.bird.move = False

            # אם אין עוד חזירים — שלב נגמר / קבוצה הושמדה
            if len(self.pigs) == 0:
                # תגמול גדול על סיום שלב
                reward += +50
                # אפשר גם להכין מעבר לשלב/איפוס — תלוי איך אתה רוצה RL
                done = True
            # או אם נגמרו הניסיונות
            elif self.tries <= 0:
                done = True
                # אפשר עונש קטן על כישלון
                reward += -30

            # … כל לוגיקה נוספת שאתה רוצה: לדוגמה time penalty, נזק, יכולת ירייה מחדש, וכו׳

            # בסוף: קבל מצב חדש
        next_state = self.state
        return next_state, reward, done
    
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
    
    def reset(self):
        # אתחל את הסביבה מחדש
        self.level = 1
        self.tries = 3
        self.pigs.empty()
        self.blocks.empty()
        # אתחל HUD / ריסט של bird
        self.bird = Bird()
        # אתחול מחדש של stage/level
        self.init_level(self.level)
        # אם צריך — גם אתחול של display / screen
        # self.init_display()  # תלוי אם אתה רוצה לפתוח חלון מחדש
        # החזר וקטור מצב התחלתי  
        return self.state()
    def is_win(self):
        if len(self.pigs)==0: return True
        return False