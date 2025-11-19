import pygame, sys
import ui.ui as ui  # ใช้ UI กลาง
from config.PageConstant import SCREEN_CENTER, SCREEN_DIMENSION
from config.game_config import *

WIDTH, HEIGHT = 1200, 800


def draw_background_image():
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

    return static_bg_image


def run(screen, dt):
    ui.init_fonts()
    clock = pygame.time.Clock()

    if not hasattr(run, "_inited"):
        run._inited = True

        # Fonts & Colors (ดึงจาก ui)
        run.FONT_TITLE = ui.FONT_TITLE
        run.FONT_LABEL = ui.FONT_SUB     # ขนาด 34 ใกล้เคียง label เดิม
        run.FONT_BTN   = ui.FONT_BTN

        run.BG_COLOR = ui.BG_COLOR
        run.BTN_FILL = ui.BTN_FILL
        run.BTN_TEXT = ui.BTN_TEXT
        run.WHITE    = ui.WHITE

        # สีสำหรับ toggle เฉพาะ setting
        run.SW_TRACK_OFF = (0, 0, 0)
        run.SW_TRACK_ON  = (34, 72, 122)
        run.SW_KNOB      = (235, 235, 235)

        # ---- classes ----
        class ToggleSwitch:
            def __init__(self, right_center, track_size=(160, 56), radius=28, value=False, callback=None):
                self.center = pygame.Vector2(right_center)
                self.tw, self.th = track_size
                self.radius = radius
                self.value = value
                self.anim = 1.0 if value else 0.0
                self.target = self.anim

                self.callback = callback

            def rect(self):
                r = pygame.Rect(0, 0, self.tw, self.th)
                r.center = (int(self.center.x), int(self.center.y))
                return r

            def update(self, _mouse_pos, dt):
                self.anim += (self.target - self.anim) * min(1.0, 12.0 * dt)

            def draw(self, surface):
                r = self.rect()
                col = (
                    int(run.SW_TRACK_OFF[0] * (1 - self.anim) + run.SW_TRACK_ON[0] * self.anim),
                    int(run.SW_TRACK_OFF[1] * (1 - self.anim) + run.SW_TRACK_ON[1] * self.anim),
                    int(run.SW_TRACK_OFF[2] * (1 - self.anim) + run.SW_TRACK_ON[2] * self.anim),
                )
                pygame.draw.rect(surface, col, r, border_radius=self.radius)

                pad = 6
                knob_r = self.th - pad * 2
                knob_min_x = r.x + pad
                knob_max_x = r.right - pad - knob_r
                knob_x = int(knob_min_x + (knob_max_x - knob_min_x) * self.anim)

                pygame.draw.ellipse(
                    surface,
                    run.SW_KNOB,
                    pygame.Rect(knob_x, r.y + pad, knob_r, knob_r),
                )

            def handle_event(self, event):
                if event.type == pygame.MOUSEBUTTONDOWN and self.rect().collidepoint(event.pos):
                    self.value = not self.value
                    self.target = 1.0 if self.value else 0.0

                    if self.callback is not None:
                        self.callback(self.value)


        class SettingRow:
            def __init__(self, label, y, switch_default=False, callback=None):
                self.label = label
                self.box_rect = pygame.Rect(WIDTH // 2 - 420, y - 36, 840, 72)
                self.switch = ToggleSwitch((self.box_rect.right - 90, y), value=switch_default, callback=callback)

            def update(self, mouse_pos, dt):
                self.switch.update(mouse_pos, dt)

            def draw(self, surface):
                pygame.draw.rect(surface, run.BTN_FILL, self.box_rect, border_radius=36)
                text = run.FONT_LABEL.render(self.label, False, run.BTN_TEXT)
                surface.blit(
                    text,
                    (self.box_rect.x + 32, self.box_rect.centery - text.get_height() // 2),
                )
                self.switch.draw(surface)

            def handle_event(self, event):
                self.switch.handle_event(event)

        # เก็บไว้ใน run
        run.SettingRow = SettingRow
        run.ToggleSwitch = ToggleSwitch

        # create once
        run.rows = [
            # SettingRow("MV Background", y=250, switch_default=game_settings["mv"], callback=config_mv),
            SettingRow("Music",         y=250, switch_default=game_settings["music"], callback=config_music),
        ]
        run.buttons = [
            ui.Button("BACK", (WIDTH // 2, 650)),
        ]

    # ---- Event loop ----
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return "quit"

        for row in run.rows:
            row.handle_event(event)

        for b in run.buttons:
            if b.was_clicked(event):
                if b.text == "BACK":
                    return "start"

    mouse = pygame.mouse.get_pos()
    for row in run.rows:
        row.update(mouse, dt)
    for b in run.buttons:
        b.update(mouse, dt)

    # ---- Draw ----
    screen.fill(run.BG_COLOR)
    draw_background_image(screen)

    # title
    title = run.FONT_TITLE.render("SETTING", False, run.WHITE)
    screen.blit(title, title.get_rect(center=(WIDTH // 2, 120)))

    for row in run.rows:
        row.draw(screen)
    for b in run.buttons:
        b.draw(screen)

    pygame.display.flip()
    return None
