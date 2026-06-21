from aiogram import Bot
from aiogram.types import Message
from aiogram.utils.chat_action import ChatActionSender

from bot.bot_utils.filters import EditFilter
from bot.keyboards import inline as ikb
from phrases import PHRASES_RU
from utils.format_song_line import format_song_line


async def handler(message: Message, bot: Bot):
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        if message.pinned_message:
            return

        if not message.text:
            await message.answer(text=PHRASES_RU.answers.unknown)
            return

        msg_text = await format_song_line(message.text)

        if not msg_text:
            await message.answer(text=PHRASES_RU.error.processing_failed)
            return

        if await EditFilter.check(bot, message.from_user.id):
            await message.answer(
                text=msg_text,
                disable_web_page_preview=True,
                reply_markup=ikb.publish_post(message.from_user.id),
            )
        else:
            await message.answer(
                text=msg_text,
                disable_web_page_preview=True,
                reply_markup=ikb.suggest_post(message.from_user.id, message.message_id),
            )
