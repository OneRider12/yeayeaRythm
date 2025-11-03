import pygame
import json

from config.BoxConstant import GAME_SCORE_HEADING_BOX_COORD, GAME_SCORE_HEADING_BOX_SIZE, GAME_SCORE_HEADING_BOX_COLOR, \
    BOX_TEMPO_COLOR, BOX_TEMPO_SIZE, BOX_TEMPO_COORD, BOX_CHECKER_OUTER_SIZE, BOX_CHECKER_INNER_SIZE, \
    BOX_CHECKER_COLOR, BOX_CHECKER1_COORD, BOX_CHECKER2_COORD, BOX_CHECKER3_COORD, BOX_CHECKER4_COORD, GAME_EDGE_COLOR, \
    GAME_EDGE1_COORD_START, GAME_EDGE1_COORD_END, GAME_EDGE2_COORD_START, GAME_EDGE2_COORD_END, \
    GAME_EDGE_INNER_LINE_COLOR, GAME_EDGE_INNER1_COORD_START, GAME_EDGE_INNER1_COORD_END, GAME_EDGE_INNER2_COORD_START, \
    GAME_EDGE_INNER2_COORD_END, GAME_EDGE_CENTER_LINE_START, GAME_EDGE_CENTER_LINE_END, BOX_NOTE_COLORS, \
    ADJUSTMENT_MULTI, BOX_CHECKER_CHECKPOINT_COORD
from config.FontConstant import GAME_SCORE_HEADING_TEXT, NORMAL24, GAME_SCORE_HEADING_COLOR, HEADER48, \
    GAME_SCORE_COUNTER, GAME_SCORE_COUNTER_COORD
from config.PageConstant import SCREEN_BACKGROUND, GAME_TITLE, SCREEN_HEIGHT_CENTER
from config.EngineConfig import EngineConfig
from util.Box import Box
from util.Screen import Screen
from util.Text import Text


