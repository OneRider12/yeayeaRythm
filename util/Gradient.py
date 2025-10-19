import pygame


class Gradient:
    def __init__(self, gradient: dict, dimension: tuple):
        self.__gradient = gradient
        self.dimension = dimension
        self.width, self.height = dimension

        self.gradient = self.draw_gradient()


    def draw_gradient(self):
        surface = pygame.Surface(self.dimension)
        stops = list()

        stops = [x for x in self.__gradient.keys()]

        r1, g1, b1 = self.__gradient[stops[0]]
        r2, g2, b2 = self.__gradient[stops[1]]
        dr, dg, db = r2 - r1, g2 - g1, b2 - b1

        for y in range(self.height):
            factor = y / self.height
            if factor > stops[1]:
                r1, g1, b1 = self.__gradient[stops[1]]
                r2, g2, b2 = self.__gradient[stops[2]]
                dr, dg, db = r2 - r1, g2 - g1, b2 - b1

            r = int(r1 + dr * factor)
            g = int(g1 + dg * factor)
            b = int(b1 + db * factor)
            pygame.draw.line(surface, (r, g, b), (0, y), (self.width, y))

        return surface


# print(Gradient({
#     0.0: (0, 0, 0),
#     0.5: (127, 127, 127),
#     1.0: (255, 255, 255)
# }, (400, 200)))
