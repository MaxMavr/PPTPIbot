from datetime import datetime

from aiogram.types import Message
from aiogram import Router, F
from aiogram.utils.chat_action import ChatActionSender

from bot.handlers import default
from config import bot
from phrases import PHRASES_RU
from utils.format_string import make_song_lyrics_message
from utils.links import make_yandex_song_link
from utils.music_yandex import get_admin_song_expanded, Ynison

router = Router()


@router.message(F.text.lower().in_(['спасибо', 'от души', 'благодарю']))
async def _(message: Message):
    await message.answer(text=PHRASES_RU.answers.welcome)


@router.message(F.text.lower().in_(['мяу', 'мау', 'мив', 'мав', 'ку', 'кря', 'пиу', 'пау', 'пум', 'квак']))
async def _(message: Message):
    await default.cmd_admin_song(message)


@router.message(F.text.lower().in_(['мрр']))
async def _(message: Message):
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        ynison = await get_admin_song_expanded()

        if isinstance(ynison, tuple):
            await default.cmd_admin_song(message)
            return
        ynison: Ynison

        # paused_icon = '❚❚' if ynison.paused else '▶'

        repeat_modes = {
            'OFF': '',
            'ONE': '🔂 ',
            'ALL': '🔁 '
        }

        repeat_icon = repeat_modes.get(ynison.repeat_mode, '')

        player_types = {
            'PLAYLIST': 'Плейлист слушает',
            'ALBUM': 'Альбом слушает',
            'ARTIST': 'Исполнителя слушает',
            'RADIO': 'Волну слушает',
        }

        player_text = player_types.get(ynison.player_type, '')

        title = make_song_lyrics_message(song=ynison.song_title, artist=ynison.artists_title,
                                         link=make_yandex_song_link(ynison.song_id))

        def ms_to_minsec(seconds: int) -> str:
            minutes = seconds // 60
            seconds = seconds % 60
            return f"{minutes}:{seconds:02}"

        def bar(duration: int, song_duration: int, length: int = 20) -> str:
            pos = int((duration / song_duration) * length)
            bar_str = "─" * length
            bar_str = bar_str[:pos] + "◉" + bar_str[pos + 1:]
            return bar_str

        progress_s = ynison.progress_s if ynison.progress_s \
            else round(datetime.now().timestamp()) - ynison.timestamp_s

        progress_bar = f"{ms_to_minsec(progress_s)} " \
                       f"{bar(progress_s, ynison.duration_s)} " \
                       f"{ms_to_minsec(ynison.duration_s)}"

        def ms_to_date(s: int) -> str:
            return datetime.fromtimestamp(s).strftime('%H:%M:%S %d.%m.%Y')

        # update_date = f'<span class="tg-spoiler">{ms_to_date(ynison.timestamp_s)}</span>'
        update_date = f''

        mgs_text = '\n'.join([repeat_icon + title, progress_bar, player_text, update_date])

        await message.answer(mgs_text, disable_web_page_preview=True)
