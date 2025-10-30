import pygame

class FontConfig:

    def __init__(self, ):
        self.font = self.set_font()


    def set_font(self):
        self.font = pygame.font.SysFont("Courier New", 48)
        return self.font