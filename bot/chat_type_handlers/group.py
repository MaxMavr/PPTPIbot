from aiogram.types import Message


async def handler(message: Message):
    print(message.from_user.id)
    print(message.text)
