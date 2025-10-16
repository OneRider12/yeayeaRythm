import pygame
from config.ScreenConfig import ScreenConfig
from config.FontConfig import FontConfig


class Game:

    def __init__(self):

        self.screenConfig = ScreenConfig()
        self.fontConfig = FontConfig()
        
        self.font = self.fontConfig.set_font()
        
        pygame.display.set_caption("yeayeaRythm")

        self.clock = pygame.time.Clock()
        self.clock.tick(1)
        self.running = True

        self.display = self.set_screen()
        
    
    def set_screen(self):
        return pygame.display.set_mode(self.screenConfig.set_dimension())

    
    def ren_text(self, text):
        text_surface = self.font.render(str(text), True, (255, 255, 255))
        self.display.blit(text_surface, (10, 10))
        pygame.display.update()

    def starting(self, ):
        

    def run(self):
        start_counter = 0
        # isNotBlit = True

        while self.running:

            # if isNotBlit and counter == 3000:
            self.ren_text(counter)
                # isNotBlit = False

            if counter == 6000:
                self.running = False
                pygame.quit()
            
            start_counter += 1
            # pygame.display.flip()
            pygame.display.update()

        pygame.quit()
        
        