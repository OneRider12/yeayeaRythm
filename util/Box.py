import pygame

from config.BoxConstant import BASE_SPEED, __ADJUSTMENT_EDGE_LINE, ADJUSTMENT_MULTI
from config.PageConstant import SCREEN_WIDTH, SCREEN_HEIGHT
from util.Gradient import Gradient


class Box(pygame.sprite.Sprite):
    def __init__(self, dimension, color, position: tuple, alignment:str=""):
        super().__init__()
        self.dimension = dimension
        self.color = color
        self.alignment = alignment

        self.image = None
        self.rect = None
        self.box = None

        self.__check_color()

        self.create_box(position)

        # Moving
        self.move_speed = BASE_SPEED
        self.vector = (0, 0)
        # For linear moving
        self.add_x = 0
        self.add_y = 0

        # Resizing
        self.size_adj = (0, 0)
        self.ratio = ()

        self.id = int()

    def __str__(self):
        return f'{self.id}'

    def update(self):
        self.__update_pos()
        self.__update_size()

    def __update_pos(self):
        self.add_x = float(BASE_SPEED * self.vector[0])
        self.add_y = float(BASE_SPEED * self.vector[1])

        self.rect.x += self.add_x
        self.rect.y += self.add_y

        # print(self.rect.x, self.rect.y)

        if self.rect.top > SCREEN_HEIGHT:
            self.kill()
            # print("log: box was killed")

    # def __update_size(self):
    #     w, h = self.dimension
    #     dw, dh = self.size_adj
    #
    #     # 1. Calculate and update precise float dimension state
    #     new_w_float = w + dw
    #     new_h_float = h + dh
    #
    #     # Prevent size from becoming zero or negative
    #     if new_w_float <= 1 or new_h_float <= 1:
    #         self.kill()
    #         return
    #
    #     self.dimension = [new_w_float, new_h_float]  # Update float state
    #
    #     # 2. CRITICAL FIX: Get the current anchor point position
    #     # If self.alignment is "midleft", this retrieves self.rect.midleft
    #     position = getattr(self.rect, self.alignment)
    #
    #     # 3. CRITICAL FIX: Re-create surface with int() and SRCALPHA
    #     new_w_int, new_h_int = int(new_w_float), int(new_h_float)
    #     self.image = pygame.Surface((new_w_int, new_h_int), pygame.SRCALPHA)
    #
    #     # 4. FIX: Handle Gradient or solid color fill
    #     self.image.fill(self.color)
    #
    #     # 5. FIX: Re-calculate rect using the specific anchor point
    #     # This is equivalent to: self.rect = self.image.get_rect(midleft=position)
    #     self.rect = self.__check_rect(self.alignment, position)

    def __update_size(self):
        w, h = self.dimension
        if self.ratio != ():
            self.dimension = (w, h)
        else:
            dw, dh = self.size_adj

            new_w = float(w + dw)
            new_h = float(h + dh)

            self.dimension = (new_w, new_h)

            if self.alignment == "midleft":
                position = self.rect.midleft
            elif self.alignment == "midright":
                position = self.rect.midright
            elif self.alignment == "topleft":
                position = self.rect.topleft
            elif self.alignment == "topright":
                position = self.rect.topright
            elif self.alignment == "bottomleft":
                position = self.rect.bottomleft
            elif self.alignment == "bottomright":
                position = self.rect.bottomright
            elif self.alignment == "center":
                position = self.rect.center
            else:
                position = self.rect.center


            self.image = pygame.Surface((int(new_w), int(new_h)), pygame.SRCALPHA)
            self.image.fill(self.color)
            self.rect = self.__check_rect(self.alignment, position)

    def set_vector(self, direction):
        self.vector = direction

    def __check_color(self):
        if isinstance(self.color, dict):
            self.color = Gradient(self.color, self.dimension)  # Dict to Gradient
        elif isinstance(self.color, tuple):
            self.color = pygame.Color(*self.color)  # Tuple to Color
        else:
            self.color = self.color  # Already Color

    def __check_rect(self, alignment, position):
        if alignment == "midleft":
            return self.image.get_rect(midleft=position)
        elif alignment == "midright":
            return self.image.get_rect(midright=position)
        elif alignment == "topleft":
            return self.image.get_rect(topleft=position)
        elif alignment == "topright":
            return self.image.get_rect(topright=position)
        elif alignment == "bottomleft":
            return self.image.get_rect(topleft=position)
        elif alignment == "bottomright":
            return self.image.get_rect(topright=position)
        elif alignment == "center":
            return self.image.get_rect(center=position)
        else:
            return self.image.get_rect(center=position)

    # Create Box
    def create_box(self, position: tuple):
        self.image = pygame.Surface(self.dimension, pygame.SRCALPHA)
        self.image.fill(self.color)
        self.rect = self.__check_rect(self.alignment, position)

        return self.box

    def isCollide(self, box_rect):
        return pygame.Rect.colliderect(self.rect, box_rect)

# class Rect(pygame.rect.Rect):
#     def __init__(self, dimenion, position, alignment:str=""):
#         super().__init__()



