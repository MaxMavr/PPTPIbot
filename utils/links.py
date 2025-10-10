import re

YANDEX_LINK_PATTERN = (
    r"(?:https://music\.yandex\.ru/album/(\d+)/track/(\d+))"
    r"|(?:https://music\.yandex\.ru/track/(\d+))"
)
LINK_PATTERN = r'https://'


def parse_yandex_music_link(link: str) -> str:
    m = re.search(YANDEX_LINK_PATTERN, link)
    if m.group(1) and m.group(2):
        return m.group(2)
    else:
        return m.group(3)


def make_yandex_song_link(song_id: str) -> str:
    return f'https://music.yandex.ru/track/{song_id}'


def is_yandex_link(link: str) -> bool:
    return bool(re.search(YANDEX_LINK_PATTERN, link))


def is_link(link: str) -> bool:
    return link.startswith(LINK_PATTERN)
