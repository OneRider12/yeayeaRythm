import pygame

from util.Gradient import Gradient
from util.Text import Text

class Box:
    def __init__(self, dimension, color, text:str=""):
        self.dimension = dimension
        self.color = color
        self.text = text

        self.image = None
        self.rect = None
        self.box = None

        self.isTexting = self.__check_text()

    def __check_text(self):
        if self.text != "":
            self.font = Text(self.text, self.color)
            return True
        else:
            return False

    def __check_gradient(self):
        if isinstance(dict, self.color):
            self.color = Gradient(self.color, self.dimension)


    # Create Box
    def create_box(self, position, text: str = None):
        self.image = pygame.Surface(self.dimension)
        self.image.fill(self.color)
        self.rect = self.image.get_rect(topleft=position)
        self.box = Box(self.dimension, self.color, self.text)

        if self.isTexting:
            pass

        return self.box

    # Return Sprite (button)
    def create_button(self, position, text: str = None):
        pass
