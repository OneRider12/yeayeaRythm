import pygame

from config.BoxConstant import *
from config.FontConstant import *
from config.PageConstant import *
from config.EngineConfig import EngineConfig
from util.Box import Box
from util.Screen import Screen
from util.Text import Text


class GamePage(Screen, EngineConfig):
    def __init__(self):
        Screen().__init__()
        EngineConfig.__init__(self)

        self.score_header = None
        self.screen = self.setup(SCREEN_BACKGROUND, GAME_TITLE)

        self.ui = pygame.sprite.Group()
        self.score_ui = pygame.sprite.Group()
        self.playfield = pygame.sprite.Group()
        self.checker_boxes = pygame.sprite.Group()

        # self.box = Box((100, 120), (255, 255, 100), SCREEN_CENTER)
        # self.align_line = Box((9, SCREEN_HEIGHT), GAME_ALIGN_LINE_COLOR, (GAME_ALIGN_LINE_MARGIN, SCREEN_HEIGHT_CENTER))
        # self.text = Text("TEST TEXT", HEADER80, pygame.Color(255, 255, 255), self.screen, (SCREEN_HEIGHT/2, 100))
        #
        # self.ui.add(self.box, self.align_line, self.text)

        self.counter = 0
        self.tick_per_tempo = 60
        self.tick_counter = 0

        self.draft_all()

    def draft_all(self):

        self.score_header_text = Text(GAME_SCORE_HEADING_TEXT, NORMAL24, GAME_SCORE_HEADING_COLOR, self.screen,
                                      GAME_SCORE_HEADING_BOX_COORD)
        self.score_counter_text = Text(str(self.counter), HEADER48, GAME_SCORE_COUNTER, self.screen,
                                       GAME_SCORE_COUNTER_COORD)
        self.score_header_box = Box(GAME_SCORE_HEADING_BOX_SIZE, GAME_SCORE_HEADING_BOX_COLOR,
                                    GAME_SCORE_HEADING_BOX_COORD)
        self.score_ui.add(self.score_header_box, self.score_header_text, self.score_counter_text)

        self.item_lane1_box = Box(GAME_SCORE_HEADING_BOX_SIZE, BOX_ITEM_COLOR[0], (100, SCREEN_HEIGHT_CENTER))
        self.item_lane2_box = Box(GAME_SCORE_HEADING_BOX_SIZE, BOX_ITEM_COLOR[1], (400, SCREEN_HEIGHT_CENTER))
        self.item_lane3_box = Box(GAME_SCORE_HEADING_BOX_SIZE, BOX_ITEM_COLOR[2], (700, SCREEN_HEIGHT_CENTER))
        self.item_lane4_box = Box(GAME_SCORE_HEADING_BOX_SIZE, BOX_ITEM_COLOR[3], (1000, SCREEN_HEIGHT_CENTER))
        self.tempo_line_box = Box(BOX_TEMPO_SIZE, BOX_TEMPO_COLOR, BOX_TEMPO_COORD)
        self.playfield.add(self.item_lane1_box, self.item_lane2_box, self.item_lane3_box, self.item_lane4_box,
                           self.tempo_line_box)

        self.checker_lane1_box = Box(BOX_CHECKER_OUTER_SIZE, BOX_CHECKER_COLOR, BOX_CHECKER1_COORD)
        self.checker_lane2_box = Box(BOX_CHECKER_INNER_SIZE, BOX_CHECKER_COLOR, BOX_CHECKER2_COORD)
        self.checker_lane3_box = Box(BOX_CHECKER_INNER_SIZE, BOX_CHECKER_COLOR, BOX_CHECKER3_COORD)
        self.checker_lane4_box = Box(BOX_CHECKER_OUTER_SIZE, BOX_CHECKER_COLOR, BOX_CHECKER4_COORD)
        self.checker_boxes.add(self.checker_lane1_box, self.checker_lane2_box, self.checker_lane3_box,
                               self.checker_lane4_box)

    def update_static(self):

        self.ui.add(self.score_ui, self.playfield, self.checker_boxes)

        self.ui.update()
        self.screen.fill(SCREEN_BACKGROUND)
        self.ui.draw(self.screen)

    def update_dynamic(self):
        # Update position of moving box
        pass

    def update_tempo(self):
        # Generate Tempo line and note
        pass

    def pause_game(self):
        self.clock.tick(0)
        print("**PAUSE**")
        self.clock.tick(60)

    def run(self):

        while self.isRunning:
            self.update_static()
            self.update_dynamic()

            if self.tick_counter == self.tick_per_tempo:
                self.update_tempo()

            self.edge_outer1_line = pygame.draw.line(self.screen, GAME_EDGE_COLOR, GAME_EDGE1_COORD_START,
                                                     GAME_EDGE1_COORD_END, 12)
            self.edge_outer2_line = pygame.draw.line(self.screen, GAME_EDGE_COLOR, GAME_EDGE2_COORD_START,
                                                     GAME_EDGE2_COORD_END, 12)

            self.edge_innner1_line = pygame.draw.line(self.screen, GAME_EDGE_INNER_LINE_COLOR,
                                                      GAME_EDGE_INNER1_COORD_START,
                                                      GAME_EDGE_INNER1_COORD_END, 10)
            self.edge_innner2_line = pygame.draw.line(self.screen, GAME_EDGE_INNER_LINE_COLOR,
                                                      GAME_EDGE_INNER2_COORD_START,
                                                      GAME_EDGE_INNER2_COORD_END, 10)

            self.edge_center_line = pygame.draw.line(self.screen, GAME_EDGE_INNER_LINE_COLOR,
                                                     GAME_EDGE_CENTER_LINE_START,
                                                     GAME_EDGE_CENTER_LINE_END, 10)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.isRunning = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.isRunning = False
                    if event.key == pygame.K_ESCAPE:
                        self.pause_game()

                    if event.key == pygame.K_s:
                        self.counter += 1
                        self.score_counter_text.update_text(self.counter)
                        print("s")
                    if event.key == pygame.K_d:
                        self.counter += 1
                        self.score_counter_text.update_text(self.counter)
                        print("d")
                    if event.key == pygame.K_g:
                        self.counter += 1
                        self.score_counter_text.update_text(self.counter)
                        print("g")
                    if event.key == pygame.K_h:
                        self.counter += 1
                        self.score_counter_text.update_text(self.counter)
                        print("h")

            self.tick_counter += 1

            self.clock.tick(60)
            pygame.display.flip()
