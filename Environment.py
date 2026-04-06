import pygame
from Bird import Bird
from Graphic import *
from Block import Block
from Pig import Pig
import random
from State import State 
import math

class Environment:
    def __init__(self):
        self.bird = Bird()
        self.pigs = pygame.sprite.Group()
        self.blocks = pygame.sprite.Group()
        self.tries = 3
        self.level = 1
        self.screen = None
        self.reward=0
        self.steps_since_shot = 0

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

        num_buildings = random.randint(1, 3)  

        for _ in range(num_buildings):
            x = random.randint(250, 600)
            num_floors = random.randint(1, 3)
            
            # משתנה שיעזור לנו לדעת מה הגובה המצטבר של המבנה
            current_top_y = 360 

            for i in range(num_floors):
                is_horizontal = random.random() < 0.3
                width = 60 if is_horizontal else 20
                height = 20 if is_horizontal else 60
                
                # מיקום הבלוק: התחתית שלו היא ה-top של הקומה הקודמת
                block = Block((x, current_top_y), width=width, height=height)
                self.blocks.add(block)
                
                # עדכון הגובה לקומה הבאה
                current_top_y -= height

            # מיקום החזיר: בדיוק על הגג של הקומה האחרונה
            # current_top_y כרגע מייצג את ה-top של הבלוק העליון ביותר
            self.init_pigs((x, current_top_y))

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

    def calculate_ballistic_distance(self,x0, y0,action, x, y):
        vx=(action[0] + 1) * 5
        vy=(action[1] - 1) * (-5)
        yp=y0+vy*(x-x0)/vx +0.5*((x-x0)**2)/vx**2
        if abs(y-yp)<1: return 1
        return abs(y-yp)
        
    def get_state(self):
        state=State()
        state.toTensor(self)
        return state
    def force_stabilize_blocks(self):
        for block in self.blocks:
            # מציאת הזווית הקרובה ביותר בקפיצות של 90 מעלות
            current_angle = block.angle % 360
            snapped_angle = round(current_angle / 90) * 90
            block.angle = snapped_angle
            
            # איפוס מהירויות פיזיקליות
            block.vy = 0
            block.falling = False

    def move(self, action):
        # — אם יש פעולה (action לא None) — בצע ירייה / התחל תנועה
        
        done = False
        pigs_num_before_step = len(self.pigs) # כמות החזירים בתחילת הצעד הנוכחי
        
        if action is not None:
            if not self.bird.move:
                # שמירת כמות החזירים ברגע הירייה כדי לבדוק פגיעה בהמשך
                pigs_before_shot = len(self.pigs)
                
                self.bird.vx = (action[0] + 1) * 3
                self.bird.vy = (action[1] - 1) * (-5)
                self.bird.move = True
                
                # הורדת ניקוד על עצם הירייה (כפי שהיה בקוד שלך)
                self.reward -= 1 
                self.tries -= 1
                
                for pig in list(self.pigs):
                    self.reward += 2 / self.calculate_ballistic_distance(45, 315, action, pig.rect.midbottom[0], pig.rect.midbottom[1])

        # תנועת הציפור
        if self.bird.move:
            check = True
            for block in list(self.blocks):
                if 270 < block.angle < 360:
                    check = False
            if check:
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
            if pig.rect.bottom >= 360:
                pig.stay = True
                pig.kill()
                self.reward += 50

        # --- עדכון בלוקים: לוגיקת נפילה משופרת ---
        
        # שלב א': נמיין את הבלוקים מלמטה למעלה (לפי Y) כדי שנוכל לבדוק יציבות מהקרקע מעלה
        sorted_blocks = sorted(list(self.blocks), key=lambda b: b.rect.bottom, reverse=True)
        
        for block in sorted_blocks:
            # נניח בתחילה שהבלוק נופל
            block.falling = True
            
            # אם הבלוק על הרצפה - הוא יציב
            if block.rect.bottom >= 360:
                block.rect.bottom = 360 # הצמדה לרצפה
                block.falling = False
            else:
                # אם הוא לא על הרצפה, נבדוק אם הוא יושב על בלוק אחר שכבר קבענו שהוא לא נופל
                for other in sorted_blocks:
                    if block is other or other.falling:
                        continue # אי אפשר להישען על בלוק שבעצמו נופל
                    
                    # בדיקה אם התחתית של הבלוק הנוכחי נוגעת בחלק העליון של הבלוק השני
                    if pygame.sprite.collide_mask(block, other):
                        # בדיקה שהבלוק מעל השני (עם טווח טעות קטן)
                        if abs(block.rect.bottom - other.rect.top) < 10:
                            block.falling = False
                            # הצמדה מדויקת כדי למנוע "רעידות"
                            block.rect.bottom = other.rect.top
                            break

            # הרצת הנפילה/סיבוב הפיזיקלי
            if block.falling:
                block.fall()
            else:
                block.vy = 0 # איפוס מהירות אם הוא יציב

            # טיפול בהתנגשות עם הציפור (נשאר דומה)
            if pygame.sprite.collide_mask(block, self.bird):
                for pig in list(self.pigs):
                    if pygame.sprite.collide_mask(block, pig):
                        self.reward += 7
                block.rect.midbottom = (block.rect.midbottom[0] + self.bird.vx * 2 + 30,
                                        block.rect.midbottom[1])
                # סימון הבלוק שיתחיל ליפול/להסתובב אחרי המכה
                block.angle -= 1 
                block.hit += 1
                self.bird.rect.midbottom = (45, 315)
                self.bird.move = False
                self.reward+=3

            # סיבוב בלוקים פגועים
            if 270 < block.angle < 360:
                block.rotate()
            
            if block.hit >= 2:
                block.kill()    

        if not self.is_stable():
            self.steps_since_shot += 1
        # בדיקה אם עבר יותר מדי זמן ללא התייצבות
        if self.steps_since_shot > 100:
            self.force_stabilize_blocks()
            self.bird.move = False
            self.bird.rect.midbottom = (45, 315)
            self.steps_since_shot = 0        
        # ציפור נופלת לקרקע (פספוס מוחלט)
        if self.bird.rect.midbottom[1] > 400 or self.bird.rect.midbottom[0] > 700:
            if hasattr(self, 'pigs_before_shot'):
                if len(self.pigs) == pigs_before_shot:
                    self.reward -= 20 # קנס על ירייה שלא פגעה בחזיר ויצאה מהמסך
                delattr(self, 'pigs_before_shot')
            
            self.bird.rect.midbottom = (45, 315)
            self.bird.move = False

        next_state = self.get_state()
        # חישוב בונוס על חזירים שנהרגו בפריים הזה
        self.reward += (pigs_num_before_step - len(self.pigs)) * 100
        if self.end_of_game(): 
            done = True
        if done and len(self.pigs) == 0:
            self.reward += 200 + (self.tries * 50) # בונוס על יריות שנשארו
        if self.tries == 0 and len(self.pigs) > 0: 
            self.reward = -300
        normalized_reward = max(min(self.reward, 5), -5)     
        return normalized_reward, done
    
    def is_stable(self):
        # בדיקה אם הציפור בתנועה
        if self.bird.move:
            return False
        # בדיקה אם יש חזיר שנופל
        for pig in self.pigs:
            if not pig.stay:
                return False
        # בדיקה אם יש בלוק שנופל או מסתובב
        for block in self.blocks:
            if block.falling or (block.angle < 360 and block.angle > 270):
                return False
        return True
    
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
        if len(self.pigs)==0:
            self.reward=0
            return True
        if self.tries==0: 
            self.reward=0
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
        return self.get_state()
    def is_win(self):
        if len(self.pigs)==0: return True
        return False