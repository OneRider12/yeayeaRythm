import pygame

from game.GamePage import GamePage
from home.HomePage import HomePage
from credits.CreditsPage import CreditsPage

class GameInstance:
    def __init__(self):
        pygame.init()
        self.instance = HomePage()
        self.instance.run()

if __name__ == "__main__":
    gameInstance = GameInstance()