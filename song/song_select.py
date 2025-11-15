import pygame, sys
import ui.ui as ui   #จาก ui.py
from config.song_dir import *
from game.GamePage2 import GamePage

WIDTH, HEIGHT = 1200, 800


def run(screen, dt):
    ui.init_fonts()

    if not hasattr(run, "_inited"):
        run._inited = True

        # ---------- ฟอนต์เฉพาะหน้าเลือกเพลง ----------
        run.FONT_TITLE_SMALL = pygame.font.Font(ui.FONT_PATH, 60)
        run.FONT_LABEL       = pygame.font.Font(ui.FONT_PATH, 25)
        run.player       = pygame.font.Font(ui.FONT_PATH, 20)

        # ---------- คลาสปุ่มเพลง ----------
        run.SongButton = SongButton

        # ---------- ปุ่มเพลง 5 ปุ่ม ----------
        song_center_x = 350     # <---- ขยับซ้าย/ขวา
        first_y = 210           # <---- ขยับขึ้น/ลง
        gap_y = 120             # <---- ระยะห่างระหว่างปุ่ม
       
        run.song_buttons = [
            SongButton("Song 1", 1, (song_center_x, first_y + 0 * gap_y)),
            SongButton("Song 2", 1, (song_center_x, first_y + 1 * gap_y)),
            SongButton("APT.", 2, (song_center_x, first_y + 2 * gap_y)),
            SongButton("Song 4", 3, (song_center_x, first_y + 3 * gap_y)),
            SongButton("Song 5", 3, (song_center_x, first_y + 4 * gap_y)),
        ]

        # ---------- ปุ่ม PLAY / HOME ด้านขวาล่าง ----------
        run.play_button = ui.Button("PLAY", (925, 600), size=(260, 70), radius=35)
        run.home_button = ui.Button("HOME", (925, 700), size=(260, 70), radius=35)

        # ---------- ข้อมูล Leaderboard 5 ชุด ----------
        run.leaderboards = [
            [("AAA", "100000"), ("BBB", "80000"), ("CCC", "60000")],
            [("DDD", "90000"),  ("EEE", "70000"), ("FFF", "50000")],
            [("GGG", "120000"), ("HHH", "90000"), ("III", "65000")],
            [("JJJ", "150000"), ("KKK", "110000"), ("LLL", "90000")],
            [("MMM", "200000"), ("NNN", "150000"), ("OOO", "120000")],
        ]
        run.active_song_index = 0  # default

        # สีกล่อง leaderboard 
        run.LB_BOX_COLOR = (250, 248, 220)

    mouse = pygame.mouse.get_pos()

    # -------- Update 1 ----------
    hover_index = None
    for i, b in enumerate(run.song_buttons):
        b.update(mouse, dt)
        if b.rect().collidepoint(mouse):
            hover_index = i

    if hover_index is not None:
        run.active_song_index = hover_index
        run.SongButton.song_index = hover_index

    # ---------- Event ----------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return "quit"

        if event.type == pygame.MOUSEBUTTONDOWN:
            if run.play_button.was_clicked(event):
                # print(run.SongButton.song_index + 1)
                return f"song0{run.SongButton.song_index + 1}"
            if run.home_button.was_clicked(event):
                return "start"

    # --------- Update 2 ----------
    run.play_button.update(mouse, dt)
    run.home_button.update(mouse, dt)

    # ---------- Draw ----------
    screen.fill(ui.BG_COLOR)

    # หัวข้อ Songs
    songs_title = run.FONT_TITLE_SMALL.render("Songs", True, ui.WHITE)
    screen.blit(songs_title, (90, 60))

    # หัวข้อ Leaderboard
    lb_title = run.FONT_TITLE_SMALL.render("Leaderboard", True, ui.WHITE)
    # ตำแหน่ง
    screen.blit(lb_title, (720, 100))

    # ปุ่มเพลงฝั่งซ้าย
    for b in run.song_buttons:
        b.draw(screen)

    # Leaderboard ของเพลงที่ active อยู่
    lb_set = run.leaderboards[run.active_song_index]

    base_y = 210
    gap_y = 110
    box_w, box_h = 320, 75
    box_x = 760

    for rank, (name, score) in enumerate(lb_set, start=1):
        y = base_y + (rank - 1) * gap_y
        rect = pygame.Rect(box_x, y, box_w, box_h)
        # เลือกสีขอบตามอันดับ
        if rank == 1:
            border_color = (255, 215, 0)       # ทอง
        elif rank == 2:
            border_color = (200, 200, 200)     # เงิน
        elif rank == 3:
            border_color = (205, 127, 50)      # ทองแดง
        else:
            border_color = (0, 0, 0)           # สำรอง (กรณีมีอันดับอื่น)

        # วาดพื้นกล่อง
        pygame.draw.rect(screen, run.LB_BOX_COLOR, rect, border_radius=35)

        # วาดขอบ (stroke)
        pygame.draw.rect(screen, border_color, rect, width=4, border_radius=35)

        # อันดับ
        rank_text = run.FONT_LABEL.render(str(rank), True, ui.BTN_TEXT)
        screen.blit(rank_text, (rect.x + 25, rect.centery - rank_text.get_height() // 2))

        # ชื่อ & score
        name_text = run.player.render(name, True, ui.BTN_TEXT)
        screen.blit(name_text, (rect.x + 85, rect.y + 10))

        score_text = run.player.render(score, True, ui.BTN_TEXT)
        surface_y = rect.y + 10 + name_text.get_height() + 4
        screen.blit(score_text, (rect.x + 85, surface_y))

    # ปุ่ม PLAY / HOME
    run.play_button.draw(screen)
    run.home_button.draw(screen)

    pygame.display.flip()
    return None


class SongButton(ui.Button):
    def __init__(self, name, stars, center):
        # กล่องยาวฝั่งซ้าย
        super().__init__("", center, size=(520, 90), radius=35)
        self.song_name = name
        self.stars = stars  # 1–3 ดาว

        self.song_index = 0
        self.song_json_dir = f"/song0{self.song_index + 1}.json"

    def draw(self, surface):
        # วาดกล่องหลัก + เงา + animation
        super().draw(surface)
        r = self.rect()

        # แถบสีเทาด้านซ้าย (เหมือนช่องใน mockup)
        thumb_w = int(r.width * 0.22)
        thumb_rect = pygame.Rect(r.x, r.y, thumb_w, r.height)
        pygame.draw.rect(surface, (230, 230, 230),
                         thumb_rect, border_radius=int(self.radius * self.scale))

        # ชื่อเพลง (วางด้านขวาของแถบเทา)
        name_x = r.x + thumb_w + 24
        name_y = r.y + 15
        name_surf = run.FONT_LABEL.render(self.song_name, True, ui.BTN_TEXT)
        surface.blit(name_surf, (name_x, name_y))

        # แสดง Level
        level_text = f"Lv.{self.stars}"
        lvl_surf = run.FONT_LABEL.render(level_text, True, (0, 0, 0))
        surface.blit(lvl_surf, (name_x, name_y + name_surf.get_height() + 6))

