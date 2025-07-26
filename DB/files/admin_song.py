from typing import Union, Tuple
from os.path import isfile, getsize, dirname
import json

DAY_SONG_FILE = f'{dirname(__file__)}/admin_song.json'


def __is_file_exist(path2file: str) -> bool:
    if isfile(path2file):
        return getsize(path2file) != 0
    return False


def __make_json(path2file: str, content: Union[list, dict]):
    with open(path2file, 'w', encoding="utf-8") as file:
        json.dump(content, file, ensure_ascii=False)


def __read_json(path2file: str) -> Union[list, dict]:
    with open(path2file, 'r', encoding='utf-8') as file:
        return json.load(file)


def read_admin_song() -> Tuple[str, str, str, str]:
    if not __is_file_exist(DAY_SONG_FILE):
        return ' ', ' ', ' ', ' '
    return tuple(__read_json(DAY_SONG_FILE))


def upd_admin_song(day_song: list):
    __make_json(DAY_SONG_FILE, day_song)
