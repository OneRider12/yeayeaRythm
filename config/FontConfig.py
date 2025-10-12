import pygame

class FontConfig:

    def __init__(self):
        pass

    def set_font(self):
        self.font = pygame.font.SysFont("Courier New", 48)
        return self.font