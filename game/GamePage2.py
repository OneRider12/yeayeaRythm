import pygame
import json

from config.BoxConstant import NOTE_VECTOR_RES, BOX_TEMPO_COORD, BOX_TEMPO_SIZE, BOX_TEMPO_COLOR, \
    BOX_CHECKER_CHECKPOINT_COORD
from config.FontConstant import *
from config.PageConstant import *

from config.EngineConfig import EngineConfig
from util.Box import Box
from util.Screen import Screen
from util.Text import Text

GAME_WIDTH_CENTER = SCREEN_WIDTH_CENTER - 40
SCORE_WIDTH_CENTER = SCREEN_WIDTH - 100

BOX_CHECKER_COLOR = (63, 169, 245)
CHECKER_SIZE = (180, 20)
CHECKER_GAP = 20
CHECKER_DISTANCE = 600

LANE1_X = GAME_WIDTH_CENTER - CHECKER_GAP*3/2 - CHECKER_SIZE[0]*3/2
LANE2_X = GAME_WIDTH_CENTER - CHECKER_GAP/2 - CHECKER_SIZE[0]/2
LANE3_X = GAME_WIDTH_CENTER + CHECKER_GAP/2 + CHECKER_SIZE[0]/2
LANE4_X = GAME_WIDTH_CENTER + CHECKER_GAP*3/2 + CHECKER_SIZE[0]*3/2

BOX_NOTE_COLORS = [(255, 17, 120), (168, 0, 170), (255, 242, 5), (124, 255, 1)]
BOX_NOTE_SIZE = (180, 60)
BOX_NOTE1_COORD = (LANE1_X, -0)
BOX_NOTE2_COORD = (LANE2_X, -0)
BOX_NOTE3_COORD = (LANE3_X, -0)
BOX_NOTE4_COORD = (LANE4_X, -0)
BOX_NOTE_COORD = (BOX_NOTE1_COORD, BOX_NOTE2_COORD, BOX_NOTE3_COORD, BOX_NOTE4_COORD)
BOX_NOTE_DATA = lambda x : (BOX_NOTE_SIZE, BOX_NOTE_COLORS[x], BOX_NOTE_COORD[x])
NOTE_BLANK = ((1, 1), (*SCREEN_BACKGROUND, 1), (SCREEN_WIDTH_CENTER, SCREEN_HEIGHT))

