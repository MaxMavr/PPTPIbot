from aiogram.types import Message
from aiogram import Router, F
from bot.handlers import default
from phrases import PHRASES_RU

router = Router()


@router.message(F.text.lower().in_(['спасибо', 'от души', 'благодарю']))
async def _(message: Message):
    await message.answer(text=PHRASES_RU.answers.welcome)


@router.message(F.text.lower().in_(['мяу', 'мау', 'мив', 'мав', 'ку', 'кря', 'мрр', 'пиу', 'пау', 'пум', 'квак']))
async def _(message: Message):
    await default.cmd_admin_song(message)
