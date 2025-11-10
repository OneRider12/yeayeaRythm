import pygame
import json

from config.BoxConstant import *
from config.FontConstant import *
from config.PageConstant import *

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
        sheet_dir = self.song_data.get("notes_sheet_dir")
        self.notes_sheets = self.__get_notes(sheet_dir)

        # Setup screen
        self.screen = self.setup(SCREEN_BACKGROUND, self.song_data.get("name") + "- Gameplay")

        # Counter (calibrate with song data)
        self.bpm = self.song_data.get("bpm")
        self.tick_per_beat = int(self.bpm * (self.bpm / 120) * 2)
        self.tick_counter = 0
        self.tempo_counter = 0

        # Static Group
        self.ui = pygame.sprite.LayeredUpdates()  # Lower numbers are drawn first (background)
        self.score_ui = pygame.sprite.Group()
        self.checker_boxes = pygame.sprite.Group()

        # Dynamic Group
        self.temp_tempo_boxes = pygame.sprite.Group()
        self.note_boxes = pygame.sprite.Group()
        self.playfield_boxes = pygame.sprite.Group()

        # Scoring
        self.score = 0
        self.stack = 0
        self.score_success = {0: 0, 20: 0.5, 50: 1, 70: 1.5}
        self.score_multi_combo_value = {10: 1.5, 25: 2, 60: 5, 100: 10}

        # Pausing game
        self.isPause = False
        self.waiting_tick_clock = pygame.time.Clock()
        self.waiting_tick_counter = 0

        # Initialize all UI
        self.draft_all()

    def draft_all(self):
        # Header UI
        self.score_header_text = Text(GAME_SCORE_HEADING_TEXT, 52, GAME_SCORE_HEADING_COLOR, self.screen,
                                      GAME_SCORE_HEADING_BOX_COORD)
        self.score_counter_text = Text(str(self.score), 56, GAME_SCORE_COUNTER, self.screen,
                                       GAME_SCORE_COUNTER_COORD)
        self.score_header_box = Box(GAME_SCORE_HEADING_BOX_SIZE, GAME_SCORE_HEADING_BOX_COLOR,
                                    GAME_SCORE_HEADING_BOX_COORD)
        self.score_ui.add(self.score_header_box, self.score_header_text, self.score_counter_text)

        # Note box
        self.note_lane1_box = Box(BOX_NOTE_OUTER_SIZE, BOX_NOTE_COLORS[0], BOX_NOTE1_COORD)
        self.note_lane2_box = Box(BOX_NOTE_INNER_SIZE, BOX_NOTE_COLORS[1], BOX_NOTE2_COORD)
        self.note_lane3_box = Box(BOX_NOTE_INNER_SIZE, BOX_NOTE_COLORS[2], BOX_NOTE3_COORD)
        self.note_lane4_box = Box(BOX_NOTE_OUTER_SIZE, BOX_NOTE_COLORS[3], BOX_NOTE4_COORD)
        self.note_spawner = [self.note_lane1_box, self.note_lane2_box, self.note_lane3_box, self.note_lane4_box]

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
        self.ui.add(self.note_boxes, layer=10)


        # Update screen
        self.ui.draw(self.screen)

    def update_dynamic(self):
        # Update position of moving box
        self.temp_tempo_boxes.update()
        self.note_boxes.update()
        self.playfield_boxes.update()

    def __update_tempo(self):
        # Generate Tempo line and note
        if self.tick_counter == self.tick_per_beat * NOTE_VECTOR_RES / 2:
            tempo_box = Box(BOX_TEMPO_SIZE, BOX_TEMPO_COLOR, BOX_TEMPO_COORD)

            # tempo_box.rect.x - (1520 / 440) * (842 + tempo_box.rect.y)
            # (440 * abs(tempo_box.rect.y) / 1520)

            tempo_box.size_adj = ((1520 / 440) / 1.152, 0)
            tempo_box.vector = (0, 1)

            self.temp_tempo_boxes.add(tempo_box)
            self.ui.add(self.temp_tempo_boxes, layer=200)

            if self.tempo_counter + 1 <= len(self.notes_sheets):
                self.__generate_note(tempo_box, self.notes_sheets[self.tempo_counter])
            else:
                print("log: song ended")

            print(f'=== {self.tempo_counter} ===')

            self.tempo_counter += 1
            self.tick_counter = 0

        if not self.isPause:
            self.tick_counter += 1
        else:
            self.waiting_tick_counter += 1

    # Not in use
    def __update_note(self):
        # self.note_lane1_box.
        pass

    def __get_notes(self, sheet_dir):
        notes = []
        with open(sheet_dir, 'r') as file:
            for line in file:
                notes.append(line.strip())
        return notes

    def __generate_note(self, anchor, notes):
        note_template = (
            (BOX_NOTE_OUTER_SIZE, BOX_NOTE_COLORS[0], BOX_NOTE1_COORD, NOTE_RESIZE_KWARGS[0]),
            (BOX_NOTE_INNER_SIZE, BOX_NOTE_COLORS[1], BOX_NOTE2_COORD, NOTE_RESIZE_KWARGS[1]),
            (BOX_NOTE_INNER_SIZE, BOX_NOTE_COLORS[2], BOX_NOTE3_COORD, NOTE_RESIZE_KWARGS[2]),
            (BOX_NOTE_OUTER_SIZE, BOX_NOTE_COLORS[3], BOX_NOTE4_COORD, NOTE_RESIZE_KWARGS[3]),
        )
        spaced_note = ((1, 1), BOX_TEMPO_COLOR, (SCREEN_WIDTH_CENTER, SCREEN_HEIGHT))
        note_vector = NOTE_VECTOR
        note_resize = NOTE_RESIZE

        note_group = pygame.sprite.Group()

        print(f'"""   """{note_vector}"""   """{note_resize}')

        for n in range(4):
            # print(f',,,{note_vector[n]} ,,,{note_resize[n]}')
            if notes[n] == "*":
                note = Box(*note_template[n])
                # print("log: create new note", n)
            else:
                note = Box(*spaced_note)
            note.vector = note_vector[n]
            note.size_adj = note_resize[n]
            note_group.add(note)

        print(note_group)
        self.note_boxes.add(note_group)

    # WIP
    def __score_calc(self, successful):  # successful : 0% - 100%
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
        successful = max(
            [min(abs(success - leading_coord), abs(leading_coord - success)) / checkpoint[1] * 100 for success in
             checkpoint])
        return successful

    # WIP; Add Button UI
    def pause_game(self):
        sec_paused = 0

        self.pause_popup = Box((400, 300), (59, 49, 73), SCREEN_CENTER)
        self.pause_text = Text("PAUSE", 60, (253, 252, 228), self.screen,
                               (SCREEN_WIDTH_CENTER, SCREEN_HEIGHT_CENTER - 80))
        self.home_button = Text("HOME", 52, (253, 252, 228), self.screen,
                                (SCREEN_WIDTH_CENTER, SCREEN_HEIGHT_CENTER + 50))
        pause_group = pygame.sprite.Group()
        pause_group.add(self.pause_popup, self.pause_text, self.home_button)
        self.ui.add(self.pause_popup, layer=201)
        self.ui.add(self.pause_text, layer=202)
        self.ui.add(self.home_button, layer=203)
        print("**PAUSE**")

        while self.isPause:

            pause_group.draw(self.screen)

            if self.waiting_tick_counter == 100:
                self.waiting_tick_counter = 0
                sec_paused += 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.isPause = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.pause_popup.kill()
                        self.pause_text.kill()
                        self.home_button.kill()
                        print("**UNPAUSE**")
                        print(f'log: paused for {sec_paused}.{self.waiting_tick_counter}s')
                        self.isPause = False

            self.waiting_tick_clock.tick(100)
            self.waiting_tick_counter += 1
            print(self.tick_counter, self.waiting_tick_counter)

            pygame.display.flip()

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
                             GAME_EDGE1_COORD_END, 30)
            pygame.draw.line(self.screen, GAME_EDGE_COLOR, GAME_EDGE2_COORD_START,
                             GAME_EDGE2_COORD_END, 30)

            # Draw Inner-edge line
            pygame.draw.line(self.screen, GAME_EDGE_INNER_LINE_COLOR,
                             GAME_EDGE_INNER1_COORD_START,
                             GAME_EDGE_INNER1_COORD_END, 24)
            pygame.draw.line(self.screen, GAME_EDGE_INNER_LINE_COLOR,
                             GAME_EDGE_INNER2_COORD_START,
                             GAME_EDGE_INNER2_COORD_END, 24)

            # Draw Center line
            pygame.draw.line(self.screen, GAME_EDGE_INNER_LINE_COLOR,
                             GAME_EDGE_CENTER_LINE_START,
                             GAME_EDGE_CENTER_LINE_END, 20)

            # Event checker
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.isRunning = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.isRunning = False
                    if event.key == pygame.K_ESCAPE:
                        if not self.isPause:
                            self.isPause = True
                            self.pause_game()

                    # Still not check
                    if event.key == pygame.K_d:
                        self.__score_calc(self.__get_successful(self.note_lane1_box.rect.bottom)) # something.rect.bottom or something
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
            self.clock.tick(self.tick_per_beat * NOTE_VECTOR_RES)
            pygame.display.flip()