SCORE_SIZE = 80

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
        self.tick_per_beat = self.bpm * 2
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
        self.score_multi_combo_value = {10: 1.3, 25: 2, 60: 3, 100: 5}
        self.color_stack = {100: (124, 255, 1), 60: (255, 242, 5), 25: (168, 0, 170), 10: (255, 17, 120), 0: (255, 254, 224)}

        # Pausing game
        self.isPause = False
        self.waiting_tick_clock = pygame.time.Clock()
        self.waiting_tick_counter = 0

        # Initialize all UI
        self.draft_all()

    def draft_all(self):
        # Header UI
        self.score_header_text = Text("SCORE", 60, NORMAL_COLOR_LIGHT, self.screen, (SCORE_WIDTH_CENTER, 60))
        # self.score_header_box = Box((180, 70), NORMAL_COLOR_LIGHT, (self.SCORE_WIDTH_CENTER, 60))
        self.score_counter_text = Text(f'{self.score:06d}', SCORE_SIZE, GAME_SCORE_COUNTER, self.screen, (SCORE_WIDTH_CENTER, SCREEN_HEIGHT_CENTER))
        self.score_ui.add(self.score_header_text)

        # Note box
        self.note_lane1_box = Box(BOX_NOTE_SIZE, BOX_NOTE_COLORS[0], BOX_NOTE1_COORD)
        self.note_lane2_box = Box(BOX_NOTE_SIZE, BOX_NOTE_COLORS[1], BOX_NOTE2_COORD)
        self.note_lane3_box = Box(BOX_NOTE_SIZE, BOX_NOTE_COLORS[2], BOX_NOTE3_COORD)
        self.note_lane4_box = Box(BOX_NOTE_SIZE, BOX_NOTE_COLORS[3], BOX_NOTE4_COORD)
        self.note_spawner = [self.note_lane1_box, self.note_lane2_box, self.note_lane3_box, self.note_lane4_box]

        # Tempo line spawner; (copy)
        # self.tempo_line_box = Box(BOX_TEMPO_SIZE, BOX_TEMPO_COLOR, BOX_TEMPO_COORD)
        self.playfield_boxes.add(self.note_lane1_box, self.note_lane2_box, self.note_lane3_box, self.note_lane4_box)

        # Checking box
        self.checker_lane1_box = Box(CHECKER_SIZE, BOX_CHECKER_COLOR, (LANE1_X, CHECKER_DISTANCE)) # 600 or 720
        self.checker_lane2_box = Box(CHECKER_SIZE, BOX_CHECKER_COLOR, (LANE2_X, CHECKER_DISTANCE))
        self.checker_lane3_box = Box(CHECKER_SIZE, BOX_CHECKER_COLOR, (LANE3_X, CHECKER_DISTANCE))
        self.checker_lane4_box = Box(CHECKER_SIZE, BOX_CHECKER_COLOR, (LANE4_X, CHECKER_DISTANCE))
        self.checker_boxes.add(self.checker_lane1_box, self.checker_lane2_box, self.checker_lane3_box,
                               self.checker_lane4_box)

        # Separate digit
        self.digit1 = Text('0', SCORE_SIZE, NORMAL_COLOR_LIGHT, self.screen,
                           (SCORE_WIDTH_CENTER, SCREEN_HEIGHT_CENTER - 40 - 80 * 2 + 20 * 2 + 10))
        self.digit2 = Text('0', SCORE_SIZE, NORMAL_COLOR_LIGHT, self.screen,
                           (SCORE_WIDTH_CENTER, SCREEN_HEIGHT_CENTER - 40 - 80 - 20 - 10))
        self.digit3 = Text('0', SCORE_SIZE, NORMAL_COLOR_LIGHT, self.screen,
                           (SCORE_WIDTH_CENTER, SCREEN_HEIGHT_CENTER - 40 - 10))
        self.digit4 = Text('0', SCORE_SIZE, NORMAL_COLOR_LIGHT, self.screen,
                           (SCORE_WIDTH_CENTER, SCREEN_HEIGHT_CENTER + 40 + 10))
        self.digit5 = Text('0', SCORE_SIZE, NORMAL_COLOR_LIGHT, self.screen,
                           (SCORE_WIDTH_CENTER, SCREEN_HEIGHT_CENTER + 40 + 80 + 20 + 10))
        self.digit6 = Text('0', SCORE_SIZE, NORMAL_COLOR_LIGHT, self.screen,
                           (SCORE_WIDTH_CENTER, SCREEN_HEIGHT_CENTER + 40 + 80 * 2 + 20 * 2 + 10))
        self.digits = [self.digit1, self.digit2, self.digit3, self.digit4, self.digit5, self.digit6]
        self.digit_group = pygame.sprite.Group()
        self.digit_group.add(self.digit1, self.digit2, self.digit3, self.digit4, self.digit5, self.digit6)

    # Lower numbers are drawn first (background)
    def update_static(self):
        self.ui.add(self.score_ui, layer=100)
        self.ui.add(self.checker_boxes, layer=20)
        self.ui.add(self.playfield_boxes, layer=150)
        self.ui.add(self.note_boxes, layer=10)
        self.ui.add(self.digit_group, layer=400)


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
            if self.tempo_counter + 1 <= len(self.notes_sheets):
                self.__generate_note(self.notes_sheets[self.tempo_counter])
            else:
                print("log: song ended")

            print(f'=== {self.tempo_counter} ===')

            self.tempo_counter += 1
            self.tick_counter = 0

        self.tick_counter += 1

    def __get_notes(self, sheet_dir):
        notes = []
        with open(sheet_dir, 'r') as file:
            for line in file:
                notes.append(line.strip())
        return notes

    def __generate_note(self, notes):
        note_template = (
            (BOX_NOTE_SIZE, BOX_NOTE_COLORS[0], BOX_NOTE1_COORD),
            (BOX_NOTE_SIZE, BOX_NOTE_COLORS[1], BOX_NOTE2_COORD),
            (BOX_NOTE_SIZE, BOX_NOTE_COLORS[2], BOX_NOTE3_COORD),
            (BOX_NOTE_SIZE, BOX_NOTE_COLORS[3], BOX_NOTE4_COORD),
        )

        note_group = pygame.sprite.Group()

        for n in range(4):
            if notes[n] == "*":
                note = Box(*BOX_NOTE_DATA(n))
                # print("log: create new note", n)
            else:
                note = Box(*NOTE_BLANK)
            note.vector = (0, 1)
            note_group.add(note)

        print(note_group)
        self.note_boxes.add(note_group)

    def __score_calc(self, successful):  # successful : 0% - 100%
        score_get = max([score for acc, score in self.score_success.items() if successful >= acc])
        if successful > 20:
            self.stack += 1
        else:
            self.stack = 0

        multi_list = [multi for combo, multi in self.score_multi_combo_value.items() if self.stack >= combo]
        multi = max(multi_list) if len(multi_list) > 0 else 1
        self.score += score_get * multi
        int(self.score)
        self.__score_updater()

        print(score_get, multi, self.stack, self.score)

    def __get_successful(self, leading_coord):
        checkpoint = BOX_CHECKER_CHECKPOINT_COORD
        successful = max(
            [min(abs(success - leading_coord), abs(leading_coord - success)) / checkpoint[1] * 100 for success in
             checkpoint])
        return successful

    def __score_updater(self):
        # 6-Digits
        score_text = f'{int(self.score):06d}'
        for n in range(len(score_text)):
            self.digits[n].text = score_text[n]

        # Coloring & Set value
        score_color = self.color_stack[0]
        for stack in self.color_stack:

            if stack >= self.stack:
                score_color = self.color_stack[stack]
                break

        self.score_counter_text.color = score_color
        self.digit_group.update() ## ** ##


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

            self.update_static()

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

            pygame.display.flip()

    def run(self):
        while self.isRunning:
            # Reset screen
            self.screen.fill(SCREEN_BACKGROUND)

            # Update state
            self.__update_tempo()
            self.update_static()
            self.update_dynamic()

            # Draw Edge line
            pygame.draw.line(self.screen, (27, 48, 91), (GAME_WIDTH_CENTER - 440, 0),
                             (GAME_WIDTH_CENTER - 440, SCREEN_HEIGHT), 12)
            pygame.draw.line(self.screen, (27, 48, 91), (GAME_WIDTH_CENTER + 440, 0),
                             (GAME_WIDTH_CENTER + 440, SCREEN_HEIGHT), 12)

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

            # self.score_counter_text.update_text(int(self.score))
            self.clock.tick(self.tick_per_beat * NOTE_VECTOR_RES)
            pygame.display.flip()
