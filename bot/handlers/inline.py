import hashlib

from aiogram import Router, types
from aiogram.types import InlineQueryResultArticle, InputTextMessageContent
from utils.format_song_line import format_song_line
from phrases import PHRASES_RU
from utils.format_string import make_song_lyrics_message
from utils.links import make_yandex_song_link
from utils.music_yandex import get_admin_song

router = Router()


@router.inline_query()
async def inline_get_photo(query: types.InlineQuery):
    text = query.query.strip()

    if not text:
        return await query.answer([], cache_time=1, is_personal=True)

    if text.strip() in ['as', '/', '@']:
        song, artists, song_id = await get_admin_song()
        title = song
        description = artists
        text = make_song_lyrics_message(song=song, artist=artists, link=make_yandex_song_link(song_id))
    else:
        title = PHRASES_RU.title.inline
        description = PHRASES_RU.footnote.inline
        text = await format_song_line(text)

    result = InlineQueryResultArticle(
        id=hashlib.md5(text.encode()).hexdigest(),
        title=title,
        description=description,
        input_message_content=InputTextMessageContent(
            message_text=text,
            disable_web_page_preview=True
        )
    )

    await query.answer([result], cache_time=1, is_personal=True)
