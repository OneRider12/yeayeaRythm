import pygame

from util.Gradient import Gradient
from util.Text import Text

class Box:
    def __init__(self, dimension, color, text:str=None):
        self.dimension = dimension
        self.color = color
        self.text = text

        self.image = None
        self.rect = None
        self.box = None

        self.isTexting = True if text else False
        self.color = Gradient(self.color, self.dimension) if isinstance(self.color, dict) else pygame.Color(*self.color) if isinstance(self.color, tuple) else None

        self.create_box()

    # Create Box
    def create_box(self, position=(200, 400)):
        self.image = pygame.Surface(self.dimension)
        self.image.fill(self.color)
        self.rect = self.image.get_rect(topleft=position)
        # self.box = Box(self.dimension, self.color, self.text)

        if self.isTexting:
            pass

        return self.box

    # Return Sprite (button)
    def create_button(self, position, text: str = None):
        pass
