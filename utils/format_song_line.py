from itertools import groupby
from utils.links import take_yandex_song_link, is_yandex_link, is_link
from utils.format_string import make_song_lyrics_message
from utils.music_yandex import get_song_artist_title_by_song_id


async def formatting(lines: str):
    raw_lines = lines.split('\n')
    groups = ['\n'.join(group) for is_empty, group in groupby(raw_lines, lambda x: x == '') if not is_empty]

    lyrics = groups[0]
    artist_song = groups[1] if len(groups) > 1 else None
    link = groups[2] if len(groups) > 2 else None

    if link and is_yandex_link(link):
        _, song_id = take_yandex_song_link(link)
        song_title, artist_title = await get_song_artist_title_by_song_id(song_id)
        return make_song_lyrics_message(lines=lyrics, song=song_title, artist=artist_title, link=link)

    elif link and is_link(link):
        return make_song_lyrics_message(lines=lyrics, artist_song=artist_song, link=link)

    elif artist_song:
        return make_song_lyrics_message(lines=lyrics, artist_song=artist_song)

    else:
        return make_song_lyrics_message(lines=lyrics)
