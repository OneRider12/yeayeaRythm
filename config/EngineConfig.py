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

        self.leaderboard = None

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
                        self.leaderboard = self.score_data[song_name]['leaderboard']
                        return self.leaderboard

        except FileNotFoundError:
            print(f"Error: The file '{FILENAME_SCORE_DATA}' was not found.")
            return None
        except json.JSONDecodeError:
            print(f"Error: The file '{FILENAME_SCORE_DATA}' contains invalid JSON syntax.")
            return None

    def load_scores(self):
        """Loads the entire score data structure from score.json."""
        try:
            with open(FILENAME_SCORE_DATA, 'r') as file:
                return json.load(file)
        except json.JSONDecodeError:
            print(f"Error: Could not decode JSON from {FILENAME_SCORE_DATA}. Returning default.")
            return [
                {"song": i + 1, "leader": {}} for i in range(5)
            ]

    def save_scores(self, score_data):
        """Writes the current score data structure back to score.json."""
        try:
            # Use 'w' mode to write (overwrite) the file
            with open(FILENAME_SCORE_DATA, 'w') as file:
                # indent=2 makes the JSON human-readable.
                json.dump(score_data, file, indent=2)
            print(f"Success: Scores saved to {FILENAME_SCORE_DATA}")
        except Exception as e:
            print(f"Error saving scores: {e}")

    # IMPORTANT: This function implements the sorting/leaderboard logic
    def save_final_score(self, song_id, username, final_score, max_leaders=3):
        """
        Saves the final score if it's a new high score for the user.
        The leaderboard is automatically sorted and truncated to max_leaders.
        """
        scores = self.load_scores()

        # JSON arrays are 0-indexed, so we use song_id - 1
        song_index = song_id - 1

        # 1. Validate song index
        if not (0 <= song_index < len(scores) and scores[song_index]["song"] == song_id):
            print(f"Error: Song ID {song_id} not found in score data structure.")
            return

        # 2. Get the current leaderboard for the song
        leaderboard = scores[song_index]["leader"]

        # 3. Check if the new score is greater than the existing score for this user
        current_best = leaderboard.get(username, 0)

        if final_score > current_best:
            leaderboard[username] = final_score
            print(f"New High Score! Song {song_id}: {username} - {final_score}")

            # 4. Sorting and Truncating (The loop and swap logic is done efficiently with Python's sort)
            # Convert dict to list of (username, score) tuples
            sorted_leaders = sorted(
                leaderboard.items(),
                key=lambda item: item[1],  # Sort by score (item[1])
                reverse=True  # Highest score first
            )

            # Rebuild the leaderboard dictionary with only the top N scores
            top_leaders = dict(sorted_leaders[:max_leaders])
            scores[song_index]["leader"] = top_leaders

            # 5. Save the updated structure
            self.save_scores(scores)
        else:
            print(f"Score {final_score} is not better than current best {current_best} for {username}.")

    def update_score_json(self):
        with open('assets/score/score.json', 'w') as file:
            json.dump(self.score_data, file, indent=4)

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
