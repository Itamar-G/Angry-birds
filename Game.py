import pygame
import sys
from Environment import Environment
from Graphic import *
import torch
from Human_agent import Human_agent
from ai_agent import DQN_Agent
PATH = "Data/DQN_PARAM_Advanced_2.pth"

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
    #player = Human_agent()
    player = DQN_Agent(parametes_path=PATH)
    run = True

    while run:
        pygame.event.pump()
        events = pygame.event.get()
        for event in events:
            
            if event.type == pygame.QUIT:
                run = False

        if not env.bird.move:
            action = player.get_action(env.state)

        env.render()
        env.move(action)

        if env.end_of_game():
            run = False

    pygame.quit()
    sys.exit()
if __name__=='__main__': main()