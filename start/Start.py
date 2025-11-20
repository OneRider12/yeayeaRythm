import pygame, sys, random
import ui.ui as ui  # ใช้ UI กลาง
from config.PageConstant import SCREEN_DIMENSION

WIDTH, HEIGHT = 1200, 800


def __draw_background_image(screen):
    """Loads the static background image with alpha channel."""
    try:
        # Load the image and preserve transparency (convert_alpha)
        static_bg_image = pygame.image.load('assets/image/background_image.png').convert_alpha()

        # Scale it to the screen size (assuming it should fill the screen)
        static_bg_image = pygame.transform.scale(static_bg_image, SCREEN_DIMENSION)

        # Optional: Set a global transparency if needed (e.g., 50% opacity)
        static_bg_image.set_alpha(128)

    except pygame.error as e:
        print(f"Failed to load static background image: {e}")
        # Fallback surface with semi-transparent color
        static_bg_image = pygame.Surface(SCREEN_DIMENSION, pygame.SRCALPHA)
        static_bg_image.fill((27, 48, 91, 255))

    screen.blit(static_bg_image, (0, 0))


def run(screen, dt):
    # เตรียมฟอนต์กลาง
    ui.init_fonts()

    if not hasattr(run, "_inited"):
        run._inited = True

        # สร้างปุ่มครั้งเดียว
        run.buttons = [
            ui.Button("PLAY",        (WIDTH // 2, 300)),
            ui.Button("SETTING", (WIDTH // 2, 420)),
            ui.Button("CREDIT",     (WIDTH // 2, 540)),
            ui.Button("QUIT",      (WIDTH // 2, 660)),
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
                elif b.text == "QUIT":
                    return "quit"
                elif b.text == "CREDIT":
                    return "credit"

    # --- Update ---
    mouse = pygame.mouse.get_pos()
    for b in run.buttons:
        b.update(mouse, dt)

    # --- Draw ---
    screen.fill(ui.BG_COLOR)
    __draw_background_image(screen)

    title = ui.FONT_TITLE.render("YeaYea RHYTHM", False, ui.WHITE)
    sub   = ui.FONT_SUB.render("By whatever", False, ui.WHITE)

    screen.blit(title, title.get_rect(center=(WIDTH // 2, 120)))
    screen.blit(sub,   sub.get_rect(center=(WIDTH // 2, 190)))

    for b in run.buttons:
        b.draw(screen)

    pygame.display.flip()
    return None
