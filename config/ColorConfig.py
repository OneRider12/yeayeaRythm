import pygame

class ColorConfig:

    def __init__(self):
        self.color_func = {
            "VIB" : self.vibrant,
            "WB" : self.monotone,
            "PAS" : self.pastel,
            }

    def color(self, color_r, t_g, b : int = 255, t : int = 255):
        if isinstance(color_r, str):
            theme, name = color_r.split('_')
            return self.color_func[theme](name, t_g)
        elif isinstance(color_r, int):
            return pygame.Color(color_r, t_g, b, t)


    def __create_color(self, rgb: tuple, t : int = 255):
        r, g, b = [*rgb]
        return pygame.Color(r, g, b, t)

    def vibrant(self, colorname: str, t : int = 255):
        VIBRANT_COLORS = {
            "RED": (255, 0, 0),
            "LIME": (0, 255, 0),
            "BLUE": (0, 0, 255),
            "YELLOW": (255, 255, 0),
            "CYAN": (0, 255, 255),
            "MAGENTA": (255, 0, 255),
            "ORANGE": (255, 165, 0),
            "GOLD": (255, 215, 0),
        }
        return self.__create_color(VIBRANT_COLORS[colorname.upper()], t)
    
    def monotone(self, colorname: str, t : int = 255):
        MONOTONE_COLORS = {
            "WHITE": (255, 255, 255),
            "BLACK": (0, 0, 0),
            
            "BLACK1": (32, 32, 32),    # Very Dark Gray
            "BLACK2": (64, 64, 64),    # Dark Gray
            "BLACK3": (96, 96, 96),
            "BLACK4": (128, 128, 128),  # Gray (Mid-tone)
            "BLACK5": (160, 160, 160),
            "BLACK6": (192, 192, 192),  # Silver
            "BLACK7": (220, 220, 220),  # Light Gray
            "BLACK8": (240, 240, 240),  # Off-White
        }
        return self.__create_color(MONOTONE_COLORS[colorname.upper()], t)
    
    def pastel(self, colorname: str, t : int = 255):
        PASTEL_COLORS = {
            "PINK": (255, 192, 203),
            "LIME": (173, 255, 168), # Lightened Lime
            "CYAN": (175, 238, 238), # Lightened Cyan
            "YELLOW": (255, 255, 153), # Lightened Yellow
            "BLUE": (173, 216, 230), # Light Blue
            "PURPLE": (221, 160, 221), # Light Purple
        }
        return self.__create_color(PASTEL_COLORS[colorname.upper()], t)
