import pygame
import sys
from Environment import Environment
from Graphic import *
import torch
from Human_agent import Human_agent
from ai_agent import DQN_Agent
from State import State
PATH = "Data/DQN_PARAM_Advanced_12.pth"

def show_game_over(screen):
    font = pygame.font.SysFont("Arial", 60)
    text = font.render("GAME OVER", True, (255, 0, 0))
    rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))

    screen.fill((0, 0, 0))
    screen.blit(text, rect)
    pygame.display.flip()
    pygame.time.wait(1500)


def main():
    env = Environment()
    env.init_display()
    player = DQN_Agent(parametes_path=PATH, env=env)
    
    font = pygame.font.SysFont("Arial", 32)
    game_running = True

    while game_running:
        # שלב חדש
        env.init_level(env.level)
        level_active = True
        
        while level_active:
            pygame.event.pump()
            
            # תצוגת ניקוד ושלב
            env.render()
            score_text = font.render(f"Score: {env.score}  Level: {env.level}  Tries: {env.tries}", True, (255, 255, 255))
            env.screen.blit(score_text, (10, 10))
            pygame.display.flip()

            # עדכון פיזיקה
            env.move(None)

            # החלטת סוכן
            if env.is_stable() and not env.end_of_game():
                state_T = env.get_state().toTensor(env)
                action = player.get_action(state_T, train=False)
                env.move(action)

            # בדיקת סיום שלב
            if env.end_of_game():
                if len(env.pigs) == 0:
                    # ניצחון בשלב!
                    bonus = env.calculate_win_bonus()
                    env.score += bonus
                    env.level += 1
                    pygame.time.wait(1000) # הפסקה קלה בין שלבים
                    level_active = False 
                else:
                    # הפסד - אין יותר ניסיונות
                    show_game_over(env.screen, env.score)
                    level_active = False
                    game_running = False # יוצא מהלולאה הראשית

    pygame.quit()

def show_game_over(screen, final_score):
    screen.fill((0, 0, 0))
    font = pygame.font.SysFont("Arial", 50)
    msg = font.render("GAME OVER", True, (255, 0, 0))
    score_msg = font.render(f"Final Score: {final_score}", True, (255, 255, 255))
    
    screen.blit(msg, (WIDTH//2 - 100, HEIGHT//2 - 50))
    screen.blit(score_msg, (WIDTH//2 - 120, HEIGHT//2 + 20))
    pygame.display.flip()
    pygame.time.wait(3000)
    pygame.quit()
    sys.exit()
if __name__=='__main__': main()