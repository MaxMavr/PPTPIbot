from aiogram import Bot, Router
from aiogram.types import Message
from aiogram.utils.chat_action import ChatActionSender

from bot.bot_utils.routers import BaseRouter, UserRouter
from bot.chat_type_handlers import group, private
from bot.filters.password import PasswordFilter
from bot.handlers.admin import command_getcmds
from bot.keyboards import inline as ikb
from db.files.admin_song import read_mood_song
from db.repositories.users import UsersRepository
from phrases import PHRASES_RU
from utils.format_string import make_song_lyrics_message
from utils.links import make_yandex_song_link
from utils.music_yandex import get_admin_song, get_random_song_lines

router = UserRouter()


@router.command('start', 'запустить бота')  # /start
async def _(message: Message):
    await message.answer(PHRASES_RU.commands.start)


@router.command(('help', 'h'), 'как пользоваться ботом')  # /help
async def _(message: Message):
    await message.answer(PHRASES_RU.commands.help, reply_markup=ikb.help_examples, disable_web_page_preview=True)


@router.command(('about', 'a'), 'о разработчиках')  # /about
async def _(message: Message):
    await message.answer_photo(
        caption=PHRASES_RU.commands.about,
        photo='https://yan-toples.ru/Phasalo/color-black-phasalo-project-margin.png',
        disable_web_page_preview=True,
    )


@router.command(('commands', 'cmds'), 'список всех команд (это сообщение)')  # /commands /cmds
async def _(message: Message):
    commands_text = '\n'.join(str(command) for command in BaseRouter.available_commands if not command.is_admin)
    await message.answer(PHRASES_RU.title.commands + commands_text)


@router.command(('admin_song', 'as'), 'получить песню, которую сейчас слушает админ')  # /admin_song
async def cmd_admin_song(message: Message, bot: Bot):
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        song, artists, song_id = await get_admin_song()
        lyrics = await get_random_song_lines(song_id)
        msg_text = make_song_lyrics_message(
            song=song, artist=artists, link=make_yandex_song_link(song_id), lyrics=lyrics
        )

        await message.answer(text=msg_text, disable_web_page_preview=True)


@router.command(('mood_song', 'ms'), 'получить песню, настроения дня')  # /mood_song
async def cmd_mood_song(message: Message, bot: Bot):
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        song, artists, song_id = read_mood_song()
        lyrics = await get_random_song_lines(song_id)
        msg_text = make_song_lyrics_message(
            song=song, artist=artists, link=make_yandex_song_link(song_id), lyrics=lyrics
        )

        await message.answer(text=msg_text, disable_web_page_preview=True)


@router.command(('playlist', 'playlists', 'p'), 'список плейлистов канала')  # /playlist
async def _(message: Message):
    await message.answer(PHRASES_RU.commands.playlist, disable_web_page_preview=True)


def register_password_handler(target: Router, password: str) -> None:
    @target.message(PasswordFilter(password))
    async def _(message: Message, **data):
        users_repo: UsersRepository = await data['dishka_container'].get(UsersRepository)
        if users_repo.set_admin(message.from_user.id, message.from_user.id):
            await message.delete()
            await message.answer(PHRASES_RU.success.promoted)
            await command_getcmds(message)
        else:
            await message.answer(PHRASES_RU.error.db)


@router.message()
async def _(message: Message, bot: Bot):
    if message.chat.type == 'private':
        await private.handler(message, bot)
        return

    if message.chat.type in ['group', 'supergroup']:
        await group.handler(message)
        return
