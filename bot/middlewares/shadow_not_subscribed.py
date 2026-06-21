import logging
from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware, Bot
from aiogram.types import TelegramObject, Update

from config.const import CHANNEL_ID
from db.models import UserModel
from phrases import PHRASES_RU

logger = logging.getLogger(__name__)


class ShadowNotSubscribedMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: dict[str, Any],
    ) -> Any:
        user_row: UserModel | None = data.get('user_row')
        if user_row is None:
            logger.warning(
                "Cannot check for shadow not subscribed. The 'user_row' key was not found in the middleware data."
            )
            return await handler(event, data)

        if event.message and event.message.text and event.message.text.startswith('/start'):
            return await handler(event, data)

        bot: Bot = data['bot']
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_row.user_id)

        if member.status in ['member', 'administrator', 'creator']:
            return await handler(event, data)

        logger.warning('Shadow not subscribed user tried to interact: %d', user_row.user_id)

        if event.callback_query:
            await event.callback_query.answer(text=PHRASES_RU.error.not_subscribed, show_alert=True)
        elif event.message:
            await event.message.answer(text=PHRASES_RU.error.not_subscribed, disable_web_page_preview=True)

        return None
