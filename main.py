import pygame

from config.song_dir import *
# from game.GamePage import GamePage
from game.GamePage2 import GamePage
# from game.Game_Gemini import GamePage
# from home.HomePage import HomePage
from credits.CreditsPage import CreditsPage

class GameInstance:
    def __init__(self):
        pygame.init()
        self.instance = GamePage(SONG03_JSON_DIR)
        self.instance.run()

if __name__ == "__main__":
    gameInstance = GameInstance()