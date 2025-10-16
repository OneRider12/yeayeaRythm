import pygame
from config.FontConfig import FontConfig

class BoxConfig:
    
    def __init__(self):
        pass

    def container(self, coord, dimension):
        self.group = pygame.sprite.Group()
        

    def create_box(self, dimension, color):
        box = pygame.Surface(dimension)
        box.fill(color)
        return box
        

    def create_text(self, text : str, color : tuple):
        self.font = FontConfig().set_font()
        self.text = self.font.render(text, True, color)


    def create_list_horizontal(self, amount, coord, dimension, color):
        hlist = pygame.sprite.Group()

        x_curr = coord[0] - (dimension[0] / 2) # Center - size of one side
        x, y = dimension

        total = amount + 1
        gap = (dimension[0] / total) / (amount-1)
        for i in range(amount):
            box = self.create_box((x / total, y), color)
            self.box = box.get_rect(topleft=(x_curr, dimension[1]))
            x_curr += dimension[0] / total + gap
            hlist.add(box)

        return hlist
            

    def create_list_vertical(self, amount, coord, dimension, color):
        vlist = pygame.sprite.Group()

        y_curr = coord[1] - (dimension[1] / 2) # Center - size of one side
        x, y = dimension

        total = amount + 1
        gap = (dimension[1] / total) / (amount-1)
        for i in range(amount):
            box = self.create_box((x, y / total), color)
            self.box = box.get_rect(topleft=(dimension[0], y_curr))
            y_curr += dimension[1] / total + gap
            vlist.add(box)

        return vlist