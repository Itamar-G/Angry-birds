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
                vx=(pos[0]-pos2[0])/2
                vy=(pos[1]-pos2[1])/2
                return vx,vy
        return None