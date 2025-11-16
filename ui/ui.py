import pygame

# --- Global config for UI ---
FONT_PATH = "assets/fonts/PixelifySans-VariableFont_wght.ttf"

# Colors
BG_COLOR        = (27, 48, 91)
BTN_FILL        = (240, 240, 240)
BTN_FILL_HOVER  = (255, 255, 255)
BTN_TEXT        = (27, 48, 91)
WHITE           = (255, 255, 255)

# Fonts
FONT_TITLE = None  # 92
FONT_SUB   = None  # 34
FONT_BTN   = None  # 44


def init_fonts():
    global FONT_TITLE, FONT_SUB, FONT_BTN
    if FONT_TITLE is not None:
        return

    try:
        FONT_TITLE = pygame.font.Font(FONT_PATH, 92)
        FONT_SUB   = pygame.font.Font(FONT_PATH, 34)
        FONT_BTN   = pygame.font.Font(FONT_PATH, 44)
    except:
        FONT_TITLE = pygame.font.SysFont("Consolas", 92, bold=True)
        FONT_SUB   = pygame.font.SysFont("Consolas", 34)
        FONT_BTN   = pygame.font.SysFont("Consolas", 54, bold=True)


class Button(pygame.sprite.Sprite):
    def __init__(self, text, center, size=(400, 80), radius=40):
        super().__init__()

        self.text = text
        self.center = pygame.Vector2(center)
        self.base_w, self.base_h = size
        self.radius = radius
        self.scale = 1.0
        self.target_scale = 1.0
        self.shadow_alpha = 90
        self.elev = 6  # ระยะเงา

    def rect(self):
        w = int(self.base_w * self.scale)
        h = int(self.base_h * self.scale)
        r = pygame.Rect(0, 0, w, h)
        r.center = self.center
        return r

    def update(self, mouse_pos, dt):
        self.target_scale = 1.08 if self.rect().collidepoint(mouse_pos) else 1.0
        self.scale += (self.target_scale - self.scale) * min(1.0, 10.0 * dt)

    def draw(self, surface):
        if FONT_BTN is None:
            raise RuntimeError("Call ui.init_fonts() before drawing buttons.")

        r = self.rect()

        # shadow
        sh = pygame.Surface((r.width, r.height), pygame.SRCALPHA)
        pygame.draw.rect(
            sh,
            (0, 0, 0, int(self.shadow_alpha * (0.9 if self.target_scale > 1 else 0.6))),
            sh.get_rect(),
            border_radius=int(self.radius * self.scale),
        )
        surface.blit(sh, (r.x, r.y + self.elev))

        # body
        fill = BTN_FILL_HOVER if self.target_scale > 1 else BTN_FILL
        pygame.draw.rect(surface, fill, r, border_radius=int(self.radius * self.scale))

        # text (dynamic scale เหมือนเดิม)
        dyn_font = pygame.font.Font(FONT_PATH, int(FONT_BTN.get_height() * self.scale))
        txt = dyn_font.render(self.text, False, BTN_TEXT)
        surface.blit(txt, txt.get_rect(center=r.center))

    def was_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect().collidepoint(event.pos)