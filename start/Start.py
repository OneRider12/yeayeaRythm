import pygame, sys, random

def run(screen, dt):
    WIDTH, HEIGHT = 1200, 800
    FONT_PATH = "assets/fonts/PixelifySans-VariableFont_wght.ttf"

    if not hasattr(run, "_inited"):
        run._inited = True

        # ----- Fonts -----
        try:
            run.FONT_TITLE = pygame.font.Font(FONT_PATH, 92)
            run.FONT_SUB   = pygame.font.Font(FONT_PATH, 34)
            run.FONT_BTN   = pygame.font.Font(FONT_PATH, 44)
        except:
            run.FONT_TITLE = pygame.font.SysFont("Consolas", 92, bold=True)
            run.FONT_SUB   = pygame.font.SysFont("Consolas", 34)
            run.FONT_BTN   = pygame.font.SysFont("Consolas", 54, bold=True)

        # ----- Colors -----
        run.BG_COLOR        = (27, 48, 91)
        run.BTN_FILL        = (240, 240, 240)
        run.BTN_FILL_HOVER  = (255, 255, 255)
        run.BTN_TEXT        = (27, 48, 91)
        run.WHITE           = (255, 255, 255)

        # ----- Classes -----
        class Button:
            def __init__(self, text, center, size=(400, 80), radius=40):
                self.text = text
                self.center = pygame.Vector2(center)
                self.base_w, self.base_h = size
                self.radius = radius
                self.scale = 1.0
                self.target_scale = 1.0
                self.shadow_alpha = 90
                self.elev = 6

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
                r = self.rect()
                # shadow
                sh = pygame.Surface((r.width, r.height), pygame.SRCALPHA)
                pygame.draw.rect(
                    sh,
                    (0, 0, 0, int(self.shadow_alpha * (0.9 if self.target_scale > 1 else 0.6))),
                    sh.get_rect(),
                    border_radius=int(self.radius * self.scale)
                )
                surface.blit(sh, (r.x, r.y + self.elev))
                # body
                fill = run.BTN_FILL_HOVER if self.target_scale > 1 else run.BTN_FILL
                pygame.draw.rect(surface, fill, r, border_radius=int(self.radius * self.scale))
                # text (ใช้สเกลเดียวกับหน้า setting)
                dyn = pygame.font.Font(FONT_PATH, int(run.FONT_BTN.get_height() * self.scale))
                txt = dyn.render(self.text, False, run.BTN_TEXT)
                surface.blit(txt, txt.get_rect(center=r.center))

            def was_clicked(self, event):
                return event.type == pygame.MOUSEBUTTONDOWN and self.rect().collidepoint(event.pos)

        run.Button = Button

        # ----- Create UI once -----
        run.buttons = [
            Button("PLAY",        (WIDTH//2, 300)),
            Button("LEADERBOARD", (WIDTH//2, 420)),
            Button("SETTING",     (WIDTH//2, 540)),
            Button("CREDIT",      (WIDTH//2, 660)),
        ]

    # ----- Events -----
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return "quit"
        for b in run.buttons:
            if b.was_clicked(event):
                if b.text == "SETTING":
                    return "setting"
                elif b.text == "PLAY":
                    return "play"
                elif b.text == "LEADERBOARD":
                    return "leaderboard"
                elif b.text == "CREDIT":
                    return "credit"

    # ----- Update -----
    mouse = pygame.mouse.get_pos()
    for b in run.buttons:
        b.update(mouse, dt)

    # ----- Draw -----
    screen.fill(run.BG_COLOR)
    title = run.FONT_TITLE.render("YeaYea RHYTHM", False, run.WHITE)
    sub   = run.FONT_SUB.render("By whatever", False, run.WHITE)
    screen.blit(title, title.get_rect(center=(WIDTH//2, 120)))
    screen.blit(sub,   sub.get_rect(center=(WIDTH//2, 190)))

    for b in run.buttons:
        b.draw(screen)

    pygame.display.flip()
    return None
