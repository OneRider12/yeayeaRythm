import pygame
from config.ScreenConfig import ScreenConfig
from config.FontConfig import FontConfig
from config.ColorConfig import ColorConfig

class Home:

    def __init__(self):
        self.screenConfig = ScreenConfig()
        self.setupScreen(self.screenConfig)

        self.fontConfig = FontConfig()
        self.setupFont(self.fontConfig)

        self.clock = pygame.time.Clock()
        self.clock.tick(60)

        self.isRunning = True

        self.colors = ColorConfig()
        self.background = self.colors.monotone("WHITE", 100)

    def setupScreen(self, config: ScreenConfig):
        config.set_caption("yeayeaRythm - Home")
        self.width = 1200
        self.height = 800
        self.screen = config.init_screen(self.width, self.height)
        self.screen.fill(pygame.Color(0, 0, 0, 255))
        

    def setupFont(self, config: FontConfig):
        self.font = config.set_font()
    
    def blitfont(self, text, color, coord):
        text_surface = self.font.render(str(text), True, color)
        self.screen.blit(text_surface, coord)

    def run(self):
        tickCount = 0
        while self.isRunning:
            if tickCount % 30 == 0:
                self.screen.fill(self.background)
                self.blitfont(str(tickCount/30), self.colors.color("WB_Black", 255), (10, 10))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.isRunning = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.isRunning = False
            pygame.display.update()
            self.clock.tick(60)
            tickCount += 1
        
        pygame.quit()