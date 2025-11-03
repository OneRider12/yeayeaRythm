import pygame

from config.BoxConstant import BASE_SPEED, __ADJUSTMENT_EDGE_LINE, ADJUSTMENT_MULTI
from config.PageConstant import SCREEN_WIDTH, SCREEN_HEIGHT
from util.Gradient import Gradient


class Box(pygame.sprite.Sprite):
    def __init__(self, dimension, color, position: tuple, size_adj: tuple = (0, 0)):
        super().__init__()
        self.dimension = dimension
        self.color = color

        self.image = None
        self.rect = None
        self.box = None

        # self.__check_isTexting()
        self.__check_color()

        self.create_box(position)

        self.move_speed = BASE_SPEED
        self.vector = (0, 0)

        self.size_adj = size_adj

    def update(self):
        self.__update_pos()
        self.__update_size()

    def __update_pos(self):
        self.rect.x += BASE_SPEED * self.vector[0]
        self.rect.y += BASE_SPEED * self.vector[1]

        if self.rect.top > SCREEN_HEIGHT:
            self.kill()
            print("log: box was killed")

    def __update_size(self):
        # print("__update_size CALLED !!")

        # new_w, new_h = int(self.size_adj[0]), int(self.size_adj[1])
        w, h = self.dimension
        dw, dh = self.size_adj

        new_w = int(w + dw)
        new_h = int(h + dh)

        self.dimension = (new_w, new_h)

        # print((w, h), (dw, dh))

        position = self.rect.center
        self.image = pygame.Surface(self.dimension)
        self.image.fill(self.color)
        self.rect = self.image.get_rect(center=position)

        # print(new_w, new_h)

    def set_vector(self, direction):
        self.vector = direction

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

        return self.box
