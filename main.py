import pygame

from game.GamePage import GamePage
from home.HomePage import HomePage

class GameInstance:
    def __init__(self):
        pygame.init()
        self.instance = GamePage()
        self.instance.run()

if __name__ == "__main__":
    gameInstance = GameInstance()