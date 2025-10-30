import pygame

from util.Screen import Screen


class CreditsPage(Screen):
    def __init__(self):
        super().__init__()

        __background = pygame.Color(100, 200, 250)
        __name = "Credits - YeaYeaRythm"
        self.screen = self.setup(__background, __name)




    def run(self):
        pass