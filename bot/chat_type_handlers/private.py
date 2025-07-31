from aiogram.types import Message
from bot.bot_utils.filters import EditFilter
from phrases import PHRASES_RU
from utils.format_song_line import format_song_line
from bot.keyboards import inline as ikb


async def handler(message: Message):
    if message.text:
        if await EditFilter.check(message.from_user.id):
            await message.answer(text=await format_song_line(message.text),
                                 disable_web_page_preview=True,
                                 reply_markup=ikb.publish_post)
        else:
            await message.answer(text=await format_song_line(message.text),
                                 disable_web_page_preview=True,
                                 reply_markup=ikb.suggest_post(message.from_user.id, message.message_id))
        return
    await message.answer(text=PHRASES_RU.answers.unknown)
