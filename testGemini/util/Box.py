import pygame
from util.Gradient import Gradient 

# --- Placeholder for util.Text (Required since Text class was not provided) ---
class Text:
    """Minimal Text class for rendering text on the Box."""
    def __init__(self, text: str, color: tuple, size: int = 24):
        self.text = text
        self.color = color
        self.size = size
        self.font_surface = self._render()

    def _render(self):
        try:
            if not pygame.font.get_init():
                pygame.font.init()
                
            font = pygame.font.Font(None, self.size)
            return font.render(self.text, True, self.color)
        except pygame.error as e:
            # Handle error if font is uninitialized or other issues
            return pygame.Surface((1, 1))
# ----------------------------------------------------------------------------------

class Box(pygame.sprite.Sprite):
    """
    A sprite representing a rectangular box with optional text and gradient background.
    """
    def __init__(self, dimension: tuple, color, text:str="", text_color: tuple = (255, 255, 255)):
        super().__init__()
        self.dimension = dimension
        self.color = color
        self.text = text
        self.text_color = text_color
        
        self.image = pygame.Surface(self.dimension)
        self.rect = self.image.get_rect()

        self.isTexting = self.__check_text()
        self.__apply_background()

    def __check_text(self):
        """Checks if there is text to display and initializes the Text object."""
        if self.text != "":
            # Text is initialized with white color for contrast
            self.text_obj = Text(self.text, (255, 255, 255)) 
            return True
        else:
            return False

    def __apply_background(self):
        """Applies solid color or gradient based on the 'color' attribute."""
        if isinstance(self.color, dict):
            # Handle Gradient (if color is a dict of stops)
            try:
                gradient_maker = Gradient(self.color, self.dimension)
                self.image = gradient_maker.gradient
            except ValueError:
                # Fallback on gradient error
                self.image.fill((255, 255, 255))
        else:
            # Handle Solid Color (assuming self.color is an RGB tuple)
            self.image.fill(self.color)
            
        # Draw text on top of the image
        if self.isTexting:
            text_surf = self.text_obj.font_surface
            # Center the text on the box surface
            text_rect = text_surf.get_rect(center=self.image.get_rect().center)
            self.image.blit(text_surf, text_rect)


    def create_box(self, position):
        """Sets the position of the box on the screen."""
        self.rect.topleft = position
        return self 

    def create_button(self, position, text: str):
        """Placeholder for button creation logic."""
        pass
