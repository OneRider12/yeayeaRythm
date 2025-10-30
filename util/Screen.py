import pygame

class Screen:
    def __init__(self):
        self.screen = None
        pass

    def setup(self, dimension, color:pygame.Color, name):
        self.screen = pygame.display.set_mode(dimension)
        pygame.display.set_caption(str(name))
        self.screen.fill(color)
        pygame.display.flip()
        return self.screen

    def draw_rect(self, rect:pygame.Rect):
        pygame.display.update(rect)

    def draw_group(self, group:pygame.sprite.Group):
        pass


    # built-in
    def draw_list(self, axis:str, amount:int, boundary:tuple, coord:tuple):
        pass

    def draw_button(self, color, dimension:tuple, coord:tuple):
        pass

    def draw_text(self, text:str, color, dimension:tuple, coord:tuple):
        pass

