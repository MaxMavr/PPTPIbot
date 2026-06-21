from aiogram import Bot
from aiogram.types import CallbackQuery

from bot.bot_utils.filters import EditFilter
from bot.keyboards import inline as ikb
from bot.metrics import record_post
from config import Config
from config.const import CHANNEL_ID
from db.repositories.users import UsersRepository
from phrases import PHRASES_RU


async def __clear_callback(callback: CallbackQuery) -> None:
    await callback.message.edit_reply_markup(reply_markup=None)


async def cancel_post(callback: CallbackQuery) -> None:
    await __clear_callback(callback)
    record_post('cancelled')


async def reject_post(callback: CallbackQuery, bot: Bot, user_id: int, message_id: int) -> None:
    await __clear_callback(callback)
    await bot.send_message(reply_to_message_id=message_id, chat_id=user_id, text=PHRASES_RU.success.not_publish_post)
    record_post('rejected')


async def publish_post(
    callback: CallbackQuery,
    bot: Bot,
    config: Config,
    users_repo: UsersRepository,
    user_id: int | None = None,
    message_id: int | None = None,
    anonymous: bool | None = None,
) -> None:
    await __clear_callback(callback)

    user = users_repo.get_user(user_id)

    if await EditFilter.check(bot, user.user_id):
        msg_text = callback.message.html_text
    elif anonymous:
        msg_text = callback.message.html_text + PHRASES_RU.info.from_user
    else:
        caption = (
            PHRASES_RU.replace('template.from_user', username=user.username)
            if user.username
            else PHRASES_RU.info.from_user
        )
        msg_text = callback.message.html_text + caption

    await bot.send_message(chat_id=CHANNEL_ID, text=msg_text, disable_web_page_preview=True)
    await callback.message.answer(text=PHRASES_RU.success.publish_post)
    record_post('published')

    if user and message_id:
        await bot.send_message(
            reply_to_message_id=message_id,
            chat_id=user.user_id,
            text=PHRASES_RU.success.publish_post,
        )


async def suggest_post(
    callback: CallbackQuery,
    bot: Bot,
    config: Config,
    users_repo: UsersRepository,
    user_id: int,
    message_id: int,
    anonymous: bool,
) -> None:
    await __clear_callback(callback)

    user = users_repo.get_user(user_id)

    user_data = {
        'username': f'@{user.username}' if user.username else PHRASES_RU.icon.not_username,
        'user_id': str(user.user_id).ljust(12),
        'registration_date': user.registration_date.strftime('%d.%m.%Y'),
    }

    await bot.send_message(
        chat_id=config.tg_bot.main_admin_id,
        text=PHRASES_RU.replace('template.user_info', **user_data),
        disable_web_page_preview=True,
    )

    main_admin_message = await callback.message.copy_to(
        chat_id=config.tg_bot.main_admin_id,
        disable_web_page_preview=True,
        reply_markup=ikb.approval_post(user_id, message_id, anonymous),
    )

    await bot.pin_chat_message(
        chat_id=config.tg_bot.main_admin_id,
        message_id=main_admin_message.message_id,
        disable_notification=True,
    )

    await callback.message.answer(text=PHRASES_RU.success.suggest_post)
    record_post('suggested')
