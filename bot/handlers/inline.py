import hashlib

from aiogram import Router, types
from aiogram.types import InlineQueryResultArticle, InputTextMessageContent
from utils.format_song_line import format_song_line
from phrases import PHRASES_RU

router = Router()


@router.inline_query()
async def inline_get_photo(query: types.InlineQuery):
    text = query.query.strip()

    if not text:
        return await query.answer([], cache_time=1, is_personal=True)

    message_text = await format_song_line(text)

    result = InlineQueryResultArticle(
        id=hashlib.md5(text.encode()).hexdigest(),
        title=PHRASES_RU.title.inline,
        description=PHRASES_RU.footnote.inline,
        input_message_content=InputTextMessageContent(
            message_text=message_text,
            disable_web_page_preview=True
        )
    )

    await query.answer([result], cache_time=1, is_personal=True)
