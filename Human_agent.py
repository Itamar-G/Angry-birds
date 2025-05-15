import pygame
class Human_agent:
    def __init__(self):
        pass
    def get_action (self,events=None,state=None):
        
        for event in events:
            # if event.type==pygame.MOUSEBUTTONDOWN:
            #     self.p1=pygame.mouse.get_pos()
            
            if event.type==pygame.MOUSEBUTTONUP:
                return pygame.mouse.get_pos()
                
        return None