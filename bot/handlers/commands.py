from aiogram.types import Message

from bot.routers import UserRouter, BaseRouter
from phrases import PHRASES_RU

from utils.music_yandex import get_admin_song, get_random_song_lines
from utils.format_string import make_song_lyrics_message, make_yandex_song_link

router = UserRouter()


@router.command('start', 'запустить бота')  # /start
async def _(message: Message):
    await message.answer(PHRASES_RU.commands.start)


@router.command('help', 'как пользоваться ботом')  # /help
async def _(message: Message):
    await message.answer(PHRASES_RU.commands.help)


@router.command('about', 'о разработчиках')  # /about
async def _(message: Message):
    await message.answer(PHRASES_RU.commands.about, disable_web_page_preview=True)


@router.command(('commands', 'cmd'), 'список всех команд (это сообщение)')  # /commands
async def _(message: Message):
    commands_text = '\n'.join(str(command) for command in BaseRouter.available_commands if not command.is_admin)
    await message.answer(PHRASES_RU.title.commands + commands_text)


@router.command('admin_song', 'получить песню, которую сейчас слушает админ')  # /admin_song
async def cmd_admin_song(message: Message):
    song, artists, song_id, album_id = await get_admin_song()
    lines = await get_random_song_lines(song_id)
    msg_text = make_song_lyrics_message(song=song, artist=artists,
                                        link=make_yandex_song_link(song_id, album_id), lines=lines)

    await message.answer(text=msg_text, disable_web_page_preview=True)
