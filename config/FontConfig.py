import pygame

from config.FontConstant import FONT_PATH, FONT_DIGIT_PATH


class FontConfig:

    def __init__(self, size, isDigit):
        self.size = size
        self.isDigit = isDigit
        self.font = self.__set_font()

    def __set_font(self):
        try:
            if not self.isDigit:
                font = pygame.font.Font(FONT_PATH, self.size)
            else:
                font = pygame.font.Font(FONT_DIGIT_PATH, self.size)
        except pygame.error as e:
            print(f"Error loading font: {e}")
            font = pygame.font.Font(None, self.size)

        return font