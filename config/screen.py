import pygame
from config.BoxConfig import BoxConfig
from config.ColorConfig import ColorConfig

class Screen:

    # Setup and init screen, width, height

    def __init__(self):
        self.width = 1200
        self.height = 800
        self.dimension = (self.width, self.height)
        
        self.boxConfig = BoxConfig()
        self.color = ColorConfig()

    def setup(self, dimension, color:pygame.Color, name):
        pygame.display.set_caption(name)
        self.screen = pygame.display.set_mode(dimension)
        self.screen.fill(color)
        self.draw_ui(color)
        return self.screen
    
    def draw_ui(self, color, amount = 4):
        self.ui = self.boxConfig.container((self.width / 2, self.height / 2), 
                                           (self.width, self.height))
        
    def draw_list(self, axis:str, amount:int, dimension:tuple, coord:tuple, color):
        if axis.upper() == "V":
            self.list = self.boxConfig.create_list_vertical(amount, coord, dimension, color)
            self.list.draw(self.screen)
        elif axis.upper() == "H":
            self.list = self.boxConfig.create_list_horizontal(amount, coord, dimension, color)
            self.list.draw(self.screen)
            
    # def animate_list(self, axis:str, dimension:tuple, amount:int, coord:tuple, color):
    #     self.draw_list(axis, dimension, amount, coord, color)