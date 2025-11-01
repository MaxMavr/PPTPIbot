from datetime import datetime
from pprint import pprint

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


@router.message(F.text.lower().in_(['мяу', 'мау', 'мив', 'мав', 'ку', 'кря', 'квак']))
async def _(message: Message):
    await default.cmd_admin_song(message)


@router.message(F.text.lower().in_(['пиу', 'пау', 'пум']))
async def _(message: Message):
    await default.cmd_mood_song(message)


REPEAT_MODES = {
    'OFF': '',
    'ONE': '↺¹ ',
    'ALL': '↺   '
}

PLAYER_TYPES = {
    'PLAYLIST': 'Плейлист слушает',
    'ALBUM': 'Альбом слушает',
    'ARTIST': 'Исполнителя слушает',
    'RADIO': 'Волну слушает',
}


@router.message(F.text.lower().in_(['мрр', 'мррр', 'мрррр']))
async def _(message: Message):
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        ynison = await get_admin_song_expanded()

        if isinstance(ynison, tuple):
            await default.cmd_admin_song(message)
            return
        ynison: Ynison

        paused_icon = '❚❚' if ynison.paused else '▷'
        offline_icon = '○' if ynison.is_offline else '●'

        repeat_icon = REPEAT_MODES.get(ynison.repeat_mode, ' -     ')

        player_text = PLAYER_TYPES.get(ynison.player_type, '      ')
        player_text = f'<b>{player_text}</b>'

        title = make_song_lyrics_message(song=ynison.song_title, artist=ynison.artists_title,
                                         link=make_yandex_song_link(ynison.song_id))

        def seconds_to_minsec(seconds: int) -> str:
            minutes = seconds // 60
            seconds = seconds % 60
            return f"{minutes}:{seconds:02}"

        def progress_bar(duration: int, song_duration: int, length: int = 16) -> str:
            pos = int((duration / song_duration) * length)
            return "━" * pos + "◉" + "┈" * (length - pos)

        def volume_bar(volume: float) -> str:
            volume_bars = ['▁', '▂', '▃', '▅', '▆', '▇', '▉']
            volume = max(0.0, min(1.0, volume))
            index = int(volume * (len(volume_bars) - 1))
            return ''.join(volume_bars[:index])

        if ynison.progress_s:
            progress_s = ynison.progress_s
        else:
            progress_s = round(datetime.now().timestamp()) - ynison.timestamp_s
            if progress_s > ynison.duration_s:
                progress_s = ynison.duration_s

        progress_bar_text = f"{seconds_to_minsec(progress_s)} " \
                            f"{progress_bar(progress_s, ynison.duration_s)} " \
                            f"{seconds_to_minsec(ynison.duration_s)}"

        volume_bar_text = volume_bar(ynison.volume)

        def seconds_to_date(seconds: int) -> str:
            return datetime.fromtimestamp(seconds).strftime('%H:%M:%S %d.%m.%Y')

        update_date = f'<span class="tg-spoiler">{seconds_to_date(ynison.timestamp_s)}</span>'

        icons_line = f"   {offline_icon}        {paused_icon}        {repeat_icon}   {volume_bar_text}"
        icons_descriptor = f"ᵒⁿˡᶦⁿᵉ   ᵖᵃᵘˢᵉ   ʳᵉᵖᵉᵃᵗ   ᵛᵒˡᵘᵐᵉ"

        caption_text = '\n'.join([player_text + ' ' + update_date, title, '', progress_bar_text, icons_line, icons_descriptor])

        await message.answer_photo(photo=ynison.cover_url, caption=caption_text)
