import pygame

WIDTH,HEIGHT=700,400
FPS=10
BROWN=(180,130,0)
BLACK=(0,0,0)
class graphics:
    def __init__(self):
        pygame.init()
        self.screen=pygame.display.set_mode((WIDTH,HEIGHT))
        self.image=pygame.image.load("img/background.webp")
        self.rug=pygame.image.load("img/rug.png")
        self.image=pygame.transform.scale(self.image,(WIDTH,HEIGHT))
        self.rug=pygame.transform.scale(self.rug,(60,60))
        self.main_surf = pygame.Surface((WIDTH, HEIGHT))
        self.agent=None
    def render(self):
        self.main_surf.blit(self.image,(0,0))
        self.main_surf.blit(self.rug,(10,296))
        self.screen.blit(self.main_surf,(0,0))
        pygame.display.update()
    def draw_agent(self, agent):
        # Draw the agent's image on the screen at the agent's position
        self.screen.blit(agent.image, agent.rect)