import re
from typing import Tuple

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


def clean_typography(text: str):
    space_sub = (r'[^\S\r\n]+', ' ')

    word_subs = (
        (r'\bбог\b', 'Бог'),
        (r'\bгосподь\b', 'Господь'),
        (r'\bхристос\b', 'Христос'),
        (r'\bиисус\b', 'Иисус'),
        (r'\bаллах\b', 'Аллах'),
        (r'\bмосква\b', 'Москва'),
        (r'\bсанкт[- ]петербург\b', 'Санкт-Петербург'),
        (r'\bпетербург\b', 'Петербург'),
        (r'\bпитер\b', 'Питер'),
        (r'\bроссия\b', 'Россия'),
    )

    typo_subs = (
        (r' - ', ' — '),
        (r' – ', ' — '),
        (r'\.\.\.', '…'),
        (r'\.\.', '…'),
        (r' \.', '.'),
        (r' ,', ','),
        (r' ;', ';'),
        (r' :', ':'),
        (r' \?', '?'),
        (r' !', '!'),
    )

    quote_subs = (
        (r'„\s', '„'),
        (r'\s“', '“'),
        (r'\s»', '»'),
        (r'«\s', '«'),
        (r'(\w)„', r'\1 „'),
        (r'“(\w)', r'“ \1'),
        (r'»(\w)', r'» \1'),
        (r'(\w)«', r'\1 «'),
    )

    pattern, repl = space_sub
    text = re.sub(pattern, repl, text, flags=re.IGNORECASE)

    for pattern, repl in word_subs:
        text = re.sub(pattern, repl, text, flags=re.IGNORECASE)

    for pattern, repl in typo_subs:
        text = re.sub(pattern, repl, text)

    for pattern, repl in quote_subs:
        text = re.sub(pattern, repl, text)

    return text


def clean_quotes(text: str) -> str:
    quote_pairs = [
        ('„', '“'),
        ('«', '»'),
    ]

    for q in ['«', '»', '„', '“', '”', '‟', '❝', '❞', '＂', "'"]:
        text = text.replace(q, '"')

    result = []
    depth = 0

    for i, ch in enumerate(text):
        if ch == '"':
            prev_char = text[i-1] if i > 0 else ' '
            next_char = text[i+1] if i < len(text)-1 else ' '

            if prev_char.isspace() or prev_char in ('',):
                open_q, _ = quote_pairs[depth % 2]
                result.append(open_q)
                depth += 1
            elif next_char.isspace() or next_char in ('',):
                depth -= 1
                _, close_q = quote_pairs[depth % 2]
                result.append(close_q)
            else:
                if depth % 2 == 0:
                    open_q, _ = quote_pairs[depth % 2]
                    result.append(open_q)
                    depth += 1
                else:
                    depth -= 1
                    _, close_q = quote_pairs[depth % 2]
                    result.append(close_q)
        else:
            result.append(ch)

    while depth > 0:
        depth -= 1
        _, close_q = quote_pairs[depth % 2]
        result.append(close_q)

    return ''.join(result)


def make_song_lyrics_message(lyrics: str = None,
                             artist_song: str = None,
                             song: str = None,
                             artist: str = None,
                             link: str = None,
                             caption: str = None,
                             artist_song_seps: Tuple[str, ...] = (' : ',)
                             ) -> str:
    message_parts = []

    if lyrics:
        lyrics = clear_string(lyrics)
        lyrics = clean_quotes(lyrics)
        lyrics = clean_typography(lyrics)
        lyrics = lyrics.strip()

        message_parts.append(f'<i>«{lyrics}»</i>\n\n')

    name_part = ''
    if artist_song:
        for sep in artist_song_seps:
            parts = artist_song.split(sep)
            if len(parts) >= 2:
                parts = [p.strip() for p in parts]
                artist = parts[0]
                song = ' '.join(parts[1:])
                name_part = f'{artist.strip()} — {song.strip()}'
                break
        else:
            name_part = artist_song.strip()

    elif artist and song:
        name_part = f'{artist.strip()} — {song.strip()}'
    elif artist:
        name_part = artist.strip()
    elif song:
        name_part = song.strip()

    if name_part and link:
        message_parts.append(f'<a href="{link}">{clear_string(name_part).strip()}</a>')

    if caption:
        message_parts.append(f'\n\n{clear_string(caption).strip()}')

    return ''.join(message_parts)


if __name__ == "__main__":
    tests = [
        '«Привет«',  # простой случай
        '\'Привет\', \'Привет\'',  # простой случай
        'Привет',  # простой случай
        '"Один \'два\' конец"',  # два уровня
        '"А "Б \'В\' Г" Д"',  # три уровня
        '"Уровень1 "Уровень2 "Уровень3 "Уровень4" конец3" конец2" конец1"',  # четыре уровня
        '"1 "2 "3 "4 "5" конец4" конец3" конец2" конец1"',  # пять уровней
        '"start "lvl2 "lvl3 "lvl4 "lvl5 "lvl6" end5" end4" end3" end2" end1"',  # шесть уровней
        "'Один 'два \"три 'четыре'\" конец два' конец один'",  # кавычки вперемешку (одинарные + двойные)
        '"Начало "середина "ещё глубже"',  # незакрытые кавычки (алгоритм должен аккуратно закрыть сам)
        '""""""""',  # куча подряд
        'Привер',  # куча подряд
        'Скинул ей двух котиков, она сказала: "Это мы"',  # куча подряд
        'На радио будут крутить мои речи „Есть идеи Маркса, остальное — не вечно“',  # куча подряд
    ]

    for n, t in enumerate(tests, 1):
        print(f"\n"
              f"Test {n}\n"
              f"input : {t}\n"
              f"output: {clean_quotes(t)}")
