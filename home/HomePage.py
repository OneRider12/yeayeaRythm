import pygame

from util.Box import Box
from util.Screen import Screen
from util.ItemList import ItemList

pygame.init()

class HomePage(Screen):
    def __init__(self):
        super().__init__()

        __dimension = (1200, 800)
        __background = pygame.Color(100, 200, 250)
        __name = "Home - YeaYeaRythm"
        self.screen = self.setup(__dimension, __background, __name)

        self.clock = pygame.time.Clock()
        self.clock.tick(60)

        self.isRunning = True

        self.box = Box((100, 120), (255, 255, 100))


    def draw_ui(self):
        pygame.draw.rect(self.screen, self.box.color, self.box.rect) # This is how to draw Rect aka Box
        # ui = ItemList()
        # draw_surface()


    def run(self):

        # self.screen.blit(self.box)

        while self.isRunning:
            self.draw_ui()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.isRunning = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.isRunning = False

            self.clock.tick(60)
            pygame.display.flip()
