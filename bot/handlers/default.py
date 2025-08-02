from aiogram import F
from aiogram.utils.chat_action import ChatActionSender

from DB.tables.users import UsersTable
from bot.chat_type_handlers import private, group
from bot.handlers.admin import command_getcmds
from aiogram.types import Message
from bot.bot_utils.routers import UserRouter, BaseRouter
from config import config, bot
from phrases import PHRASES_RU
from utils.format_string import make_song_lyrics_message
from utils.links import make_yandex_song_link
from utils.music_yandex import get_random_song_lines, get_admin_song
from bot.keyboards import inline as ikb

router = UserRouter()


@router.command('start', 'запустить бота')  # /start
async def _(message: Message):
    await message.answer(PHRASES_RU.commands.start)


@router.command('help', 'как пользоваться ботом')  # /help
async def _(message: Message):
    await message.answer(PHRASES_RU.commands.help, reply_markup=ikb.help_examples)


@router.command('about', 'о разработчиках')  # /about
async def _(message: Message):
    await message.answer(PHRASES_RU.commands.about, disable_web_page_preview=True)


@router.command(('commands', 'cmds'), 'список всех команд (это сообщение)')  # /commands /cmds
async def _(message: Message):
    commands_text = '\n'.join(str(command) for command in BaseRouter.available_commands if not command.is_admin)
    await message.answer(PHRASES_RU.title.commands + commands_text)


@router.command('admin_song', 'получить песню, которую сейчас слушает админ')  # /admin_song
async def cmd_admin_song(message: Message):
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        song, artists, song_id, album_id = await get_admin_song()
        lyrics = await get_random_song_lines(song_id)
        msg_text = make_song_lyrics_message(song=song, artist=artists,
                                            link=make_yandex_song_link(song_id, album_id), lyrics=lyrics)

        await message.answer(text=msg_text, disable_web_page_preview=True)


@router.message(F.text == config.tg_bot.password)
async def _(message: Message):
    with UsersTable() as users_db:
        if users_db.set_admin(message.from_user.id, message.from_user.id):
            await message.delete()
            await message.answer(PHRASES_RU.success.promoted)
            await command_getcmds(message)
        else:
            await message.answer(PHRASES_RU.error.db)


@router.message()
async def _(message: Message):
    if message.chat.type == 'private':
        await private.handler(message)
        return

    if message.chat.type in ['group', 'supergroup']:
        await group.handler(message)
        return