class GamePage(Screen, EngineConfig):
    def __init__(self, filename):
        # Screen, GameEngine setup
        Screen.__init__(self)
        EngineConfig.__init__(self)

        # WIP
        # Load song data
        self.song_data = self._load(filename)
        self.sheet_dir = self.song_data.get("notes_sheet_dir")


        # Setup screen
        self.screen = self.setup(SCREEN_BACKGROUND, self.song_data.get("name"))

        # Counter (calibrate with song data)
        self.bpm = self.song_data.get("bpm")
        self.tick_per_beat = self.bpm * 2
        self.tick_counter = 0


        # Static Group
        self.ui = pygame.sprite.LayeredUpdates() # Lower numbers are drawn first (background)
        self.score_ui = pygame.sprite.Group()
        self.checker_boxes = pygame.sprite.Group()

        # Dynamic Group
        self.temp_tempo_boxes = pygame.sprite.Group()
        self.note_boxes = pygame.sprite.Group()
        self.playfield_boxes = pygame.sprite.Group()


        # Scoring
        self.score = 0
        self.stack = 0
        self.score_success = {0:0, 20:0.5, 50:1, 70:1.5}
        self.score_multi_combo_value = {10:1.3, 25:2, 60:3, 100:5}

        # Initialize all UI
        self.draft_all()



    def draft_all(self):
        # Header UI
        self.score_header_text = Text(GAME_SCORE_HEADING_TEXT, NORMAL24, GAME_SCORE_HEADING_COLOR, self.screen,
                                      GAME_SCORE_HEADING_BOX_COORD)
        self.score_counter_text = Text(str(self.score), HEADER48, GAME_SCORE_COUNTER, self.screen,
                                       GAME_SCORE_COUNTER_COORD)
        self.score_header_box = Box(GAME_SCORE_HEADING_BOX_SIZE, GAME_SCORE_HEADING_BOX_COLOR,
                                    GAME_SCORE_HEADING_BOX_COORD)
        self.score_ui.add(self.score_header_box, self.score_header_text, self.score_counter_text)

        # Note box
        self.note_lane1_box = Box(GAME_SCORE_HEADING_BOX_SIZE, BOX_NOTE_COLORS[0], (100, SCREEN_HEIGHT_CENTER))
        self.note_lane2_box = Box(GAME_SCORE_HEADING_BOX_SIZE, BOX_NOTE_COLORS[1], (400, SCREEN_HEIGHT_CENTER))
        self.note_lane3_box = Box(GAME_SCORE_HEADING_BOX_SIZE, BOX_NOTE_COLORS[2], (700, SCREEN_HEIGHT_CENTER))
        self.note_lane4_box = Box(GAME_SCORE_HEADING_BOX_SIZE, BOX_NOTE_COLORS[3], (1000, SCREEN_HEIGHT_CENTER))

        # Tempo line spawner; (copy)
        # self.tempo_line_box = Box(BOX_TEMPO_SIZE, BOX_TEMPO_COLOR, BOX_TEMPO_COORD)
        self.playfield_boxes.add(self.note_lane1_box, self.note_lane2_box, self.note_lane3_box, self.note_lane4_box,
                                 # self.tempo_line_box
                                 )

        # Checking box
        self.checker_lane1_box = Box(BOX_CHECKER_OUTER_SIZE, BOX_CHECKER_COLOR, BOX_CHECKER1_COORD)
        self.checker_lane2_box = Box(BOX_CHECKER_INNER_SIZE, BOX_CHECKER_COLOR, BOX_CHECKER2_COORD)
        self.checker_lane3_box = Box(BOX_CHECKER_INNER_SIZE, BOX_CHECKER_COLOR, BOX_CHECKER3_COORD)
        self.checker_lane4_box = Box(BOX_CHECKER_OUTER_SIZE, BOX_CHECKER_COLOR, BOX_CHECKER4_COORD)
        self.checker_boxes.add(self.checker_lane1_box, self.checker_lane2_box, self.checker_lane3_box,
                               self.checker_lane4_box)

    # Lower numbers are drawn first (background)
    def update_static(self):
        # Add all group to ui
        self.ui.add(self.score_ui, layer=100)
        self.ui.add(self.checker_boxes, layer=20)
        self.ui.add(self.playfield_boxes, layer=150)

        # Update screen
        self.ui.draw(self.screen)

    def update_dynamic(self):
        # Update position of moving box
        self.temp_tempo_boxes.update()
        self.playfield_boxes.update()

    def __update_tempo(self):
        # Generate Tempo line and note
        if self.tick_counter == self.tick_per_beat / 2:
            tempo_box = Box(BOX_TEMPO_SIZE, BOX_TEMPO_COLOR, BOX_TEMPO_COORD)

            # tempo_box.rect.x - (1520 / 440) * (842 + tempo_box.rect.y)
            # (440 * abs(tempo_box.rect.y) / 1520)

            tempo_box.size_adj = ((1520 / 440) / 1.152, 0)
            tempo_box.vector = (0, 1)

            self.temp_tempo_boxes.add(tempo_box)
            self.ui.add(self.temp_tempo_boxes, layer=200)

            print(self.temp_tempo_boxes)
            self.tick_counter = 0

        self.tick_counter += 1

    def __update_note(self):
        # self.note_lane1_box.
        pass

    def __generate_note(self):
        with open(self.sheet_dir, 'r') as file:
            for line in file:
                print(line)

    # WIP
    def pause_game(self):
        self.clock.tick(0)
        print("**PAUSE**")
        self.clock.tick(60)

    # WIP
    def __score_calc(self, successful): # successful : 0% - 100%
        score_get = max([score for acc, score in self.score_success.items() if successful >= acc])
        if successful > 20:
            self.stack += 1
        else:
            self.stack = 0

        multi_list = [multi for combo, multi in self.score_multi_combo_value.items() if self.stack >= combo]
        multi = max(multi_list) if len(multi_list) > 0 else 1
        self.score += score_get * multi
        print(score_get, multi, self.stack, self.score)

    def __get_successful(self, leading_coord):
        checkpoint = BOX_CHECKER_CHECKPOINT_COORD
        successful = max([min((success / leading_coord), (leading_coord / success)) * 100 for success in checkpoint])
        return successful

    def run(self):
        while self.isRunning:
            # Reset screen
            self.screen.fill(SCREEN_BACKGROUND)

            # Update state
            self.__update_tempo()
            self.update_static()
            self.update_dynamic()

            # Draw Outer-edge line
            pygame.draw.line(self.screen, GAME_EDGE_COLOR, GAME_EDGE1_COORD_START,
                             GAME_EDGE1_COORD_END, 12)
            pygame.draw.line(self.screen, GAME_EDGE_COLOR, GAME_EDGE2_COORD_START,
                             GAME_EDGE2_COORD_END, 12)

            # Draw Inner-edge line
            pygame.draw.line(self.screen, GAME_EDGE_INNER_LINE_COLOR,
                             GAME_EDGE_INNER1_COORD_START,
                             GAME_EDGE_INNER1_COORD_END, 10)
            pygame.draw.line(self.screen, GAME_EDGE_INNER_LINE_COLOR,
                             GAME_EDGE_INNER2_COORD_START,
                             GAME_EDGE_INNER2_COORD_END, 10)

            # Draw Center line
            pygame.draw.line(self.screen, GAME_EDGE_INNER_LINE_COLOR,
                             GAME_EDGE_CENTER_LINE_START,
                             GAME_EDGE_CENTER_LINE_END, 10)

            # Event checker
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.isRunning = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.isRunning = False
                    if event.key == pygame.K_ESCAPE:
                        self.pause_game()

                    # Still not check
                    if event.key == pygame.K_d:
                        self.__score_calc(self.__get_successful(self.note_lane1_box.rect.bottom))
                        print("log: pressed d", self.note_lane1_box.rect.bottom)
                    if event.key == pygame.K_f:
                        self.__score_calc(self.__get_successful(self.note_lane2_box.rect.bottom))
                        print("log: pressed f", self.note_lane1_box.rect.bottom)
                    if event.key == pygame.K_j:
                        self.__score_calc(self.__get_successful(self.note_lane3_box.rect.bottom))
                        print("log: pressed j", self.note_lane1_box.rect.bottom)
                    if event.key == pygame.K_k:
                        self.__score_calc(self.__get_successful(self.note_lane4_box.rect.bottom))
                        print("log: pressed k", self.note_lane1_box.rect.bottom)

            self.score_counter_text.update_text(int(self.score))
            self.clock.tick(self.tick_per_beat)
            pygame.display.flip()
