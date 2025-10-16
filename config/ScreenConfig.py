import pygame

class ScreenConfig:

    def __init__(self):
        pass

    def set_dimension(self, width=500, height=500):
        self.width = width
        self.height = height
        return (width if width != self.width else self.width, 
                height if height != self.height else self.height)
    
    def set_background(self, color=pygame.Color(200, 200, 200, 255)):
        self.color_base = color
        return self.color_base
    
    def set_caption(self, caption):
        pygame.display.set_caption(caption)
    
    def init_screen(self, width, height):
        return pygame.display.set_mode(self.set_dimension(width, height))