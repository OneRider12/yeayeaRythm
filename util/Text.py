import pygame
from pygame import Surface

from util.Gradient import Gradient

class Text:
    def __init__(self, text, color, screen:pygame.Surface, position):
        self.text = text
        self.color = color
        self.screen = screen
        self.position = position

        font_path = "assets/fonts/PixelifySans-VariableFont_wght.ttf"
        try:
            self.font = pygame.font.Font(font_path, 48)
        except pygame.error:
            print(f'Error: Could not load font from {font_path}')
            pygame.quit()
            exit()

        '''
        # Gradient ({stop1 : (r1,g1,b1)}, {stop2 : (r2,g2,b2)}, {stop3 : (r3,g3,b3)}) (max and only 3 stops)
        # Example:
        self.gradient = {
            0.23 : (191, 191, 191),
            0.56 : (255, 254, 224),
            1.0 : (255, 255, 241)
        }
        '''

        self.create_text_surface()


    def __check_gradient(self, dimension:tuple, text_surface:pygame.Surface):
        if isinstance(dict, self.color):
            gradient_surface = Gradient(self.color, dimension)
            text_surface.blit(gradient_surface, (0, 0), special_flags=pygame.BLEND_MULT)
            return None
        else:
            return text_surface

    def create_text_surface(self): # Not surely checking
        text_surface = self.font.render(self.text, True, pygame.Color(255, 255, 255))
        text_dimension = text_surface.get_size()
        try:
            if isinstance(self.__check_gradient(text_dimension, text_surface), pygame.Surface):
                self.screen.blit(text_surface, self.position)
            else:
                return
        except pygame.error:
            print(f'ERROR : Blit Text')
