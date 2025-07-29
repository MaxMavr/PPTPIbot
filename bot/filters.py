from typing import Optional

from aiogram.filters import BaseFilter, Filter
from aiogram.types import Message

from DB.tables.users import UsersTable
from DB.models import UserModel

from config import bot
from config.const import CHANNEL_ID


async def get_editors():
    return [editor.user.id for editor in
            (await bot.get_chat_administrators(chat_id=CHANNEL_ID))
            if not editor.user.is_bot]


class AdminFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        with UsersTable() as users_db:
            user: Optional[UserModel] = users_db.get_user(message.from_user.id)
            if user:
                return user.is_admin
            return False


class EditFilter(Filter):
    @staticmethod
    async def check(user_id) -> bool:
        return user_id in (await get_editors())

    async def __call__(self, message: Message) -> bool:
        return await self.check(message.from_user.id)
