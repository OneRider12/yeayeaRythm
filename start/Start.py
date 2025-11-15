import pygame, sys, random
import ui.ui as ui  # ใช้ UI กลาง

WIDTH, HEIGHT = 1200, 800


def run(screen, dt):
    # เตรียมฟอนต์กลาง
    ui.init_fonts()

    if not hasattr(run, "_inited"):
        run._inited = True

        # สร้างปุ่มครั้งเดียว
        run.buttons = [
            ui.Button("PLAY",        (WIDTH // 2, 300)),
            ui.Button("LEADERBOARD", (WIDTH // 2, 420)),
            ui.Button("SETTING",     (WIDTH // 2, 540)),
            ui.Button("CREDIT",      (WIDTH // 2, 660)),
        ]

    # --- Events ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return "quit"

        for b in run.buttons:
            if b.was_clicked(event):
                if b.text == "SETTING":
                    return "setting"
                elif b.text == "PLAY":
                    return "song_select"
                elif b.text == "LEADERBOARD":
                    return "leaderboard"
                elif b.text == "CREDIT":
                    return "credit"

    # --- Update ---
    mouse = pygame.mouse.get_pos()
    for b in run.buttons:
        b.update(mouse, dt)

    # --- Draw ---
    screen.fill(ui.BG_COLOR)

    title = ui.FONT_TITLE.render("YeaYea RHYTHM", False, ui.WHITE)
    sub   = ui.FONT_SUB.render("By whatever", False, ui.WHITE)

    screen.blit(title, title.get_rect(center=(WIDTH // 2, 120)))
    screen.blit(sub,   sub.get_rect(center=(WIDTH // 2, 190)))

    for b in run.buttons:
        b.draw(screen)

    pygame.display.flip()
    return None
