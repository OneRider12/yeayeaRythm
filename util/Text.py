import pygame

from config.FontConfig import FontConfig
from util.Gradient import Gradient

class Text(pygame.sprite.Sprite):
    def __init__(self, text: str, size: int, color, screen: pygame.Surface, position):
        super().__init__()
        self.text = text
        self.color = color
        self.screen = screen
        self.position = position

        self.image = None
        self.rect = None

        self.text_surface = None
        self.text_dimension = None

        self.font = FontConfig(size)

        self.create_text_surface()

    def __render_text(self):
        center = self.rect.center
        self.image = self.font.font.render(self.text, True, self.color)
        self.rect = self.image.get_rect(center=center)

    def update_text(self, text):
        str(text)
        self.text = text
        self.__render_text()

    def update_color(self, color):
        self.color = color
        self.__render_text()

    def __check_color(self, dimension):
        if isinstance(self.color, dict):
            text_gradient_surface = Gradient(self.color, dimension) # Dict to Gradient
            self.text_surface.blit(text_gradient_surface, (0, 0), special_flags=pygame.BLEND_MULT)
        else:
            if isinstance(self.color, tuple):
                color = pygame.Color(*self.color)  # Tuple to Color
            else:
                color = self.color  # Already Color

            text_color_surface = pygame.Surface(dimension)
            text_color_surface.fill(color)

            self.text_surface.blit(text_color_surface, (0, 0), special_flags=pygame.BLEND_MULT)

    def create_text_surface(self, alignment="center"):
        white = pygame.Color(255, 255, 255)
        self.text_surface = self.font.font.render(self.text, True, white)
        self.text_dimension = self.text_surface.get_size()

        self.image = self.text_surface
        if alignment == "topleft":
            self.rect = self.image.get_rect(topleft=self.position)
        elif alignment == "center":
            self.rect = self.image.get_rect(center=self.position)

        self.__check_color(self.text_dimension)

