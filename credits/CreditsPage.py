import pygame
import sys
from config.FontConstant import FONT_PATH
from config.PageConstant import SCREEN_BACKGROUND
from util.Screen import Screen
from util.Text import Text
from itertools import cycle
from PIL import Image  # ใช้แยกเฟรมของ GIF


class CreditsPage(Screen):
    def __init__(self):
        super().__init__()

        __background = pygame.Color(13, 0, 30)
        __name = "Credits - YeaYeaRythm"
        self.screen = self.setup(__background, __name)

        self.clock = pygame.time.Clock()
        self.isRunning = True

        # --- โหลด GIF พื้นหลัง ---
        # self.frames = self.load_gif_frames("assets/gif/8904fb777b93efc7bd4b8aa22482672a.gif")
        # self.frame_cycle = cycle(self.frames)

        # --- ฟอนต์ ---
        self.title_font = pygame.font.Font(FONT_PATH, 100)
        self.text_font = pygame.font.Font(FONT_PATH, 35)
        self.button_font = pygame.font.Font(FONT_PATH, 55)

        # --- กล่องและปุ่ม ---
        self.credit_box = pygame.Rect(350, 250, 500, 250)
        self.button_rect = pygame.Rect(540, 650, 140, 60)

        self.credits = [
            "Watchara Wattanalaosomboon 6834453823",
            "Pattarapon Kitkamonsawet 6834444123",
            "Primrada Thitasomboon 6834438423"
        ]

    # GIF เป็น list ของภาพ
    # def load_gif_frames(self, filename):
    #     gif_dir = "assets/gif/8904fb777b93efc7bd4b8aa22482672a.gif"
    #     gif_surface = pygame.image.load(gif_dir)
    #     im = Image.open(filename)
    #     frames = []
    #     try:
    #         while True:
    #             frame = im.convert('RGBA')
    #             pygame_img = pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode)
    #             pygame_img = pygame.transform.scale(pygame_img, (1200, 800))
    #             pygame_img.set_alpha(77)  # ความจาง 30% (255 * 0.3 ≈ 77)
    #             frames.append(pygame_img)
    #             im.seek(im.tell() + 1)
    #     except EOFError:
    #         pass
    #     return frames

    def draw(self):
        self.bg_color = SCREEN_BACKGROUND
        frame = next(self.frame_cycle)
        self.screen.fill(self.bg_color)
        self.screen.blit(frame, (0, 0))

        # หัวข้อ
        title = self.title_font.render("CREDIT", True, (255, 255, 255))
        self.screen.blit(title, (600 - title.get_width() // 2, 50))

        # กล่องสีเทา
        pygame.draw.rect(self.screen, (200, 200, 200), self.credit_box.move(0, -35))


        # รายชื่อ
        y = 510
        for line in self.credits:
            txt = self.text_font.render(line, True, (255, 255, 255))
            self.screen.blit(txt, (600 - txt.get_width() // 2, y))
            y += 50

        # ปุ่ม HOME
        #pygame.draw.ellipse(self.screen, (240, 240, 240), self.button_rect)
        #btn_text = self.button_font.render("HOME", True, (25, 25, 60))
        #self.screen.blit(
           # btn_text,
            #(self.button_rect.centerx - btn_text.get_width() // 2,
             #self.button_rect.centery - btn_text.get_height() // 2)
        #)
        offset_y = 40  # จำนวนพิกเซลที่อยากขยับลง
        moved_rect = self.button_rect.move(0, offset_y)

        pygame.draw.ellipse(self.screen, (240, 240, 240), moved_rect)
        btn_text = self.button_font.render("HOME", True, (25, 25, 60))
        self.screen.blit(
          btn_text,
          (moved_rect.centerx - btn_text.get_width() // 2,
          moved_rect.centery - btn_text.get_height() // 2)
        )

    def run(self):
        while self.isRunning:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.isRunning = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.isRunning = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button_rect.collidepoint(event.pos):
                        print("Back to HOME")
                        self.isRunning = False

            self.draw()
            pygame.display.flip()
            self.clock.tick(12)  # FPS สำหรับ GIF

        pygame.quit()

#เชื่อมกับ main
def run():
    page = CreditsPage()   # สร้างหน้าเครดิต
    page.run()             # ให้มันรัน loop ของมันเอง
    return "start"         # กลับไปหน้า start หลังจากปิดเครดิต
