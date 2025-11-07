import pygame
# from config.song_dir import SONG01_JSON_DIR

from credits.CreditsPage import CreditsPage
from leaderboard.LeaderPage import LeaderPage
from home.HomePage import HomePage
from game.GamePage import GamePage
import sys, os
sys.path.append(os.path.dirname(__file__))

class GameInstance:
    def __init__(self):
        pygame.init()

        # ✅ สร้างหน้าจอหลักก่อน
        self.screen = pygame.display.set_mode((800, 1200))
        pygame.display.set_caption("My Game")

        # ✅ ส่งหน้าจอให้ CreditsPage
        self.instance = LeaderPage(self.screen)
        # self.instance = LeaderPage(self.screen)  # ใช้ตอนสลับหน้าอื่นได้

        # ✅ เรียกใช้งานหน้า
        self.instance.run()

if __name__ == "__main__":
    gameInstance = GameInstance()
