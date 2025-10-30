import pygame

class PageConfig:
    def __init__(self, page):
        self.name = None
        self.background = None
        self.dimension = None



    def home(self):
        self.dimension = (1200, 800)
        self.background = pygame.Color(100, 200, 250)
        self.name = "Home - YeaYeaRythm"
