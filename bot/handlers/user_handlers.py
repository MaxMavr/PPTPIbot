from aiogram.types import Message
from aiogram import Router, F
from DB.tables.users import UsersTable
from bot.filters import EditFilter
from config import config
from phrases import PHRASES_RU
from utils.format_song_line import format_song_line
from bot.keyboards import inline_keyboards as ikb

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
