import pygame, sys
import Start
import Setting

pygame.init()
WIDTH, HEIGHT = 1324, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("YeaYea RHYTHM")

clock = pygame.time.Clock()
current_scene = "start"   # เริ่มต้นที่หน้า start

# -------- Main loop --------
while True:
    dt = clock.tick(60) / 1000.0

    if current_scene == "start":
        next_scene = Start.run(screen, dt)
        if next_scene:
            current_scene = next_scene

    elif current_scene == "setting":
        next_scene = Setting.run(screen, dt)
        if next_scene:
            current_scene = next_scene

    # ปิดเกม
    if current_scene == "quit":
        pygame.quit()
        sys.exit()

