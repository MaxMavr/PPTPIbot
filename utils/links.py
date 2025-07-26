import re

YANDEX_LINK_PATTERN = r'https://music\.yandex\.ru/album/\d+/track/\d+'
YANDEX_SONG_ID_PATTERN = r'https://music\.yandex\.ru/album/(\d+)/track/(\d+)'
LINK_PATTERN = r'https://'


def take_yandex_song_link(link: str) -> (str, str):
    return re.search(YANDEX_SONG_ID_PATTERN, link).groups()


def make_yandex_song_link(song_id: str, album_id: str) -> str:
    return f'https://music.yandex.ru/album/{album_id}/track/{song_id}'


def is_yandex_link(link: str) -> bool:
    return bool(re.search(YANDEX_LINK_PATTERN, link))


def is_link(link: str) -> bool:
    return link.startswith(LINK_PATTERN)
