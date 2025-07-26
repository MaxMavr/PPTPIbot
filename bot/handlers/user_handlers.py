from aiogram.types import Message
from aiogram import Router, F
from DB.tables.users import UsersTable
from config import config
from phrases import PHRASES_RU
from utils.format_song_line import format_song_line

router = Router()


@router.message(F.text == config.tg_bot.password)
async def _(message: Message):
    with UsersTable() as users_db:
        if users_db.set_admin(message.from_user.id, message.from_user.id):
            await message.answer(PHRASES_RU.success.promoted)
        else:
            await message.answer(PHRASES_RU.error.db)


@router.message()
async def _(message: Message):
    await message.answer(text=await format_song_line(message.text), disable_web_page_preview=True)
