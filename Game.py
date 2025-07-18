import pygame
from Bird import Bird
from Graphic import *
import sys 
from Block import Block
from Environment import Environment
from Human_agent import Human_agent


def main():
    env = Environment()
    env.init_display()
    player = Human_agent()
    run = True

    while run:
        pygame.event.pump()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                run = False

        if not env.bird.move:
            action = player.get_action(env.bird.rect.midbottom, events)

        env.render()
        env.move(action)

        if env.end_of_game():
            run = False

    pygame.quit()
    sys.exit()
if __name__=='__main__': main()