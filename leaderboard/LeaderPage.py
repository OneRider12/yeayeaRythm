import pygame
from util.Screen import Screen
from config.FontConstant import FONT_PATH
from config.PageConstant import SCREEN_BACKGROUND


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
        self.font_title = pygame.font.Font(FONT_PATH, 100)
        self.font_label = pygame.font.Font(FONT_PATH, 45)
        self.font_button = pygame.font.Font(FONT_PATH, 55)

        # 🎨 สี
        self.text_color = (255, 255, 255)
        self.box_color = (240, 240, 240)
        self.number_color = (25, 25, 60)
        self.button_color = (240, 240, 240)
        self.button_shadow = (80, 90, 130)

        # พื้นที่ฝั่งขวา (ใช้ดีไซน์เดียวกับหน้า CreditsPage)
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
        self.screen.blit(title, (600 - title.get_width() // 2, 80))

        # 🔳 กล่องอันดับ 1–3
        rank_y = 300
        rank_gap = 120
        for i, (name, score) in enumerate(self.ranks):
            rect = pygame.Rect(self.panel_x + 100, rank_y + i * rank_gap, 500, 90)
            pygame.draw.rect(self.screen, self.box_color, rect, border_radius=35)

            # อันดับ
            num_text = self.font_label.render(str(i + 1), True, self.number_color)
            self.screen.blit(num_text, (rect.x + 30, rect.y + 20))

            # ชื่อ
            name_text = self.font_label.render(name, True, (70, 70, 90))
            self.screen.blit(name_text, (rect.x + 130, rect.y + 20))

            # คะแนน
            score_text = self.font_label.render(score, True, (100, 100, 120))
            self.screen.blit(score_text, (rect.x + 380, rect.y + 20))

            # 👑 มงกุฎเฉพาะอันดับ 1
            if i == 0:
                pygame.draw.polygon(
                    self.screen, (255, 215, 0),
                    [
                        (rect.x + 60, rect.y - 25),
                        (rect.x + 80, rect.y),
                        (rect.x + 100, rect.y - 25),
                        (rect.x + 120, rect.y),
                        (rect.x + 140, rect.y - 25)
                    ]
                )

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
            self.clock.tick(60)

        pygame.quit()
