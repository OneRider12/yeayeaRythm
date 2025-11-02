import pygame, sys, random

def run(screen, dt):
    WIDTH, HEIGHT = 1324, 768
    FONT_PATH = "PixelifySans-VariableFont_wght.ttf"

    #font
    def load_fonts():
        try:
            return (
                pygame.font.Font(FONT_PATH, 96),
                pygame.font.Font(FONT_PATH, 44),
                pygame.font.Font(FONT_PATH, 44),
            )
        except:
            return (
                pygame.font.SysFont("Consolas", 96, bold=True),
                pygame.font.SysFont("Consolas", 44),
                pygame.font.SysFont("Consolas", 56, bold=True),
            )
    FONT_TITLE, FONT_SUB, FONT_BTN = load_fonts()

    #color
    BG_COLOR = (27, 48, 91)
    BTN_FILL = (240, 240, 240)
    BTN_FILL_HOVER = (255, 255, 255)
    BTN_TEXT = (27, 48, 91)

    def draw_text_center(txt, font, color, y):
        surf = font.render(txt, True, color)
        rect = surf.get_rect(center=(WIDTH//2, y))
        screen.blit(surf, rect)

    #classes
    class Button:
        def __init__(self, text, center, size=(420, 92), radius=40):
            self.text = text
            self.center = pygame.Vector2(center)
            self.base_w, self.base_h = size
            self.radius = radius
            self.scale = 1.0
            self.target_scale = 1.0
            self.elev = 6
            self.shadow_alpha = 110

        def rect(self):
            w = int(self.base_w * self.scale)
            h = int(self.base_h * self.scale)
            r = pygame.Rect(0, 0, w, h)
            r.center = self.center
            return r

        def update(self, mouse_pos, dt):
            if self.rect().collidepoint(mouse_pos):
                self.target_scale = 1.08
            else:
                self.target_scale = 1.0
            self.scale += (self.target_scale - self.scale) * min(1.0, 10.0 * dt)

        def draw(self, surface):
            r = self.rect()
            shadow = pygame.Surface((r.width, r.height), pygame.SRCALPHA)
            pygame.draw.rect(shadow, (0,0,0,int(self.shadow_alpha*(0.9 if self.target_scale>1 else 0.6))),
                             shadow.get_rect(), border_radius=int(self.radius*self.scale))
            surface.blit(shadow, (r.x, r.y+self.elev))
            fill = BTN_FILL_HOVER if self.target_scale>1 else BTN_FILL
            pygame.draw.rect(surface, fill, r, border_radius=int(self.radius*self.scale))
            dynamic_font = pygame.font.Font(FONT_PATH, int(FONT_BTN.get_height()*self.scale))
            text = dynamic_font.render(self.text, True, BTN_TEXT)
            screen.blit(text, text.get_rect(center=r.center))

        def was_clicked(self, event):
            return event.type == pygame.MOUSEBUTTONDOWN and self.rect().collidepoint(event.pos)

    buttons = [
        Button("PLAY", (WIDTH//2, 300)),
        Button("LEADERBOARD", (WIDTH//2, 420)),
        Button("SETTING", (WIDTH//2, 540)),
        Button("CREDIT", (WIDTH//2, 660)),
    ]
    # เชื่อมไปหน้าต่างๆ
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return "quit"
        for b in buttons:
            if b.was_clicked(event):
                if b.text == "SETTING":
                    return "setting"
                #เชื่อมไปหน้าอื่นเพิ่มได้

    mouse = pygame.mouse.get_pos()
    for b in buttons:
        b.update(mouse, dt)

    screen.fill(BG_COLOR)
    draw_text_center("YeaYea RHYTHM", FONT_TITLE, (255,255,255), 120)
    draw_text_center("By whatever", FONT_SUB, (255,255,255), 190)
    for b in buttons: b.draw(screen)

    pygame.display.flip()
    return None
