import pygame
from Bird import Bird
from Graphic import *
import sys 
from Block import Block
from Environment import Environment
from Human_agent import Human_agent
import time

def show_game_over(screen):
    font = pygame.font.SysFont("Arial", 60)
    text = font.render("GAME OVER", True, (255, 0, 0))
    rect = text.get_rect(center=(screen.get_width()//2, screen.get_height()//2))

    screen.fill((0, 0, 0))
    screen.blit(text, rect)
    pygame.display.flip()
    pygame.time.wait(1500)  # זמן הצגת Game Over (מילי־שניות)

def main():
    while True:     # לולאה חיצונית – משחק מחדש
        env = Environment()
        env.init_display()
        player = Human_agent()
        run = True

        while run:
            pygame.event.pump()
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if not env.bird.move:
                action = player.get_action(env.bird.rect.midbottom, events)

            env.render()
            env.move(action)

            if env.end_of_game():
                show_game_over(env.screen)  # מציג GAME OVER
                run = False                # יציאה ללולאה החיצונית כדי להתחיל משחק מחדש

        # ממשיך כאן ללולאה החיצונית ומתחיל משחק חדש באופן אוטומטי

if __name__=='__main__':
    main()
