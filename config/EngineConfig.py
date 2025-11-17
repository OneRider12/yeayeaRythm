import pygame.time
import json

from config.PageConstant import SCREEN_WIDTH, SCREEN_HEIGHT

FILENAME_SONG_DATA = "assets/song_data/song.json"
FILENAME_SCORE_DATA = "assets/score/score.json"


class EngineConfig:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.mouse = pygame.mouse.get_pos()

        self.tick_in_sec = 60
        self.isRunning = True
        self.catch_event = None

        self.music_volume = 0.8

    def _load_song(self, song_name):
        try:
            with open(FILENAME_SONG_DATA, 'r', encoding='utf-8') as file:

                raw_data = json.load(file)
                for data in raw_data:
                    if data['name'] == song_name:
                        self.sheet_dir = data['desc']['notes_sheet_dir']
                        self.song_dir = data['desc']['song_dir']
                        print(self.sheet_dir, self.song_dir)
                        pygame.mixer.music.load(self.song_dir)

                        return data['desc']

        except FileNotFoundError:
            print(f"Error: The file '{FILENAME_SONG_DATA}' was not found.")
            return None
        except json.JSONDecodeError:
            print(f"Error: The file '{FILENAME_SONG_DATA}' contains invalid JSON syntax.")
            return None

    def _load_score(self, song_name):
        try:
            with open(FILENAME_SCORE_DATA, 'r', encoding='utf-8') as file:
                self.score_data = json.load(file)
                for song in self.score_data:
                    if song == song_name:
                        print(self.score_data[song_name]['leaderboard'])
                        return self.score_data[song_name]['leaderboard']

        except FileNotFoundError:
            print(f"Error: The file '{FILENAME_SCORE_DATA}' was not found.")
            return None
        except json.JSONDecodeError:
            print(f"Error: The file '{FILENAME_SCORE_DATA}' contains invalid JSON syntax.")
            return None


    def play_song(self):
        pygame.mixer.music.set_volume(self.music_volume)
        pygame.mixer.music.play()

    def stop_song(self):
        pygame.mixer.music.stop()

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
