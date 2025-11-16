import pygame, sys, json

from start.Start import run as start
from setting.Setting import run as setting
from song.song_select import run as song_select
from credits.CreditsPage import run as credit
from game.GamePage2 import run as gameplay

from config.song_dir import *

WIDTH, HEIGHT = 1200, 800
SONG_DATA_DIR = "assets/song_data/song.json"

def load_data(filename):
    try:
        # Use 'with open' to open the file for reading ('r')
        with open(filename, 'r', encoding='utf-8') as file:
            # The json.load() function reads the file content,
            # parses the JSON structure, and returns a Python dictionary/list.
            data = json.load(file)
            print(data)
            return data

    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: The file '{filename}' contains invalid JSON syntax.")
        return None


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("YeaYea RHYTHM")

    clock = pygame.time.Clock()
    current_scene = "start"   # เริ่มที่หน้า start

    song_dir = (SONG01_JSON_DIR,
                SONG02_JSON_DIR,
                SONG03_JSON_DIR,
                SONG04_JSON_DIR,
                SONG05_JSON_DIR)

    song_data = load_data(SONG_DATA_DIR)

    
    while True:
        dt = clock.tick(60) / 1000.0  # แปลงเป็นวินาที (ไว้ใช้ใน animation)

        # print(current_scene)
        # เลือก scene ตาม state ปัจจุบัน
        if current_scene == "start":
            next_scene = start(screen, dt)

        elif current_scene == "setting":
            next_scene = setting(screen, dt)

        elif current_scene == "song_select":
            next_scene = song_select(screen, dt)

        elif current_scene == "credit":
            next_scene = credit()

        elif "song0" in current_scene:
            song_number = int(current_scene[-1])
            song_json = song_dir[int(current_scene[-1]) - 1]
            next_scene = gameplay(song_json)

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