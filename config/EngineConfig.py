import pygame.time

class EngineConfig:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.tick_in_sec = 60
        self.isRunning = True
        self.catch_event = None

    def page_run(self):
        while self.isRunning:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.isRunning = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.isRunning = False
