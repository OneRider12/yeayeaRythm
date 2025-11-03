import pygame.font

class Text:
    def __init__(self, text:str, color, dimension:tuple, coord:tuple, font_size:int=30):
        self.text = text
        self.color = color
        self.dimension = dimension
        self.coord = coord
        self.font_size = font_size

        self.font = pygame.font.SysFont(None, self.font_size)
        self.rendered_text = self.font.render(self.text, True, self.color)

    def draw(self, surface:pygame.Surface):
        surface.blit(self.rendered_text, self.coord)
