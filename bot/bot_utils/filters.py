from aiogram import Bot
from aiogram.filters import BaseFilter, Filter
from aiogram.types import Message

from config.const import CHANNEL_ID
from db.models import UserModel


class AdminFilter(BaseFilter):
    async def __call__(self, message: Message, user_row: UserModel | None = None) -> bool:
        return user_row is not None and user_row.is_admin


async def get_editors(bot: Bot) -> list[int]:
    return [
        editor.user.id for editor in (await bot.get_chat_administrators(chat_id=CHANNEL_ID)) if not editor.user.is_bot
    ]


class EditFilter(Filter):
    @staticmethod
    async def check(bot: Bot, user_id: int) -> bool:
        return user_id in (await get_editors(bot))

    async def __call__(self, message: Message, bot: Bot) -> bool:
        return await self.check(bot, message.from_user.id)
