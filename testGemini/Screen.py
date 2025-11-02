import pygame
# Assuming util directory for component files
from util.ItemList import ItemList 
from util.Box import Box 

# --- Base Pygame Screen Class ---

class Screen:
    """
    A concrete base class for Pygame screen management and drawing operations.
    Provides fundamental setup and drawing utilities.
    """
    def __init__(self):
        self.screen = None
        self.dimension = (0, 0)
        self.name = "Pygame App"

    def setup(self, dimension: tuple, color, name: str):
        """Sets up the Pygame display window."""
        self.dimension = dimension
        self.name = name
        self.screen = pygame.display.set_mode(dimension)
        pygame.display.set_caption(name)
        self.screen.fill(color)
        return self.screen

    # --- Drawing Methods ---

    def draw_surface(self, surface: pygame.Surface, coord: tuple):
        """Draw a generic Pygame Surface at the given coordinates."""
        if self.screen:
            self.screen.blit(surface, coord)

    def draw_group(self, group: pygame.sprite.Group):
        """Draw all sprites in a Pygame sprite Group."""
        if self.screen:
            group.draw(self.screen)

    def draw_list(self, axis: str, amount: int, boundary: tuple, coord: tuple):
        """Placeholder for drawing a list of items."""
        pass

    def draw_button(self, color: tuple, dimension: tuple, coord: tuple, text: str = ""):
        """Draws a simple button rectangle with centered text."""
        if self.screen:
            pygame.draw.rect(self.screen, color, (*coord, *dimension))
            if text:
                try:
                    font = pygame.font.Font(None, 24)
                    text_surface = font.render(text, True, (0, 0, 0))
                    text_rect = text_surface.get_rect(center=(coord[0] + dimension[0] // 2, coord[1] + dimension[1] // 2))
                    self.screen.blit(text_surface, text_rect)
                except pygame.error:
                    pass 

    def draw_text(self, text: str, color: tuple, size: int, coord: tuple):
        """Draw text on the screen at the given coordinates and size."""
        if self.screen:
            try:
                font = pygame.font.Font(None, size)
                text_surface = font.render(text, True, color)
                self.screen.blit(text_surface, coord)
            except pygame.error:
                pass 

# --- HomePage Concrete Subclass ---

class HomePage(Screen):
    def __init__(self):
        super().__init__()
        
        # Initialize Pygame systems
        if not pygame.get_init():
            pygame.init()
        if not pygame.font.get_init():
            pygame.font.init()
            
        # Screen Dimension
        self.dimension = (1200, 800)
        
        # Setup Screen (Dark background for contrast)
        self.screen = self.setup(
            dimension=self.dimension, 
            color=pygame.Color(20, 20, 40), 
            name="Home - YeaYeaRythm"
        )

        self.clock = pygame.time.Clock()
        self.isRunning = True
        
        # --- List Setup ---
        self.item_list_manager = ItemList(self.dimension, padding=20, spacing=15)
        
        # Define the 3-step gradient colors
        gradient_data = {
            0.0 : (191, 191, 191),
            0.5 : (255, 254, 224),
            1.0 : (255, 255, 241),
            # 0.0: (100, 100, 255),  # Top: Light Blue
            # 0.5: (10, 10, 150),    # Middle: Deep Blue
            # 1.0: (50, 200, 50)     # Bottom: Green
        }
        
        # Data for the list items
        list_items_data = [
            {'text': 'Rhythm Track 1', 'color': gradient_data},
            {'text': 'Rhythm Track 2', 'color': gradient_data},
            {'text': 'Rhythm Track 3', 'color': gradient_data},
            {'text': 'Rhythm Track 4', 'color': gradient_data},
        ]
        
        # Create the list of Box sprites, centered horizontally
        self.rhythm_items = self.item_list_manager.create_list(
            center_x=self.dimension[0] // 2, 
            data=list_items_data
        )

    def draw(self):
        """Handles all drawing logic for the home page."""
        
        # 1. Clear screen (re-fill background)
        self.screen.fill(pygame.Color(20, 20, 40))
        
        # 2. Draw Title
        self.draw_text(
            "Rhythm Tracks List", 
            (255, 255, 255), # White text
            64, 
            (self.dimension[0] // 2 - 250, 50)
        )
        
        # 3. Draw the list of gradient boxes using the inherited draw_group
        self.draw_group(self.rhythm_items)
        
        # 4. Update the display
        pygame.display.flip()


    def run(self):
        """Main game loop for the home page."""
        while self.isRunning:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.isRunning = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.isRunning = False

            # Drawing
            self.draw()
            
            # Frame rate control
            self.clock.tick(60)

        pygame.quit()
        
# --- Demonstration of Usage ---

pygame.init()

if __name__ == '__main__':
    try:
        game = HomePage()
        game.run()
    except Exception as e:
        print(f"An error occurred in the main execution: {e}")
        pygame.quit()
