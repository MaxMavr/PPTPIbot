import json
from os.path import dirname, getsize, isfile

SONG_FILE = f'{dirname(__file__)}/songs.json'
_EMPTY_SONG = (' ', ' ', ' ')


def __is_file_exist(path2file: str) -> bool:
    return isfile(path2file) and getsize(path2file) != 0


def __make_json(content: dict) -> None:
    with open(SONG_FILE, 'w', encoding='utf-8') as file:
        json.dump(content, file, ensure_ascii=False, indent=2)


def __read_json() -> dict:
    with open(SONG_FILE, encoding='utf-8') as file:
        return json.load(file)


def __get_songs() -> dict:
    if not __is_file_exist(SONG_FILE):
        data = {'admin_song': list(_EMPTY_SONG), 'mood_song': list(_EMPTY_SONG)}
        __make_json(data)
        return data
    return __read_json()


def read_admin_song() -> tuple[str, str, str]:
    data = __get_songs()
    return tuple(data.get('admin_song', list(_EMPTY_SONG)))


def upd_admin_song(admin_song: tuple[str, str, str]) -> None:
    data = __get_songs()
    data['admin_song'] = list(admin_song)
    __make_json(data)


def read_mood_song() -> tuple[str, str, str]:
    data = __get_songs()
    return tuple(data.get('mood_song', list(_EMPTY_SONG)))


def upd_mood_song(mood_song: tuple[str, str, str]) -> None:
    data = __get_songs()
    data['mood_song'] = list(mood_song)
    __make_json(data)
