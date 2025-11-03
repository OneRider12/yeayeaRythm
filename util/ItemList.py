import pygame
from util.Box import Box

class ItemList(Box):
    def __init__(self, dimension, color, text:str=""):
        super().__init__(self, dimension, color, text)
        self.box = None

    # Return Sprite (box)
    def __create_box(self, dimension, text: str = None):
        box = Box(self.dimension, self.color, text)
        return box.rect

    def list_h(self, dimension:tuple, position:tuple, amount:int):
        box_dimension = ()
        box_rect = self.__create_box(position, )
        pass

    def list_v(self):
        pass

    # Return Sprite (button)
    def create_button(self, position, text: str = None):
        pass