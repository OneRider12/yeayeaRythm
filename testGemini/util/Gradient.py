import pygame
import math

class Gradient:
    """
    Creates a vertical three-step gradient Pygame Surface.
    
    The gradient dictionary must contain exactly three stops: 0.0, 0.5, and 1.0.
    Example: {0.0: (R, G, B), 0.5: (R, G, B), 1.0: (R, G, B)}
    """
    def __init__(self, gradient: dict, dimension: tuple):
        self.__gradient = gradient
        self.dimension = dimension
        self.width, self.height = dimension
        
        # Ensure stops are correctly ordered
        self.stops = sorted(self.__gradient.keys())
        if len(self.stops) != 3 or self.stops != [0.0, 0.5, 1.0]:
            raise ValueError("Gradient must contain exactly three stops: 0.0, 0.5, and 1.0.")

        self.gradient = self.draw_gradient()


    def draw_gradient(self):
        surface = pygame.Surface(self.dimension)
        
        # Determine the y-coordinates for the stops
        y_mid = int(self.height * self.stops[1]) # Stop at 0.5

        # --- Segment 1: 0.0 to 0.5 ---
        r1, g1, b1 = self.__gradient[self.stops[0]]
        r2, g2, b2 = self.__gradient[self.stops[1]]
        
        dr1, dg1, db1 = r2 - r1, g2 - g1, b2 - b1
        segment1_height = y_mid
        
        for y in range(segment1_height):
            # Factor within the first segment (0.0 to 1.0 within this segment)
            factor = y / segment1_height if segment1_height > 0 else 0
            r = int(r1 + dr1 * factor)
            g = int(g1 + dg1 * factor)
            b = int(b1 + db1 * factor)
            pygame.draw.line(surface, (r, g, b), (0, y), (self.width, y))

        # --- Segment 2: 0.5 to 1.0 ---
        r1, g1, b1 = self.__gradient[self.stops[1]]
        r2, g2, b2 = self.__gradient[self.stops[2]]
        
        dr2, dg2, db2 = r2 - r1, g2 - g1, b2 - b1
        segment2_height = self.height - y_mid
        
        for y in range(y_mid, self.height):
            # Factor within the second segment (0.0 to 1.0 within this segment)
            factor = (y - y_mid) / segment2_height if segment2_height > 0 else 0
            r = int(r1 + dr2 * factor)
            g = int(g1 + dg2 * factor)
            b = int(b1 + db2 * factor)
            pygame.draw.line(surface, (r, g, b), (0, y), (self.width, y))

        return surface
