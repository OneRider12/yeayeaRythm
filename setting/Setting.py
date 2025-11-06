import pygame, sys

def run(screen, dt):
    WIDTH, HEIGHT = 1324, 768
    FONT_PATH = "assets/fonts/PixelifySans-VariableFont_wght.ttf"

    if not hasattr(run, "_inited"):
        run._inited = True

        # Fonts 
        try:
            run.FONT_TITLE = pygame.font.Font(FONT_PATH, 92)
            run.FONT_LABEL = pygame.font.Font(FONT_PATH, 34)
            run.FONT_BTN   = pygame.font.Font(FONT_PATH, 54)
        except:
            run.FONT_TITLE = pygame.font.SysFont("Consolas", 92, bold=True)
            run.FONT_LABEL = pygame.font.SysFont("Consolas", 34)
            run.FONT_BTN   = pygame.font.SysFont("Consolas", 54, bold=True)

        # Colors
        run.BG_COLOR       = (27, 48, 91)
        run.BTN_FILL       = (240, 240, 240)
        run.BTN_FILL_HOVER = (255, 255, 255)
        run.BTN_TEXT       = (27, 48, 91)
        run.WHITE          = (255, 255, 255)
        run.SW_TRACK_OFF   = (0, 0, 0)
        run.SW_TRACK_ON    = (34, 72, 122)
        run.SW_KNOB        = (235, 235, 235)

        # ---- classes ----
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
                sh = pygame.Surface((r.width, r.height), pygame.SRCALPHA)
                pygame.draw.rect(sh, (0,0,0,int(self.shadow_alpha*(0.9 if self.target_scale>1 else 0.6))),
                                 sh.get_rect(), border_radius=int(self.radius*self.scale))
                surface.blit(sh, (r.x, r.y + self.elev))
                fill = run.BTN_FILL_HOVER if self.target_scale>1 else run.BTN_FILL
                pygame.draw.rect(surface, fill, r, border_radius=int(self.radius*self.scale))
                dyn = pygame.font.Font(FONT_PATH, int(run.FONT_BTN.get_height()*self.scale))
                txt = dyn.render(self.text, False, run.BTN_TEXT)
                surface.blit(txt, txt.get_rect(center=r.center))

            def was_clicked(self, event):
                return event.type == pygame.MOUSEBUTTONDOWN and self.rect().collidepoint(event.pos)

        class ToggleSwitch:
            def __init__(self, right_center, track_size=(160, 56), radius=28, value=False):
                self.center = pygame.Vector2(right_center)
                self.tw, self.th = track_size
                self.radius = radius
                self.value = value
                self.anim = 1.0 if value else 0.0
                self.target = self.anim

            def rect(self):
                r = pygame.Rect(0, 0, self.tw, self.th)
                r.center = (int(self.center.x), int(self.center.y))
                return r

            def update(self, _mouse_pos, dt):
                self.anim += (self.target - self.anim) * min(1.0, 12.0 * dt)

            def draw(self, surface):
                r = self.rect()
                col = (
                    int(run.SW_TRACK_OFF[0]*(1-self.anim) + run.SW_TRACK_ON[0]*self.anim),
                    int(run.SW_TRACK_OFF[1]*(1-self.anim) + run.SW_TRACK_ON[1]*self.anim),
                    int(run.SW_TRACK_OFF[2]*(1-self.anim) + run.SW_TRACK_ON[2]*self.anim),
                )
                pygame.draw.rect(surface, col, r, border_radius=self.radius)
                pad = 6
                knob_r = self.th - pad*2
                knob_min_x = r.x + pad
                knob_max_x = r.right - pad - knob_r
                knob_x = int(knob_min_x + (knob_max_x - knob_min_x) * self.anim)
                pygame.draw.ellipse(surface, run.SW_KNOB,
                                    pygame.Rect(knob_x, r.y+pad, knob_r, knob_r))

            def handle_event(self, event):
                if event.type == pygame.MOUSEBUTTONDOWN and self.rect().collidepoint(event.pos):
                    self.value = not self.value
                    self.target = 1.0 if self.value else 0.0

        class SettingRow:
            def __init__(self, label, y, switch_default=False):
                self.label = label
                self.box_rect = pygame.Rect(WIDTH//2 - 420, y-36, 840, 72)
                self.switch = ToggleSwitch((self.box_rect.right - 90, y), value=switch_default)

            def update(self, mouse_pos, dt):
                self.switch.update(mouse_pos, dt)

            def draw(self, surface):
                pygame.draw.rect(surface, run.BTN_FILL, self.box_rect, border_radius=36)
                text = run.FONT_LABEL.render(self.label, False, run.BTN_TEXT)
                surface.blit(text, (self.box_rect.x + 32, self.box_rect.centery - text.get_height()//2))
                self.switch.draw(surface)

            def handle_event(self, event):
                self.switch.handle_event(event)

        # keep classes
        run.Button = Button
        run.SettingRow = SettingRow

        # create once
        run.rows = [
            SettingRow("MV Background", y=250, switch_default=True),
            SettingRow("VFX",           y=340, switch_default=True),
        ]
        run.buttons = [
            Button("SONG", (WIDTH//2, 500)),
            Button("PLAY", (WIDTH//2, 600)),
            Button("HOME", (WIDTH//2, 700)),
        ]

    # เชื่อมไปหน้าต่างๆ
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return "quit"
        for row in run.rows:
            row.handle_event(event)
        for b in run.buttons:
            if b.was_clicked(event):
                if b.text == "HOME":
                    return "start"
                # เพิ่มหน้าในปุ่มอื่นๆ

    mouse = pygame.mouse.get_pos()
    for row in run.rows:
        row.update(mouse, dt)
    for b in run.buttons:
        b.update(mouse, dt)

    screen.fill(run.BG_COLOR)
    # title
    title = run.FONT_TITLE.render("SETTING", False, run.WHITE)
    screen.blit(title, title.get_rect(center=(WIDTH//2, 120)))

    for row in run.rows:
        row.draw(screen)
    for b in run.buttons:
        b.draw(screen)

    pygame.display.flip()
    return None

