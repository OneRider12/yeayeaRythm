import pygame

from config.PageConstant import SCREEN_DIMENSION, SCREEN_BACKGROUND
from itertools import cycle
from PIL import Image  # ใช้แยกเฟรมของ GIF


class Screen:
    def __init__(self):
        self.screen = None

    def setup(self, color:pygame.Color, name):
        self.screen = pygame.display.set_mode(SCREEN_DIMENSION)

        pygame.display.set_caption(str(name))
        self.screen.fill(pygame.Color(*SCREEN_BACKGROUND))

        pygame.display.flip()

        load_gif_frames = self.__load_gif_frames("assets/gif/8904fb777b93efc7bd4b8aa22482672a.gif")
        self.frame_cycle = cycle(load_gif_frames)

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

    def __load_gif_frames(self, filename):
        gif_dir = "assets/gif/8904fb777b93efc7bd4b8aa22482672a.gif"
        gif_surface = pygame.image.load(gif_dir)
        im = Image.open(filename)
        frames = []
        try:
            while True:
                frame = im.convert('RGBA')
                pygame_img = pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode)
                pygame_img = pygame.transform.scale(pygame_img, (1200, 800))
                pygame_img.set_alpha(77)  # ความจาง 30% (255 * 0.3 ≈ 77)
                frames.append(pygame_img)
                im.seek(im.tell() + 1)
        except EOFError:
            pass
        return frames
    
    def draw_background(self):
        """Draw next GIF frame as the background."""
        if self.frame_cycle:
            frame = next(self.frame_cycle)
            self.screen.blit(frame, (0, 0))
