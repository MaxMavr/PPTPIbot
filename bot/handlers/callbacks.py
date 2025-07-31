from aiogram import Router
from aiogram.types import CallbackQuery
from bot.bot_utils.models import PageCallBack, PostCallBack, HelpCallBack
from bot import pages
from bot.chat_type_handlers import channel
from phrases import PHRASES_RU

router = Router()


@router.callback_query(PageCallBack.filter())
async def cut_message_distributor(callback: CallbackQuery, callback_data: PageCallBack):
    type_of_event = callback_data.type_of_event
    page = callback_data.page
    user_id = callback_data.user_id
    if type_of_event == 1:
        await pages.get_users(callback.from_user.id, page, callback.message.message_id)
    elif type_of_event == 2:
        await pages.user_query(callback.from_user.id, user_id, page, callback.message.message_id)
    elif type_of_event == -1:
        await callback.answer()


@router.callback_query(PostCallBack.filter())
async def cut_message_distributor(callback: CallbackQuery, callback_data: PostCallBack):
    action = callback_data.action
    chat_id = callback_data.chat_id
    message_id = callback_data.message_id

    if action == 1:
        await channel.suggest_post(callback, callback.from_user.id, callback.message.message_id)
    elif action == 2:
        await channel.publish_post(callback, chat_id, message_id)
    elif action == -1:
        await channel.reject_post(callback)


@router.callback_query(HelpCallBack.filter())
async def cut_message_distributor(callback: CallbackQuery, callback_data: PostCallBack):
    action = callback_data.action

    if action == 1:
        await callback.answer(PHRASES_RU.callback.help_examples.example1, disable_web_page_preview=True)
        await callback.message.answer(PHRASES_RU.help_examples.exemple1.request, disable_web_page_preview=True)
        await callback.message.answer(PHRASES_RU.help_examples.exemple1.response, disable_web_page_preview=True)
    elif action == 2:
        await callback.answer(PHRASES_RU.callback.help_examples.example2, disable_web_page_preview=True)
        await callback.message.answer(PHRASES_RU.help_examples.exemple2.request, disable_web_page_preview=True)
        await callback.message.answer(PHRASES_RU.help_examples.exemple2.response, disable_web_page_preview=True)
    elif action == 3:
        await callback.answer(PHRASES_RU.callback.help_examples.example3, disable_web_page_preview=True)
        await callback.message.answer(PHRASES_RU.help_examples.exemple3.request, disable_web_page_preview=True)
        await callback.message.answer(PHRASES_RU.help_examples.exemple3.response, disable_web_page_preview=True)
