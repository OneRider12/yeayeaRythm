import pygame.time
import json

class EngineConfig:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.tick_in_sec = 60
        self.isRunning = True
        self.catch_event = None

    def _load(self, filename):
        try:
            # Use 'with open' to open the file for reading ('r')
            with open(filename, 'r', encoding='utf-8') as file:

                # The json.load() function reads the file content,
                # parses the JSON structure, and returns a Python dictionary/list.
                data = json.load(file)

                return data

        except FileNotFoundError:
            print(f"Error: The file '{filename}' was not found.")
            return None
        except json.JSONDecodeError:
            print(f"Error: The file '{filename}' contains invalid JSON syntax.")
            return None

    def page_run(self):
        while self.isRunning:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.isRunning = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.isRunning = False
