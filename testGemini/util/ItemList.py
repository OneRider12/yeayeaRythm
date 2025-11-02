import pygame
from util.Box import Box

class ItemList:
    """
    Manages the creation and vertical layout of a list of Box objects (sprites).
    """
    def __init__(self, dimension: tuple, padding: int = 20, spacing: int = 10):
        self.dimension = dimension # Dimension of the entire screen/area
        self.padding = padding     # Padding around the list area
        self.spacing = spacing     # Spacing between items
        self.items = pygame.sprite.Group()
        
        # Fixed Box dimensions for list items
        self.item_dim = (200, 80)

    def create_list(self, center_x: int, data: list):
        """
        Generates and lays out Box objects vertically, centered on the given X coordinate.
        
        Args:
            center_x (int): The X coordinate to center the list on.
            data (list): A list of dictionaries, where each dict contains 
                         'text' (str) and 'color' (dict/tuple) for the Box.
                         
        Returns:
            pygame.sprite.Group: A group containing all the created Box sprites.
        """
        # Calculate the starting Y position to center the entire list vertically
        num_items = len(data)
        if num_items == 0:
            return self.items
            
        total_item_height = num_items * self.item_dim[1]
        total_spacing_height = (num_items - 1) * self.spacing
        total_list_height = total_item_height + total_spacing_height
        
        start_y = (self.dimension[1] // 2) - (total_list_height // 2)
        current_y = start_y

        for item_data in data:
            box_text = item_data.get('text', 'No Text')
            box_color = item_data.get('color', (50, 50, 50))
            
            # 1. Create the Box sprite
            new_box = Box(
                dimension=self.item_dim,
                color=box_color,
                text=box_text
            )
            
            # 2. Calculate position (centered on X)
            pos_x = center_x - (self.item_dim[0] // 2)
            
            # 3. Set position
            new_box.create_box((pos_x, current_y))
            
            # 4. Add to the sprite group
            self.items.add(new_box)
            
            # 5. Increment Y position for the next item
            current_y += self.item_dim[1] + self.spacing
        
        return self.items

    def create_box(self, position, text: str):
        """Not implemented in ItemList."""
        pass

    def create_button(self, position, text: str):
        """Not implemented in ItemList."""
        pass
