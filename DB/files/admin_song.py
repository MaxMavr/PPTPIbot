from typing import Union, Tuple
from os.path import isfile, getsize, dirname
import json

SONG_FILE = f'{dirname(__file__)}/songs.json'


def __is_file_exist(path2file: str) -> bool:
    return isfile(path2file) and getsize(path2file) != 0


def __make_json(content: dict):
    with open(SONG_FILE, 'w', encoding='utf-8') as file:
        json.dump(content, file, ensure_ascii=False, indent=2)


def __read_json() -> dict:
    with open(SONG_FILE, 'r', encoding='utf-8') as file:
        return json.load(file)


def __get_songs() -> dict:
    if not __is_file_exist(SONG_FILE):
        data = {"admin_song": [' ', ' ', ' '], "mood_song": [' ', ' ', ' ']}
        __make_json(data)
        return data
    return __read_json()


def read_admin_song() -> Tuple[str, str, str]:
    data = __get_songs()
    return tuple(data.get("admin_song", [' ', ' ', ' ']))


def upd_admin_song(admin_song: Tuple[str, str, str]):
    data = __get_songs()
    data["admin_song"] = list(admin_song)
    __make_json(data)


def read_mood_song() -> Tuple[str, str, str]:
    data = __get_songs()
    return tuple(data.get("mood_song", [' ', ' ', ' ']))


def upd_mood_song(mood_song: Tuple[str, str, str]):
    data = __get_songs()
    data["mood_song"] = list(mood_song)
    __make_json(data)
