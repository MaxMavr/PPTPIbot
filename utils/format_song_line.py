from typing import Tuple

from utils.links import parse_yandex_music_link, is_yandex_link, is_link
from utils.format_string import make_song_lyrics_message
from utils.music_yandex import get_song_artist_title_by_song_id


async def format_song_line(lines: str, artist_song_seps: Tuple[str, ...] = (' : ',)) -> str:
    lyrics_parts = []
    artist_song = None
    song = None
    artist = None
    link = None

    clear_lines = [l.strip() for l in lines.split('\n') if l.strip()]
    clear_not_link_lines = []

    for line in clear_lines:
        if is_link(line):
            link = line
            if is_yandex_link(link):
                song_id = parse_yandex_music_link(link)
                song, artist = await get_song_artist_title_by_song_id(song_id)
        else:
            clear_not_link_lines.append(line)

    for line in clear_not_link_lines:
        if not artist_song and not (song and artist):
            for sep in artist_song_seps:
                if sep in line:
                    artist_song = line
                    break
            else:
                lyrics_parts.append(line)
        else:
            lyrics_parts.append(line)

    lyrics = '\n'.join(lyrics_parts) if lyrics_parts else None

    if not lyrics:
        lyrics = artist_song
        artist_song = None

    return make_song_lyrics_message(lyrics=lyrics,
                                    artist_song=artist_song,
                                    song=song,
                                    artist=artist,
                                    link=link,
                                    artist_song_seps=artist_song_seps)
