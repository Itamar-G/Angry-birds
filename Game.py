import pygame
import sys
from Environment import Environment
from Graphic import *
import torch
from Human_agent import Human_agent
from ai_agent import DQN_Agent
from State import State
PATH = "Data/DQN_PARAM_Advanced_10.pth"

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
    state=State()
    env.init_display()
    #player = Human_agent()
    player = DQN_Agent(parametes_path=PATH, env=env) # הוספת ה-env כאן
    run = True

    while run:
        pygame.event.pump()
        events = pygame.event.get()
        
        # 1. קודם כל נותנים לפיזיקה לרוץ (נפילת חזירים/בלוקים בתחילת שלב)
        env.render()
        env.move(None) # מריץ עדכון פיזיקלי בלי ירייה

        # 2. רק אם הציפור לא בתנועה והסביבה התייצבה - הסוכן מקבל החלטה
        # בתוך main.py
        if not env.end_of_game() and env.is_stable():
            state=State()
            state_T=state.toTensor(env)
            # אפשר להעביר את ה-env כאן אם לא הגדרת אותו ב-init
            #action = player.get_action((45, 315),events)
            action = player.get_action(state_T, train=False) 
            env.move(action)
            
        # בדיקת סוף משחק
        if env.end_of_game():
            run = False

    pygame.quit()
    sys.exit()
if __name__=='__main__': main()