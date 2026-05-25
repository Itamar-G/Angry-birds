import pygame
import sys
from Environment import Environment
from Graphic import *
import torch
from Human_agent import Human_agent
from ai_agent import DQN_Agent
from State import State
PATH = "Data/DQN_PARAM_Advanced_11.pth"

def show_menu(screen):
    font = pygame.font.SysFont("Arial", 40)
    title_font = pygame.font.SysFont("Arial", 60, bold=True)
    
    # הגדרת כפתורים
    human_button = pygame.Rect(WIDTH // 2 - 150, 150, 300, 60)
    ai_button = pygame.Rect(WIDTH // 2 - 150, 250, 300, 60)
    
    while True:
        screen.fill((30, 30, 30))  # רקע כהה
        
        # כותרת
        title = title_font.render("ANGRY BIRDS AI", True, (255, 255, 255))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))
        
        # ציור כפתורים
        pygame.draw.rect(screen, (0, 150, 0), human_button)
        pygame.draw.rect(screen, (0, 0, 150), ai_button)
        
        # טקסט על הכפתורים
        human_text = font.render("Human Player", True, (255, 255, 255))
        ai_text = font.render("AI Agent", True, (255, 255, 255))
        
        screen.blit(human_text, (human_button.centerx - human_text.get_width() // 2, human_button.centery - human_text.get_height() // 2))
        screen.blit(ai_text, (ai_button.centerx - ai_text.get_width() // 2, ai_button.centery - ai_text.get_height() // 2))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if human_button.collidepoint(event.pos):
                    return "HUMAN"
                if ai_button.collidepoint(event.pos):
                    return "AI"
                
def show_game_over_screen(screen, final_score):
    screen.fill((0, 0, 0))
    font = pygame.font.SysFont("Arial", 50)
    msg = font.render("GAME OVER", True, (255, 0, 0))
    score_msg = font.render(f"Final Score: {final_score}", True, (255, 255, 255))
    
    screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(score_msg, (WIDTH // 2 - score_msg.get_width() // 2, HEIGHT // 2 + 20))
    
    pygame.display.flip()
    pygame.time.wait(3000) # מחכה 3 שניות לפני חזרה לתפריט


def main():
    env = Environment()
    env.init_display()
    
    # אתחול הסוכנים
    playerAI = DQN_Agent(parametes_path=PATH, env=env)
    playerHuman = Human_agent() 
    
    font = pygame.font.SysFont("Arial", 32)

    while True: # לולאת תפריט ראשית (מכאן מתחילים אחרי הפסד)
        mode = show_menu(env.screen) # בחירת מצב משחק
        
        env.reset() # איפוס הסביבה (ניקוד, שלב, ניסיונות)
        env.score = 0
        env.level = 1
        game_running = True

        while game_running:
            env.init_level(env.level)
            level_active = True
            
            while level_active:
                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                # תצוגה
                env.render()
                score_text = font.render(f"Mode: {mode} | Score: {env.score} | Level: {env.level} | Tries: {env.tries}", True, (255, 255, 255))
                env.screen.blit(score_text, (10, 10))
                pygame.display.flip()

                # עדכון פיזיקה (תנועת בלוקים/חזירים נופלים)
                env.move(None)

                # החלטת שחקן (רק אם הכל יציב והמשחק לא נגמר)
                if env.is_stable() and not env.end_of_game():
                    if mode == "AI":
                        state_T = env.get_state().toTensor(env)
                        action = playerAI.get_action(state_T, train=False)
                    else:
                        # מצב אנושי - מעבירים את ה-events שקלטנו
                        action = playerHuman.get_action((45, 315), events)
                    
                    if action is not None:
                        env.move(action)

                # בדיקת סיום שלב
                if env.end_of_game():
                    if len(env.pigs) == 0:
                        # ניצחון בשלב!
                        bonus = env.calculate_win_bonus()
                        env.score += bonus
                        env.level += 1
                        pygame.time.wait(1000)
                        level_active = False 
                    else:
                        # הפסד - נגמרו הניסיונות
                        show_game_over_screen(env.screen, env.score)
                        level_active = False
                        game_running = False # שובר את הלולאה וחוזר לתפריט

if __name__ == '__main__':
    main()