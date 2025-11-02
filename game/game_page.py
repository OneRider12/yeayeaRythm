import pygame
from config.ScreenConfig import ScreenConfig
from config.FontConfig import FontConfig
from config.ColorConfig import ColorConfig
from config.screen import Screen


class Game(Screen):

    def __init__(self, width, height):
        self.screen = Screen()
        self.color = ColorConfig()

        self.setupScreen(
            (width, height), self.color.vibrant("LIME", 255), "Hello test test")

        self.clock = pygame.time.Clock()
        self.clock.tick(60)

        self.isRunning = True

    def setupScreen(self, dimension : tuple, color : pygame.Color, caption : str):
        self.screen = Screen()
        self.screen.setup(dimension, color, caption)
        width = dimension[0]
        height = dimension[1]
        self.screen.draw_list("H",
                              4,
                              (width * 0.8, height * 0.1),
                              (width * 0.5, height * 0.7),
                              self.color.pastel("pink", 255)
                              )
        

    def run(self):
        while self.isRunning:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.isRunning = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.isRunning = False
            # pygame.display.update()
