import pygame
from Bird import Bird
from Graphic import *
import sys 
from Block import Block
pygame.init()
screen=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Angry birds")
clock=pygame.time.Clock()
background=pygame.image.load("img/background.webp")
background=pygame.transform.scale(background,(WIDTH,HEIGHT))
#pygame.draw.line(background,color=BROWN,start_pos=(600,250),end_pos=(600,355),width=20)
block=Block((200,200),(200,300))
block.Draw(background)
rug=pygame.image.load("img/rug.png")
rug=pygame.transform.scale(rug,(60,60))

red_bird=Bird()
pig=pygame.image.load("img/pig.webp")
pig=pygame.transform.scale(pig,(40,40))
background.blit(rug,(10,296))
background.blit(pig,(580,210))
red_bird.Draw(background)
screen.blit(background,(0,0))
def main():
    run=True
    shoot=False
    move=False
    vx=0
    vy=0
    while(run):
        events=pygame.event.get()
        for event in events:
            if event.type==pygame.QUIT: run=False
            if event.type==pygame.MOUSEBUTTONDOWN:
                shoot = True
                p1=event.pos
            if event.type == pygame.MOUSEBUTTONUP and shoot:
                vx,vy=red_bird.Shoot(p1,event.pos)
                shoot=False
                move=True
            if move:
                red_bird.Move(vx,vy)
                vy=vy+1
            if red_bird.rect.midbottom[1]>400 or red_bird.rect.midbottom[0]>700:
                move=False
                red_bird.rect.midbottom=(45,315)
        background=pygame.image.load("img/background.webp")
        background=pygame.transform.scale(background,(WIDTH,HEIGHT))
        #pygame.draw.line(background,color=BROWN,start_pos=(600,250),end_pos=(600,355),width=20)
        block.Draw(background)
        background.blit(rug,(10,296))
        background.blit(pig,(580,210))
        red_bird.Draw(background)
        screen.blit(background,(0,0))
        pygame.display.update()
        clock.tick(FPS)
if __name__=='__main__': main()