import pygame

class Screen:
    def __init__(self):
        pass

    def setup(self, dimension, color, name):
        screen = pygame.display.set_mode(dimension)
        pygame.display.set_caption(str(name))
        screen.fill(pygame.Color(100, 200, 250))
        return screen

    def draw_surface(self, surface:pygame.Surface):
        pass

    def draw_group(self, group:pygame.sprite.Group):
        pass


    # built-in
    def draw_list(self, axis:str, amount:int, boundary:tuple, coord:tuple):
        pass

    def draw_button(self, color, dimension:tuple, coord:tuple):
        pass

    def draw_text(self, text:str, color, dimension:tuple, coord:tuple):
        pass

