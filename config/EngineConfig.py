import pygame.time
import json

FILENAME = "assets/song_data/song.json"

class EngineConfig:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.mouse = pygame.mouse.get_pos()

        self.tick_in_sec = 60
        self.isRunning = True
        self.catch_event = None

        self.music_volume = 0.8

    def _load(self, song_name):
        try:
            with open(FILENAME, 'r', encoding='utf-8') as file:

                raw_data = json.load(file)
                for data in raw_data:
                    if data['name'] == song_name:
                        self.sheet_dir = data['desc']['notes_sheet_dir']
                        self.song_dir = data['desc']['song_dir']
                        print(self.sheet_dir, self.song_dir)
                        pygame.mixer.music.load(self.song_dir)

                        return data['desc']

        except FileNotFoundError:
            print(f"Error: The file '{FILENAME}' was not found.")
            return None
        except json.JSONDecodeError:
            print(f"Error: The file '{FILENAME}' contains invalid JSON syntax.")
            return None

        try:
            transparent_bg_image = pygame.image.load('assets/image/').convert_alpha()
        except pygame.error as e:
            print(f"Failed to load image: {e}")
            # Handle error or use a fallback surface
            transparent_bg_image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            transparent_bg_image.fill((255, 0, 0, 128))  # Example fallback: semi-transparent red

    def play_song(self):
        pygame.mixer.music.set_volume(self.music_volume)
        pygame.mixer.music.play()

    def pause_song(self):
        pygame.mixer.music.pause()

    def unpause_song(self):
        pygame.mixer.music.unpause()

    def page_run(self):
        while self.isRunning:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.isRunning = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.isRunning = False
