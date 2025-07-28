import logging
from typing import Any, Awaitable, Callable, Optional

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Update
from DB.models import UserModel as UserModel
from config import bot
from config.const import CHANNEL_ID
from phrases import PHRASES_RU

logger = logging.getLogger(__name__)


class ShadowNotSubscribedMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: dict[str, Any],
    ) -> Any:

        user_row: Optional[UserModel] = data.get('user_row')
        if user_row is None:
            logger.warning(
                'Cannot check for shadow not subscribed. The \'user_row\' '
                'key was not found in the middleware data.'
            )
            return await handler(event, data)

        if event.message and event.message.text and event.message.text.startswith('/start'):
            return await handler(event, data)

        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_row.user_id)

        if member.status in ['member', 'administrator', 'creator']:
            return await handler(event, data)

        logger.warning('Shadow not subscribed user tried to interact: %d', user_row.user_id)

        if event.callback_query:
            await event.callback_query.answer(text=PHRASES_RU.error.not_subscribed, show_alert=True,
                                              disable_web_page_preview=True)
        elif event.message:
            await event.message.answer(text=PHRASES_RU.error.not_subscribed, disable_web_page_preview=True)

        return


