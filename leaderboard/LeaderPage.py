import pygame

import sys
from config.FontConstant import FONT_PATH
from config.PageConstant import SCREEN_BACKGROUND
from util.Screen import Screen
from util.Text import Text
from itertools import cycle
from PIL import Image  # ใช้แยกเฟรมของ GIF
from math import radians

class LeaderPage(Screen):
    def __init__(self):
        super().__init__()

        # ตั้งค่าหน้าจอ (ใช้ method จาก Screen เหมือน CreditsPage)
        __background = pygame.Color(13, 0, 30)
        __name = "Leaderboard - YeaYeaRythm"
        self.screen = self.setup(__background, __name)

        self.clock = pygame.time.Clock()
        self.isRunning = True

        # 🎨 ฟอนต์
        self.font_title = pygame.font.Font(FONT_PATH, 48)
        self.font_label = pygame.font.Font(FONT_PATH, 35)
        self.font_button = pygame.font.Font(FONT_PATH, 55)

        # 🎨 สี
        self.text_color = (255, 255, 255)
        self.box_color = (255, 254, 224)
        self.number_color = (25, 25, 60)
        self.button_color = (240, 240, 240)
        self.button_shadow = (80, 90, 130)

        # พื้นที่ฝั่งขวา 
        self.panel_x = 350

        # ปุ่ม
        self.play_rect = pygame.Rect(self.panel_x + 150, 870, 200, 70)
        self.home_rect = pygame.Rect(self.panel_x + 150, 960, 200, 70)

        # รายชื่ออันดับ
        self.ranks = [
            ("A", "9800"),
            ("B", "8700"),
            ("C", "8600")
        ]

    def draw(self):
        self.screen.fill(SCREEN_BACKGROUND)

        # 🏆 หัวข้อ Leaderboard
        title = self.font_title.render("LEADERBOARD", True, self.text_color)
        self.screen.blit(title, (735, 141))

        # 🔳 กล่องอันดับ 1–3
        fixed_x = 722
        start_y = 247
        # ขนาดกล่อง
        box_width = 335
        box_height = 64
        border_radius = 25

       # ระยะห่างแนวตั้งระหว่างกล่อง
        gap_y = 112
        for i, (name, score) in enumerate(self.ranks):
          rect = pygame.Rect(fixed_x, start_y + i * gap_y, box_width, box_height)
          pygame.draw.rect(self.screen, self.box_color, rect, border_radius=border_radius)

          # อันดับ
          num_text = self.font_label.render(str(i + 1), True, self.number_color)
          self.screen.blit(num_text, (rect.x + 20, rect.y + 10))

          # ชื่อ
          name_text = self.font_label.render(name, True, (70, 70, 90))
          self.screen.blit(name_text, (rect.x + 90, rect.y + 10))
 
          # คะแนน
          score_text = self.font_label.render(score, True, (100, 100, 120))
          self.screen.blit(score_text, (rect.x + 230, rect.y + 10))

        image = pygame.image.load("assets/crown/crown-removebg-preview.png").convert_alpha()  # convert_alpha() ถ้ารูปมีโปร่งใส
        # กำหนดตำแหน่ง
        x, y = 692, 188
        rect = image.get_rect()
        rect.topleft = (x, y)  # ตั้งมุมซ้ายบนที่ x=692, y=188
        # วาดรูปบนหน้าจอ
        self.screen.blit(image, rect)
        
        # 🟣 ปุ่ม PLAY
        self.draw_button(self.play_rect, "PLAY")
        # 🟣 ปุ่ม HOME
        self.draw_button(self.home_rect, "HOME")

    def draw_button(self, rect, text):
        # เงา
        shadow_rect = rect.move(0, 6)
        pygame.draw.ellipse(self.screen, self.button_shadow, shadow_rect)
        # ปุ่ม
        pygame.draw.ellipse(self.screen, self.button_color, rect)
        label = self.font_button.render(text, True, (25, 25, 60))
        self.screen.blit(
            label,
            (rect.centerx - label.get_width() // 2,
             rect.centery - label.get_height() // 2)
        )

    def run(self):
        while self.isRunning:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.isRunning = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.isRunning = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.home_rect.collidepoint(event.pos):
                        print("Back to HOME")
                        self.isRunning = False
                    elif self.play_rect.collidepoint(event.pos):
                        print("Go to GAME")
                        self.isRunning = False

            self.draw()
            pygame.display.flip()
            self.clock.tick(12)

        pygame.quit()
