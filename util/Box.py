import pygame

from config.BoxConstant import BASE_SPEED
from config.PageConstant import SCREEN_WIDTH, SCREEN_HEIGHT
from util.Gradient import Gradient
from util.Text import Text


class Box(pygame.sprite.Sprite):
    def __init__(self, dimension, color, position: tuple, text: pygame.sprite.Sprite = None):
        super().__init__()
        self.dimension = dimension
        self.color = color
        self.text = text

        self.image = None
        self.rect = None
        self.box = None

        self.__check_isTexting()
        self.__check_color()

        self.create_box(position)

        self.move_speed = BASE_SPEED
        self.vector = (0, 0)

    def update(self):
        self.__update_pos()
        self.__update_size()

    def __update_pos(self):
        self.rect.x += BASE_SPEED * self.vector[0]
        self.rect.y += BASE_SPEED * self.vector[1]

        if self.rect.bottom > SCREEN_HEIGHT:
            self.kill()

    def __update_size(self):
        multiplier = 1
        w, h = self.dimension
        self.dimension = (w * multiplier, h * multiplier)

    def set_vector(self, direction):
        self.vector = direction

    # Check State
    def __check_isTexting(self):
        self.isTexting = isinstance(self.text, str)

    def __check_color(self):
        if isinstance(self.color, dict):
            self.color = Gradient(self.color, self.dimension)  # Dict to Gradient
        elif isinstance(self.color, tuple):
            self.color = pygame.Color(*self.color)  # Tuple to Color
        else:
            self.color = self.color  # Already Color

    # Create Box
    def create_box(self, position: tuple):
        self.image = pygame.Surface(self.dimension)
        self.image.fill(self.color)
        self.rect = self.image.get_rect(center=position)
        # self.box = Box(self.dimension, self.color, self.text)

        # if self.isTexting:
        #     pass

        # self.create_center_text(position)

        return self.box

    # Add centered Text in Box
    # def create_center_text(self, position):
    #     if self.text is None:
    #         pass
    #     else:
    #         self.text.rect = self.image.get_rect(center=position)
