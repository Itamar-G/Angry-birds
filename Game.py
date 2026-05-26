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
    font_title = pygame.font.SysFont("Arial", 60, bold=True)
    font_button = pygame.font.SysFont("Arial", 40)
    
    # הגדרת כפתורים
    human_rect = pygame.Rect(WIDTH//2 - 150, HEIGHT//2 - 20, 300, 60)
    ai_rect = pygame.Rect(WIDTH//2 - 150, HEIGHT//2 + 60, 300, 60)
    
    while True:
        screen.fill((30, 30, 30)) # רקע כהה לתפריט
        
        title_text = font_title.render("ANGRY BIRDS", True, (255, 255, 255))
        screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, 80))
        
        # ציור כפתורים
        pygame.draw.rect(screen, (50, 150, 50), human_rect, border_radius=10)
        pygame.draw.rect(screen, (50, 50, 150), ai_rect, border_radius=10)
        
        human_text = font_button.render("Human Player", True, (255, 255, 255))
        ai_text = font_button.render("AI Agent", True, (255, 255, 255))
        
        screen.blit(human_text, (human_rect.centerx - human_text.get_width()//2, human_rect.centery - human_text.get_height()//2))
        screen.blit(ai_text, (ai_rect.centerx - ai_text.get_width()//2, ai_rect.centery - ai_text.get_height()//2))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if human_rect.collidepoint(event.pos):
                    return "HUMAN"
                if ai_rect.collidepoint(event.pos):
                    return "AI"

def show_game_over(screen, final_score):
    """מציג מסך סיום וחזרה לתפריט"""
    screen.fill((0, 0, 0))
    font = pygame.font.SysFont("Arial", 50)
    msg = font.render("GAME OVER", True, (255, 0, 0))
    score_msg = font.render(f"Final Score: {final_score}", True, (255, 255, 255))
    info_msg = pygame.font.SysFont("Arial", 20).render("Returning to Menu...", True, (150, 150, 150))
    
    screen.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT//2 - 60))
    screen.blit(score_msg, (WIDTH//2 - score_msg.get_width()//2, HEIGHT//2))
    screen.blit(info_msg, (WIDTH//2 - info_msg.get_width()//2, HEIGHT//2 + 80))
    
    pygame.display.flip()
    pygame.time.wait(3000)
    # כאן אנחנו לא עושים sys.exit() כדי שנוכל לחזור לתפריט

def main():
    env = Environment()
    env.init_display()
    font = pygame.font.SysFont("Arial", 32)
    
    while True: # לולאה אינסופית שמאפשרת חזרה לתפריט אחרי הפסד
        mode = show_menu(env.screen)
        
        if mode == "HUMAN":
            player = Human_agent()
        else:
            player = DQN_Agent(parametes_path=PATH, env=env)
            
        env.score = 0
        env.level = 1
        game_active = True

        while game_active:
            env.init_level(env.level)
            level_active = True
            
            while level_active:
                pygame.event.pump()
                
                # תצוגה
                env.render()
                score_text = font.render(f"Score: {env.score}  Level: {env.level}  Tries: {env.tries}", True, (255, 255, 255))
                env.screen.blit(score_text, (10, 10))
                pygame.display.flip()

                # עדכון פיזיקה
                env.move(None)

                # החלטת סוכן/שחקן
                if env.is_stable() and not env.end_of_game():
                    if mode == "AI":
                        state_T = env.get_state().toTensor(env)
                        action = player.get_action(state_T, train=False)
                    else:
                        action = player.get_action((45,315))
                    
                    if action is not None:
                        env.move(action)

                # בדיקת סיום שלב
                if env.end_of_game():
                    if len(env.pigs) == 0:
                        # ניצחון בשלב
                        bonus = env.calculate_win_bonus()
                        env.score += bonus
                        env.level += 1
                        pygame.time.wait(1000)
                        level_active = False 
                    else:
                        # הפסד
                        show_game_over(env.screen, env.score)
                        level_active = False
                        game_active = False # חוזר ללולאה של ה-Menu

if __name__=='__main__': 
    main()