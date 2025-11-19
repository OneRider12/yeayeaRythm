from config.FontConstant import *
from config.PageConstant import *

from config.EngineConfig import EngineConfig
from config.game_config import game_settings
from ui.ui import Button
from util.Box import Box
from util.Screen import Screen
from util.Text import Text

GAME_WIDTH_CENTER = SCREEN_WIDTH_CENTER - 40
SCORE_WIDTH_CENTER = SCREEN_WIDTH - 100

BOX_CHECKER_COLOR = (63, 169, 245)
CHECKER_SIZE = (180, 40)
CHECKER_GAP = 20
CHECKER_DISTANCE = 620
CHECKER_ZONE_Y = [CHECKER_DISTANCE + 10, CHECKER_DISTANCE, CHECKER_DISTANCE - 8]

LANE1_X = GAME_WIDTH_CENTER - CHECKER_GAP * 3 / 2 - CHECKER_SIZE[0] * 3 / 2
LANE2_X = GAME_WIDTH_CENTER - CHECKER_GAP / 2 - CHECKER_SIZE[0] / 2
LANE3_X = GAME_WIDTH_CENTER + CHECKER_GAP / 2 + CHECKER_SIZE[0] / 2
LANE4_X = GAME_WIDTH_CENTER + CHECKER_GAP * 3 / 2 + CHECKER_SIZE[0] * 3 / 2

BOX_NOTE_COLORS = [(255, 17, 120, 255), (168, 0, 170, 255), (255, 242, 5, 255), (124, 255, 1, 255)]
BOX_NOTE_COLORS_T = [(255, 17, 120, 120), (168, 0, 170, 120), (255, 242, 5, 120), (124, 255, 1, 120)]
BOX_NOTE_SIZE = (180, 60)  ##
BOX_NOTE1_COORD = (LANE1_X, -0)
BOX_NOTE2_COORD = (LANE2_X, -0)
BOX_NOTE3_COORD = (LANE3_X, -0)
BOX_NOTE4_COORD = (LANE4_X, -0)
# BOX_NOTE_COORD = (BOX_NOTE1_COORD, BOX_NOTE2_COORD, BOX_NOTE3_COORD, BOX_NOTE4_COORD)
# BOX_NOTE_DATA = lambda x: (BOX_NOTE_SIZE, BOX_NOTE_COLORS[x], BOX_NOTE_COORD[x])
NOTE_BLANK = ((1, 1), (*SCREEN_BACKGROUND, 1), (SCREEN_WIDTH_CENTER, SCREEN_HEIGHT))
#
# NOTE_LONG_SIZE = (180, 640)  ##
# BOX_LONG_NOTE_COORD = [(LANE1_X, -300), (LANE2_X, -300), (LANE3_X, -300), (LANE4_X, -300)]
# BOX_LONG_NOTE_ATTR = lambda lane: (NOTE_LONG_SIZE, BOX_NOTE_COLORS[lane], BOX_LONG_NOTE_COORD[lane])

# Single / Long (2) / Long (3)
UNIV_NOTE_SIZE = [(180, 60), (180, 420), (180, 900)]
UNIV_NOTE_COORD = [-300, -480, -720]
LANEX_X = [GAME_WIDTH_CENTER - CHECKER_GAP * 3 / 2 - CHECKER_SIZE[0] * 3 / 2,
           GAME_WIDTH_CENTER - CHECKER_GAP / 2 - CHECKER_SIZE[0] / 2,
           GAME_WIDTH_CENTER + CHECKER_GAP / 2 + CHECKER_SIZE[0] / 2,
           GAME_WIDTH_CENTER + CHECKER_GAP * 3 / 2 + CHECKER_SIZE[0] * 3 / 2]

UNIV_NOTE_DATA = lambda lane, size: (UNIV_NOTE_SIZE[size], BOX_NOTE_COLORS[lane],
                                     (LANEX_X[lane], UNIV_NOTE_COORD[size]))

SCORE_SIZE = 80

