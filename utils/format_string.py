from phrases import PHRASES_RU


def clear_string(text: str):
    if not text:
        return PHRASES_RU.error.not_text
    return text.replace('<', '&lt;').replace('>', '&gt;').replace('&', '&amp;')


def get_query_count_emoji(count: int) -> str:
    for emoji, threshold in PHRASES_RU.icon.query.thresholds.__dict__.items():
        if count > threshold:
            return emoji
    return PHRASES_RU.icon.query.default


def make_song_lyrics_message(lines: str,
                             artist_song: str = None, song: str = None, artist: str = None,
                             link: str = None
                             ) -> str:
    message_parts = []

    if lines:
        message_parts.append(f'<i>«{clear_string(lines)}»</i>\n\n')

    name_part = ''
    if artist_song:
        for sep in [' - ', ' – ', ' — ', ' : ']:
            parts = artist_song.split(sep)
            if len(parts) == 2:
                artist, song = parts
                name_part = f'{artist} — {song}'
                break
        else:
            name_part = artist_song

    elif artist and song:
        name_part = f'{artist} — {song}'
    elif artist:
        name_part = artist
    elif song:
        name_part = song

    if link and name_part:
        message_parts.append(f'<a href="{link}">{clear_string(name_part)}</a>')

    return ''.join(message_parts)
