import pygame
from util.Box import Box

class ItemList(Box):
    def __init__(self, dimension, color, text:str=""):
        super().__init__(self, dimension, color, text)

    # Return Sprite (box)
    def create_box(self, position, text: str = None):
        return self.rect

    # Return Sprite (button)
    def create_button(self, position, text: str = None):
        pass