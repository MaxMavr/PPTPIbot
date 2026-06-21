from aiogram.types import InlineKeyboardButton as IButton
from aiogram.types import InlineKeyboardMarkup as IMarkup

from bot.bot_utils.models import HelpCallBack, PostCallBack
from phrases import PHRASES_RU


def suggest_post(user_id: int, message_id: int) -> IMarkup:
    return IMarkup(
        inline_keyboard=[
            [
                IButton(
                    text=PHRASES_RU.button.suggest_post,
                    callback_data=PostCallBack(action=1, user_id=user_id, message_id=message_id).pack(),
                ),
                IButton(
                    text=PHRASES_RU.button.anonymous_suggest_post,
                    callback_data=PostCallBack(action=1, user_id=user_id, message_id=message_id, anonymous=True).pack(),
                ),
            ],
            [
                IButton(text=PHRASES_RU.button.cancel_post, callback_data=PostCallBack(action=-2).pack()),
            ],
        ]
    )


def publish_post(user_id: int) -> IMarkup:
    return IMarkup(
        inline_keyboard=[
            [
                IButton(
                    text=PHRASES_RU.button.publish_post,
                    callback_data=PostCallBack(action=2, user_id=user_id).pack(),
                ),
                IButton(text=PHRASES_RU.button.cancel_post, callback_data=PostCallBack(action=-2).pack()),
            ]
        ]
    )


def approval_post(user_id: int, message_id: int, anonymous: bool) -> IMarkup:
    return IMarkup(
        inline_keyboard=[
            [
                IButton(
                    text=PHRASES_RU.button.publish_post,
                    callback_data=PostCallBack(
                        action=2, user_id=user_id, message_id=message_id, anonymous=anonymous
                    ).pack(),
                ),
                IButton(
                    text=PHRASES_RU.button.reject_post,
                    callback_data=PostCallBack(action=-1, user_id=user_id, message_id=message_id).pack(),
                ),
            ]
        ]
    )


help_examples = IMarkup(
    inline_keyboard=[
        [
            IButton(text=PHRASES_RU.button.help_examples.example1, callback_data=HelpCallBack(action=1).pack()),
            IButton(text=PHRASES_RU.button.help_examples.example2, callback_data=HelpCallBack(action=2).pack()),
            IButton(text=PHRASES_RU.button.help_examples.example3, callback_data=HelpCallBack(action=3).pack()),
        ]
    ]
)
