import pygame

from config.PageConstant import SCREEN_DIMENSION, SCREEN_BACKGROUND


class Screen:
    def __init__(self):
        self.screen = None

    def setup(self, color:pygame.Color, name):
        self.screen = pygame.display.set_mode(SCREEN_DIMENSION)

        pygame.display.set_caption(str(name))
        self.screen.fill(pygame.Color(*SCREEN_BACKGROUND))

        pygame.display.flip()

        return self.screen

    def draw_rect(self, rect:pygame.Rect):
        pass

    # Not in use
    def draw_group(self, group:pygame.sprite.Group):
        pass


    # built-in
    def draw_list(self, axis:str, amount:int, boundary:tuple, coord:tuple):
        pass

    # Not in use
    def draw_button(self, color, dimension:tuple, coord:tuple):
        pass

    # Not in use
    def draw_text(self, text:str, color, dimension:tuple, coord:tuple):
        pass

