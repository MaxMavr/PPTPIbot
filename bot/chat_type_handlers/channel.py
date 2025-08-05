from typing import Optional

from aiogram.types import CallbackQuery

from bot.bot_utils.filters import EditFilter
from config.const import CHANNEL_ID
from config import bot, config
from bot.keyboards import inline as ikb
from phrases import PHRASES_RU


async def __clear_callback(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_reply_markup(reply_markup=None)


async def reject_post(callback: CallbackQuery):
    await __clear_callback(callback)
    # TODO: Сделать оповещение, что мы не выложили пост


async def publish_post(callback: CallbackQuery, chat_id: Optional[int] = None, message_id: Optional[int] = None):
    await __clear_callback(callback)

    if not await EditFilter.check(callback.from_user.id):
        msg_text = callback.message.text + f'\n\nОт @{callback.from_user.username}'
    else:
        msg_text = callback.message.text

    await bot.send_message(chat_id=CHANNEL_ID, text=msg_text)
    await callback.message.answer(text=PHRASES_RU.success.publish_post)

    if chat_id and message_id:
        await bot.send_message(reply_to_message_id=message_id,
                               chat_id=chat_id,
                               text=PHRASES_RU.success.publish_post)


async def suggest_post(callback: CallbackQuery, chat_id: int, message_id: int):
    # TODO: Предложить выложить анонимно
    await __clear_callback(callback)
    await bot.send_message(chat_id=config.tg_bot.main_admin_id,
                           text=PHRASES_RU.replace('template.from_user', username=callback.from_user.username))
    await callback.message.copy_to(chat_id=config.tg_bot.main_admin_id,
                                   disable_web_page_preview=True,
                                   reply_markup=ikb.approval_post(chat_id, message_id))
    await callback.message.answer(text=PHRASES_RU.success.suggest_post)
