import pygame
import sys
from leaderboard.LeaderPage import LeaderPage
def main():
    # เริ่มต้น pygame
    pygame.init()

    # สร้างหน้า Leaderboard
    page = LeaderPage()
    page.run()  # เรียก loop หลักของหน้า

    # ออกจากโปรแกรม
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