class GamePage(Screen, EngineConfig):
    def __init__(self, song_name):
        # Screen, GameEngine setup
        Screen.__init__(self)
        EngineConfig.__init__(self)

        # Load song data
        self.song_data = self._load_song(song_name)  # as Dict
        self.leaderboard = self._load_score(song_name)
        self.sheet_dir = self.song_data["notes_sheet_dir"]
        self.notes_sheets = self.__get_notes(self.sheet_dir)

        # Setup screen
        self.screen = self.setup(SCREEN_BACKGROUND, self.song_data["name"] + "- Gameplay", False)

        # Counter (calibrate with song data)
        self.bpm = self.song_data["bpm"]
        self.tick_base = 100
        self.tick_multi = self.bpm / self.tick_base

        self.tick_per_beat = self.tick_base * self.tick_multi
        self.tick_counter = 0
        self.tempo_counter = 0
        self.tick_delay_end_counter = 0

        self.difficulty = self.song_data.get("difficulty")

        # Static Group
        self.ui = pygame.sprite.LayeredUpdates()  # Lower numbers are drawn first (background)
        self.score_ui = pygame.sprite.Group()
        self.checker_boxes = pygame.sprite.Group()
        self.checker_zone = []

        # Dynamic Group
        self.temp_tempo_boxes = pygame.sprite.Group()
        self.note_boxes = pygame.sprite.Group()
        self.playfield_boxes = pygame.sprite.Group()

        # Scoring
        self.score = 0
        self.stack = 0
        self.score_success = {0: 0, 20: 1, 50: 1.5, 70: 2}
        self.score_multi_combo_value = {10: 1.3, 25: 2, 60: 3, 100: 5}
        self.color_stack = {0: (255, 254, 224), 10: (124, 255, 1), 25: (255, 242, 5), 60: (168, 0, 170),
                            100: (255, 17, 120)}

        self.note_in_lane = [(0, []), (0, []), (0, []), (0, [])]

        self.isLongPressing = [False, False, False, False]
        self.isPressing = False

        # Pausing game
        self.isPause = False
        self.waiting_tick_clock = pygame.time.Clock()
        self.waiting_tick_counter = 0

        # Ending game
        self.isEnded = False
        self.ending_tick_clock = pygame.time.Clock()

        # Initialize all UI
        self.draft_all()

    def draft_all(self):
        # Header UI
        self.score_header_text = Text("SCORE", 60, NORMAL_COLOR_LIGHT, self.screen, (SCORE_WIDTH_CENTER, 60))
        self.score_ui.add(self.score_header_text)

        # Note box
        self.note_lane1_box = Box(BOX_NOTE_SIZE, BOX_NOTE_COLORS[0], BOX_NOTE1_COORD)
        self.note_lane2_box = Box(BOX_NOTE_SIZE, BOX_NOTE_COLORS[1], BOX_NOTE2_COORD)
        self.note_lane3_box = Box(BOX_NOTE_SIZE, BOX_NOTE_COLORS[2], BOX_NOTE3_COORD)
        self.note_lane4_box = Box(BOX_NOTE_SIZE, BOX_NOTE_COLORS[3], BOX_NOTE4_COORD)
        self.note_spawner = [self.note_lane1_box, self.note_lane2_box, self.note_lane3_box, self.note_lane4_box]

        self.playfield_boxes.add(self.note_lane1_box, self.note_lane2_box, self.note_lane3_box, self.note_lane4_box)

        # Checking box
        self.checker_lane1_box = Box(CHECKER_SIZE, BOX_CHECKER_COLOR, (LANE1_X, CHECKER_DISTANCE))  # 600 or 720
        self.checker_lane2_box = Box(CHECKER_SIZE, BOX_CHECKER_COLOR, (LANE2_X, CHECKER_DISTANCE))
        self.checker_lane3_box = Box(CHECKER_SIZE, BOX_CHECKER_COLOR, (LANE3_X, CHECKER_DISTANCE))
        self.checker_lane4_box = Box(CHECKER_SIZE, BOX_CHECKER_COLOR, (LANE4_X, CHECKER_DISTANCE))
        self.checker_boxes_list = [self.checker_lane1_box, self.checker_lane2_box, self.checker_lane3_box,
                                   self.checker_lane4_box]
        self.checker_boxes.add(self.checker_lane1_box, self.checker_lane2_box, self.checker_lane3_box,
                               self.checker_lane4_box)

        # Separate digit
        self.digit1 = Text('0', SCORE_SIZE, NORMAL_COLOR_LIGHT, self.screen,
                           (SCORE_WIDTH_CENTER, SCREEN_HEIGHT_CENTER - 40 - 80 * 2 + 20 * 2 + 10), isDigit=True)
        self.digit2 = Text('0', SCORE_SIZE, NORMAL_COLOR_LIGHT, self.screen,
                           (SCORE_WIDTH_CENTER, SCREEN_HEIGHT_CENTER - 40 - 80 - 20 - 10), isDigit=True)
        self.digit3 = Text('0', SCORE_SIZE, NORMAL_COLOR_LIGHT, self.screen,
                           (SCORE_WIDTH_CENTER, SCREEN_HEIGHT_CENTER - 40 - 10), isDigit=True)
        self.digit4 = Text('0', SCORE_SIZE, NORMAL_COLOR_LIGHT, self.screen,
                           (SCORE_WIDTH_CENTER, SCREEN_HEIGHT_CENTER + 40 + 10), isDigit=True)
        self.digit5 = Text('0', SCORE_SIZE, NORMAL_COLOR_LIGHT, self.screen,
                           (SCORE_WIDTH_CENTER, SCREEN_HEIGHT_CENTER + 40 + 80 + 20 + 10), isDigit=True)
        self.digit6 = Text('0', SCORE_SIZE, NORMAL_COLOR_LIGHT, self.screen,
                           (SCORE_WIDTH_CENTER, SCREEN_HEIGHT_CENTER + 40 + 80 * 2 + 20 * 2 + 10), isDigit=True)

        self.digits = [self.digit1, self.digit2, self.digit3, self.digit4, self.digit5, self.digit6]
        self.digit_group = pygame.sprite.Group()
        self.digit_group.add(self.digit1, self.digit2, self.digit3, self.digit4, self.digit5, self.digit6)

    # Lower numbers are drawn first (background)
    def update_static(self):
        self.ui.add(self.score_ui, layer=100)
        self.ui.add(self.digit_group, layer=110)

        self.ui.add(self.checker_boxes, layer=20)
        self.ui.add(self.playfield_boxes, layer=150)
        self.ui.add(self.note_boxes, layer=10)
        # self.ui.add(self.checker_boxes, layer=300)

        # print(self.ui)
        # Update screen
        self.ui.draw(self.screen)

    def update_dynamic(self):
        # Update position of moving box
        self.temp_tempo_boxes.update()
        self.note_boxes.update()
        self.playfield_boxes.update()

    def __get_notes(self, sheet_dir):
        notes = []
        with open(sheet_dir, 'r') as file:
            for line in file:
                notes.append(line.strip())
        return notes

    def __update_tempo(self):

        # Generate Tempo line and note
        if self.tick_counter == int(self.tick_per_beat / self.difficulty):
            if self.tempo_counter + 1 <= len(self.notes_sheets):
                self.__generate_note(self.notes_sheets[self.tempo_counter])
            else:
                self.isEnded = True
                print("log: song ended")

            print(f'=== {self.tempo_counter} ===')

            self.tempo_counter += 1
            self.tick_counter = 0

        self.tick_counter += 1

    def __update_long_note(self):
        # Update color
        for lane in range(len(self.note_in_lane)):
            for note in self.note_in_lane[lane][1]:
                if note.isLongNote and self.isLongPressing[lane]:
                    note.color = BOX_NOTE_COLORS_T[lane]
                if note.isLongNote and not self.isLongPressing[lane]:
                    note.color = BOX_NOTE_COLORS[lane]

    def __generate_note(self, notes):
        note_group = pygame.sprite.Group()

        for n in range(4):
            # if notes[n].isdigit():
            note_size = int(notes[n])
            if note_size >= 1:
                note = Box(*UNIV_NOTE_DATA(n, note_size - 1))
                note.isLongNote = True if note_size > 1 else False
            else:
                note = Box(*NOTE_BLANK)

            note.vector = (0, 1 * self.tick_multi)
            # note.vector = (0, 1 / 100)
            note_group.add(note)
            self.note_in_lane[n][1].append(note)

        self.note_boxes.add(note_group)

    def __score_calc(self, successful):  # successful : 0% - 100%
        score_get = max([score for acc, score in self.score_success.items() if successful >= acc])
        if successful > 20:
            self.stack += 1

            multi_list = [multi for combo, multi in self.score_multi_combo_value.items() if self.stack >= combo]
            multi = max(multi_list) if len(multi_list) > 0 else 1
            self.score += score_get * multi

            int(self.score)
            self.__update_score()

        else:
            self.stack = 0

        print(f'score: {self.score}')

    def __get_successful(self, rect1: pygame.Rect, rect2: pygame.Rect):
        if not rect1.colliderect(rect2):
            return 0

        intersection_rect = rect1.clip(rect2)
        area_of_rect1 = rect1.width * rect1.height
        intersection_area = intersection_rect.width * intersection_rect.height
        percent = (intersection_area / area_of_rect1) * 100

        print(f'percent: {percent}')
        return percent

    def __update_score(self):
        # Coloring
        color_max = max([k for k, v in self.color_stack.items() if self.stack >= k])
        score_color = self.color_stack[color_max]

        # Texting
        score_text = f'{int(self.score):06d}'
        for n in range(len(score_text)):
            self.digits[n].update_text(score_text[n])
            self.digits[n].update_color(score_color)
        print(f'score_digits: -- {score_text} --')

    def __get_checking_box(self, lane_index) -> Box:
        checking_box = None
        lane_list = self.note_in_lane[lane_index][1]

        if len(lane_list) > 0:
            if lane_list[0].rect.bottom > 400:
                checking_box = lane_list[0]
                if not checking_box.isLongNote:
                    lane_list.pop(0)

        return checking_box

    def __kill_long_note(self, lane_index: int):
        lane_list = self.note_in_lane[lane_index][1]

        for note in lane_list:
            if note.isLongNote and self.isLongPressing[lane_index]:
                lane_list.pop(0)
                self.note_in_lane[0][1][0].kill()

    def pause_game(self):
        sec_paused = 0
        dt = 100

        # Setup UI
        self.pause_popup = Box((600, 450), (59, 49, 73), SCREEN_CENTER)
        self.pause_text = Text("PAUSE", 60, (253, 252, 228), self.screen,
                               (SCREEN_WIDTH_CENTER, SCREEN_HEIGHT_CENTER - 120))
        home_button = Button("Home", (SCREEN_WIDTH_CENTER, SCREEN_HEIGHT_CENTER + 80))

        # Display UI
        pause_group = pygame.sprite.Group()
        pause_group.add(self.pause_popup, self.pause_text)
        self.ui.add(self.pause_popup, layer=201)
        self.ui.add(self.pause_text, layer=202)
        print("**PAUSE**")

        # Pause song
        self.pause_song()

        # Pausing loop
        while self.isPause:

            self.update_static()

            home_button.draw(self.screen)
            home_button.update(self.mouse, dt)

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
                        self.unpause_song()
                        print("**UNPAUSE**")
                        print(f'log: paused for {sec_paused}.{self.waiting_tick_counter}s')
                        self.isPause = False

                    if event.key == pygame.K_SPACE:
                        self.isPause = False
                        self.isRunning = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if home_button.was_clicked(event):
                        self.pause_popup.kill()
                        self.pause_text.kill()

                        self.isPause = False
                        self.isRunning = False

                        print("**TO HOME**")
                        print(f'log: paused for {sec_paused}.{self.waiting_tick_counter}s')


            self.waiting_tick_clock.tick(dt)
            self.waiting_tick_counter += 1

            pygame.display.flip()

    def end_game(self):
        dt = 100
        int(self.score) if self.score > 100 else self.score
        self.end_popup = Box((560, 420), (59, 49, 73), SCREEN_CENTER)
        self.end_text = Text("ENDED", 60, (253, 252, 228), self.screen,
                             (SCREEN_WIDTH_CENTER, SCREEN_HEIGHT_CENTER - 160), isDigit=True)
        self.score_text = Text(str(int(self.score)), 100, (253, 252, 228), self.screen,
                               (SCREEN_WIDTH_CENTER, SCREEN_HEIGHT_CENTER))
        home_button = Button("Home", (SCREEN_WIDTH_CENTER, SCREEN_HEIGHT_CENTER + 120))

        ending_group = pygame.sprite.Group()
        ending_group.add(self.end_popup, self.end_text, self.score_text)
        self.ui.add(self.end_popup, layer=501)
        self.ui.add(self.end_text, layer=502)
        self.ui.add(self.score_text, layer=503)

        self.__update_leaderboard()

        print("**ENDED**")

        while self.isEnded:

            self.update_static()

            home_button.update(self.mouse, dt)
            home_button.draw(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.isEnded = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.end_popup.kill()
                        self.end_text.kill()
                        self.score_text.kill()

                        self.isEnded = False
                        return "quit"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if home_button.was_clicked(event):
                        return "start"

            self.ending_tick_clock.tick(dt)

            pygame.display.flip()
            self.isRunning = False

    def __update_leaderboard(self):
        score_list = [s for s in self.leaderboard.values()]
        score_list.append(int(self.score))
        score_list.sort(reverse=True)
        score_list.pop(-1)
        i = 0
        for n in self.leaderboard:
            self.leaderboard[n] = score_list[i]
            i += 1
        print(self.leaderboard)
        self._update_score_json()

    # Pressing >1 box flow, PRESSDOWN -> __update -> PRESSUP -> kill()
    def __press_DOWN_method(self, lane_index):
        checking_box = self.__get_checking_box(lane_index)
        if checking_box is not None:
            if not checking_box.isLongNote:
                self.__score_calc(
                    self.__get_successful(self.checker_boxes_list[lane_index].rect, checking_box.rect))
                checking_box.kill()
            else:
                self.__score_calc(
                    self.__get_successful(self.checker_boxes_list[lane_index].rect, checking_box.rect))
                self.isLongPressing[lane_index] = True
                self.__update_long_note()
            # print(
            #     f"log: pressed d {self.note_in_lane[lane_index][1][0] if len(self.note_in_lane[lane_index][1]) > 0 else None}")

    def __press_UP_method(self, lane_index):
        checking_box = self.__get_checking_box(lane_index)
        if checking_box is not None and checking_box.isLongNote:
            self.__score_calc(
                self.__get_successful(self.checker_boxes_list[lane_index].rect, checking_box.rect))
            self.isLongPressing[lane_index] = False
            self.__update_long_note()

            lane_list = self.note_in_lane[lane_index][1]

            # print(
            #     f"log: pressed d {self.note_in_lane[lane_index][1][0] if len(self.note_in_lane[lane_index][1]) > 0 else None}")


    def run(self):

        # Play Song
        if game_settings["music"]:
            self.music_volume = 0.8
        else:
            self.music_volume = 0

        self.play_song()

        self.play_song()

        while self.isRunning:
            # Reset screen
            self.screen.fill(SCREEN_BACKGROUND)
            self.draw_background()

            # Update state
            self.__update_tempo()
            self.update_static()
            self.update_dynamic()

            # Draw Edge line
            pygame.draw.line(self.screen, (27, 48, 91), (GAME_WIDTH_CENTER - 440, 0),
                             (GAME_WIDTH_CENTER - 440, SCREEN_HEIGHT), 12)
            pygame.draw.line(self.screen, (27, 48, 91), (GAME_WIDTH_CENTER + 440, 0),
                             (GAME_WIDTH_CENTER + 440, SCREEN_HEIGHT), 12)

            # Kill outbound notes
            for lane in self.note_in_lane:
                # Iterate backwards using indices
                lane = lane[1]
                for j in range(len(lane) - 1, -1, -1):
                    box = lane[j]

                    # Check if the box is below the screen height
                    if box.rect.y > 700:
                        box.kill()  # Remove from Pygame groups
                        lane.pop(j)  # Remove from the Python list by index

            # Ending game with 2 seconds delay
            if self.isEnded:
                self.tick_delay_end_counter += 1
                if self.tick_delay_end_counter == int(self.tick_per_beat * 2):
                    self.isRunning = False
                    self.end_game()

            # Event checker_fx
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
                        self.__press_DOWN_method(0)
                    if event.key == pygame.K_f:
                        self.__press_DOWN_method(1)
                    if event.key == pygame.K_j:
                        self.__press_DOWN_method(2)
                    if event.key == pygame.K_k:
                        self.__press_DOWN_method(3)

                    # Update long note color (Special Case)
                    self.__update_long_note()

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_d:
                        self.isLongPressing[0] = False
                        self.__kill_long_note(0)
                        self.__press_UP_method(0)

                    if event.key == pygame.K_f:
                        self.isLongPressing[1] = False
                        self.__kill_long_note(1)
                        self.__press_UP_method(1)

                    if event.key == pygame.K_j:
                        self.isLongPressing[2] = False
                        self.__kill_long_note(2)
                        self.__press_UP_method(2)

                    if event.key == pygame.K_k:
                        self.isLongPressing[3] = False
                        self.__kill_long_note(3)
                        self.__press_UP_method(3)

                    # Update long note color (Special Case)
                    self.__update_long_note()

            # self.score_counter_text.update_text(int(self.score))
            # print("log: isPressing:", self.isPressing)

            self.clock.tick(self.tick_per_beat)
            pygame.display.flip()

        if (not self.isRunning and not self.isPause) or self.isEnded:
            self.stop_song()


def run(song_name):
    print('game_instance!!!')
    game_instance = GamePage(song_name)
    game_instance.run()
    return "song_select"
