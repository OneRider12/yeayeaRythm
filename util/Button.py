import pygame

from util.Box import Box

## NOT IN USE ##
class Button(Box):
    def __init__(self, dimension, color, position:tuple, text:str=None):
        super().__init__(dimension, color, position, text)
        self.dimension = dimension
        self.color = color
        self.text = text

        self.image = None
        self.rect = None
        self.box = None

        # self.__check_isTexting()
        self.__check_color()

        self.create_box(position)

    def onPress(self):
        pass


