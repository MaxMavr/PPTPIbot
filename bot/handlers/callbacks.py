from aiogram import Router
from aiogram.types import CallbackQuery
from bot.models import PageCallBack, PostCallBack
from bot import pages
from bot.chat_type_handlers import channel

router = Router()


@router.callback_query(PageCallBack.filter())
async def cut_message_distributor(callback: CallbackQuery, callback_data: PageCallBack):
    action = callback_data.action
    page = callback_data.page
    user_id = callback_data.user_id
    if action == 1:
        await pages.get_users(callback.from_user.id, page, callback.message.message_id)
    elif action == 2:
        await pages.user_query(callback.from_user.id, user_id, page, callback.message.message_id)
    elif action == -1:
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
