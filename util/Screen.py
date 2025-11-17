import pygame

from config.PageConstant import SCREEN_DIMENSION, SCREEN_BACKGROUND, SCREEN_WIDTH, SCREEN_HEIGHT
from itertools import cycle
from PIL import Image  # ใช้แยกเฟรมของ GIF


class Screen:
    def __init__(self):
        self.isStatic = None
        self.screen = None
        self.isGif = True
        self.static_bg_image = None  # To hold the static image Surface
        self.frame_cycle = None  # To hold the GIF frame iterator

    def setup(self, color, name, isGif=False):
        """Initializes the screen and loads the appropriate background."""
        self.screen = pygame.display.set_mode(SCREEN_DIMENSION)
        self.isGif = isGif
        self.isStatic = not isGif

        pygame.display.set_caption(str(name))

        # Fill the screen with the base color
        self.screen.fill(pygame.Color(*SCREEN_BACKGROUND))

        if not isGif:
            # Load the static background image
            self.draw_background_image()

            # Blit the static image immediately (if loaded)
            if self.static_bg_image:
                self.screen.blit(self.static_bg_image, (0, 0))
        else:
            # Load GIF frames and create the cycle iterator
            load_gif_frames = self.__load_gif_frames("assets/gif/8904fb777b93efc7bd4b8aa22482672a.gif")
            self.frame_cycle = cycle(load_gif_frames)

        pygame.display.flip()

        return self.screen

    def __load_gif_frames(self, filename):
        """Loads and scales GIF frames with transparency set."""
        frames = []
        try:
            im = Image.open(filename)
            while True:
                # Convert PIL frame to Pygame Surface
                frame = im.convert('RGBA')
                pygame_img = pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode)

                # Scale the image to fit the screen
                pygame_img = pygame.transform.scale(pygame_img, SCREEN_DIMENSION)

                # Set global transparency (opacity 30%, 255 * 0.3 ≈ 77)
                pygame_img.set_alpha(77)

                frames.append(pygame_img)
                im.seek(im.tell() + 1)
        except EOFError:
            pass
        except FileNotFoundError:
            print(f"Error: GIF file not found at {filename}")
        except Exception as e:
            print(f"An error occurred during GIF loading: {e}")

        return frames

    def draw_background(self):
        """
        Draws the appropriate background:
        - If static, blit the pre-loaded image.
        - If dynamic, blit the next GIF frame.
        """
        if self.isStatic and self.static_bg_image:
            self.screen.blit(self.static_bg_image, (0, 0))
        elif not self.isStatic and self.frame_cycle:
            # This handles the animation logic for the GIF
            frame = next(self.frame_cycle)
            self.screen.blit(frame, (0, 0))

    def draw_background_image(self):
        """Loads the static background image with alpha channel."""
        try:
            # Load the image and preserve transparency (convert_alpha)
            self.static_bg_image = pygame.image.load('assets/image/background_image.png').convert_alpha()

            # Scale it to the screen size (assuming it should fill the screen)
            self.static_bg_image = pygame.transform.scale(self.static_bg_image, SCREEN_DIMENSION)

            # Optional: Set a global transparency if needed (e.g., 50% opacity)
            self.static_bg_image.set_alpha(128)

        except pygame.error as e:
            print(f"Failed to load static background image: {e}")
            # Fallback surface with semi-transparent color
            self.static_bg_image = pygame.Surface(SCREEN_DIMENSION, pygame.SRCALPHA)
            self.static_bg_image.fill((27, 48, 91, 255))

