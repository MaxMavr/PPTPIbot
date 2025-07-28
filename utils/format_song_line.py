from itertools import groupby
from utils.links import take_yandex_song_link, is_yandex_link, is_link
from utils.format_string import make_song_lyrics_message
from utils.music_yandex import get_song_artist_title_by_song_id


async def format_song_line(lines: str):
    groups = ['\n'.join(group) for key, group in groupby(lines.split('\n'), lambda x: x == '') if not key]

    if len(groups) >= 3:
        if is_yandex_link(groups[2]):
            _, song_id = take_yandex_song_link(groups[2])
            song_title, artist_title = await get_song_artist_title_by_song_id(song_id)
            msg_text = make_song_lyrics_message(lines=groups[0],
                                                song=song_title,
                                                artist=artist_title,
                                                link=groups[2])

        elif is_link(groups[2]):
            msg_text = make_song_lyrics_message(lines=groups[0],
                                                artist_song=groups[1],
                                                link=groups[2])
        else:
            msg_text = make_song_lyrics_message(lines=groups[0],
                                                artist_song=groups[1])

    elif len(groups) == 2:
        if is_yandex_link(groups[1]):
            _, song_id = take_yandex_song_link(groups[1])
            song_title, artist_title = await get_song_artist_title_by_song_id(song_id)
            msg_text = make_song_lyrics_message(lines=groups[0],
                                                song=song_title,
                                                artist=artist_title,
                                                link=groups[1])
        else:
            msg_text = make_song_lyrics_message(lines=groups[0],
                                                artist_song=groups[1])

    else:
        msg_text = make_song_lyrics_message(lines=groups[0])

    return msg_text
