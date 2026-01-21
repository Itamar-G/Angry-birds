import pygame
class Human_agent:
    def __init__(self):
        pass
    def get_action (self,pos,events=None,state=None):
        
        for event in events:
            # if event.type==pygame.MOUSEBUTTONDOWN:
            #     self.p1=pygame.mouse.get_pos()
            
            if event.type==pygame.MOUSEBUTTONUP:
                pos2= pygame.mouse.get_pos()
                vx=int(((pos[0]-pos2[0])/2)/5)-1
                if vx<0: vx=0
                if vx>9: vx=9
                vy=int(((pos[1]-pos2[1])/2)/(-5))+1
                if vy<0: vy=0
                if vy>9: vy=9
                return vx,vy
        return None