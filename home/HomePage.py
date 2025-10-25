import pygame

from util.Screen import Screen
from util.ItemList import ItemList

pygame.init()

class HomePage(Screen):
    def __init__(self):
        super().__init__()
        color = pygame.Color(100, 100, 100)
        self.setup((1200, 800), pygame.color.Color(100, 200, 250), "Home - YeaYeaRythm")

        self.clock = pygame.time.Clock()
        self.clock.tick(60)

        self.isRunning = True

    def setupp(self, dimension, color:tuple, name):
        screen = pygame.display.set_mode(dimension)
        pygame.display.set_caption(str(name))
        screen.fill(pygame.Color(color[0], color[1], color[2]))
        # return screen


    # def draw_ui(self):
    #     ui = ItemList()
    #     draw_surface()


    def run(self):
        while self.isRunning:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.isRunning = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.isRunning = False


