import pygame

from config.EngineConfig import EngineConfig
from config.PageConstant import SCREEN_BACKGROUND, HOME_TITLE
from util.Box import Box
from util.Screen import Screen
from util.ItemList import ItemList


class HomePage(Screen, EngineConfig):
    def __init__(self):
        Screen().__init__()
        EngineConfig.__init__(self)

        self.screen = self.setup(SCREEN_BACKGROUND, HOME_TITLE)

        self.box = Box((100, 120), (255, 255, 100))

        self.static_ui = pygame.sprite.Group()
        self.dynamic_ui = pygame.sprite.Group()

    def draw_rect(self, rect:pygame.Rect):
        pygame.draw.rect(self.screen, self.box.color, rect) # This is how to draw Rect aka Box

    # def draw_ui(self):
        # ui = ItemList()
        # draw_surface()

    def run(self):
        while self.isRunning:
            self.draw_rect(self.box.rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.isRunning = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.isRunning = False

            self.clock.tick(60)
            pygame.display.flip()
