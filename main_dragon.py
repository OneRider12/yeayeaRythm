import pygame, sys, json

from start.Start import run as start
from setting.Setting import run as setting
from song.song_select import run as song_select
from credits.CreditsPage import run as credit
from game.GamePage2 import run as gameplay

from config.song_dir import *

WIDTH, HEIGHT = 1200, 800
FILENAME = "assets/song_data/song.json"


def load_song_name():
    try:
        with open(FILENAME, 'r', encoding='utf-8') as file:
            data = []
            raw_data = json.load(file)
            for song_data in raw_data:
                data.append(song_data['name'])

            return data

    except FileNotFoundError:
        print(f"Error: The file '{FILENAME}' was not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: The file '{FILENAME}' contains invalid JSON syntax.")
        return None


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("YeaYea RHYTHM")

    clock = pygame.time.Clock()
    current_scene = "start"   # เริ่มที่หน้า start

    song_name = load_song_name()

    
    while True:
        dt = clock.tick(60) / 1000.0  # แปลงเป็นวินาที (ไว้ใช้ใน animation)

        # print(current_scene) # DEBUGGING
        # เลือก scene ตาม state ปัจจุบัน
        if current_scene == "start":
            next_scene = start(screen, dt)

        elif current_scene == "setting":
            next_scene = setting(screen, dt)

        elif current_scene == "song_select":
            next_scene = song_select(screen, dt)

        elif current_scene == "credit":
            next_scene = credit()

        elif current_scene == "quit":
            pygame.quit

        elif current_scene in song_name:
            # song_number = int(current_scene[-1])
            # song_json = song_dir[int(current_scene[-1]) - 1]
            next_scene = gameplay(current_scene)

        else:
            # ถ้าเจอ scene แปลก ๆ ให้ดีดกลับไป start ไปก่อน
            next_scene = "start"

        # ถ้า scene ใด return ค่ากลับมา != None
        if next_scene is not None:
            if next_scene == "quit":
                pygame.quit()
                sys.exit()

            # เปลี่ยนหน้า
            current_scene = next_scene


if __name__ == "__main__":
    main()