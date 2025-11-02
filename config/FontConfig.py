import pygame

from config.FontConstant import FONT_PATH


class FontConfig:

    def __init__(self, size):
        self.size = size
        self.font = self.__set_font()

    def __set_font(self):
        try:
            font = pygame.font.Font(FONT_PATH, self.size)
        except pygame.error as e:
            print(f"Error loading font: {e}")
            font = pygame.font.Font(None, self.size)

        return font