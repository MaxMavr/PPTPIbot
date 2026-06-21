from aiogram import Bot, Router
from aiogram.types import CallbackQuery

from bot.bot_utils.models import HelpCallBack, PostCallBack
from bot.chat_type_handlers import channel
from config import Config
from db.repositories.users import UsersRepository
from phrases import PHRASES_RU
from utils.format_song_line import format_song_line

router = Router()


@router.callback_query(PostCallBack.filter())
async def post_distributor(callback: CallbackQuery, callback_data: PostCallBack, bot: Bot, **kwargs):
    await callback.answer()

    container = kwargs['dishka_container']
    config: Config = await container.get(Config)
    users_repo: UsersRepository = await container.get(UsersRepository)

    action = callback_data.action
    user_id = callback_data.user_id
    message_id = callback_data.message_id
    anonymous = callback_data.anonymous

    if action == 1:
        await channel.suggest_post(callback, bot, config, users_repo, user_id, callback.message.message_id, anonymous)
    elif action == 2:
        await channel.publish_post(callback, bot, config, users_repo, user_id, message_id, anonymous)
    elif action == -1:
        await channel.reject_post(callback, bot, user_id, message_id)
    elif action == -2:
        await channel.cancel_post(callback)


@router.callback_query(HelpCallBack.filter())
async def help_distributor(callback: CallbackQuery, callback_data: HelpCallBack):
    await callback.answer()

    action = callback_data.action

    examples = {
        1: (PHRASES_RU.callback.help_examples.example1, PHRASES_RU.help_examples.exemple1),
        2: (PHRASES_RU.callback.help_examples.example2, PHRASES_RU.help_examples.exemple2),
        3: (PHRASES_RU.callback.help_examples.example3, PHRASES_RU.help_examples.exemple3),
    }

    if action in examples:
        example = examples[action]
        await callback.answer(example[0])
        await callback.message.answer(example[1], disable_web_page_preview=True)
        await callback.message.answer(await format_song_line(example[1]), disable_web_page_preview=True)
