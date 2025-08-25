from aiogram import Router
from aiogram.types import CallbackQuery
from bot.bot_utils.models import PageCallBack, PostCallBack, HelpCallBack
from bot import pages
from bot.chat_type_handlers import channel
from phrases import PHRASES_RU
from utils.format_song_line import format_song_line

router = Router()


@router.callback_query(PageCallBack.filter())
async def cut_message_distributor(callback: CallbackQuery, callback_data: PageCallBack):
    await callback.answer()

    type_of_event = callback_data.type_of_event
    page = callback_data.page
    user_id = callback_data.user_id

    if type_of_event == 1:
        await pages.get_users(callback.from_user.id, page, callback.message.message_id)
    elif type_of_event == 2:
        await pages.user_query(callback.from_user.id, user_id, page, callback.message.message_id)
    elif type_of_event == -1:
        pass


@router.callback_query(PostCallBack.filter())
async def cut_message_distributor(callback: CallbackQuery, callback_data: PostCallBack):
    await callback.answer()

    action = callback_data.action
    user_id = callback_data.user_id
    message_id = callback_data.message_id
    anonymous = callback_data.anonymous

    if action == 1:
        await channel.suggest_post(callback, user_id, callback.message.message_id, anonymous)
    elif action == 2:
        await channel.publish_post(callback, user_id, message_id, anonymous)
    elif action == -1:
        await channel.reject_post(callback, user_id, message_id)
    elif action == -2:
        await channel.cancel_post(callback)


@router.callback_query(HelpCallBack.filter())
async def cut_message_distributor(callback: CallbackQuery, callback_data: PostCallBack):
    await callback.answer()

    action = callback_data.action

    examples = {
        1: (PHRASES_RU.callback.help_examples.example1, PHRASES_RU.help_examples.exemple1),
        2: (PHRASES_RU.callback.help_examples.example2, PHRASES_RU.help_examples.exemple2),
        3: (PHRASES_RU.callback.help_examples.example3, PHRASES_RU.help_examples.exemple3),
    }

    if action in examples:
        example = examples[action]
        await callback.answer(example[0], disable_web_page_preview=True)
        await callback.message.answer(example[1], disable_web_page_preview=True)
        await callback.message.answer(await format_song_line(example[1]), disable_web_page_preview=True)
