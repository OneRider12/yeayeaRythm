import pygame
from home.home_page_test import Home
from game.game_page import Game
from config.ScreenAttribute import ScreenAttribute
from config.screen import Screen


class Start:
    def __init__(self):
        pygame.init()
        pass

    def run(self):
        self.width = Screen().width
        self.height = Screen().height

        self.home = Game(self.width, self.height)
        self.home.run()

        # screenAttribute = ScreenAttribute()
        # textAttribute = TextAttribute()
        


if __name__ == "__main__":
    instance = Start()
    instance.run()