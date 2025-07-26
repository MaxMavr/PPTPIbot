from aiogram.types import Message
from aiogram import Router, F
from bot.handlers.commands import cmd_admin_song
from phrases import PHRASES_RU

router = Router()


@router.message(F.text.lower().in_(['спасибо', 'от души', 'благодарю']))
async def _(message: Message):
    await message.answer(text=PHRASES_RU.answers.welcome)


@router.message(F.text.lower().in_(['мяу', 'мау', 'мив', 'мав']))
async def _(message: Message):
    await cmd_admin_song(message)
