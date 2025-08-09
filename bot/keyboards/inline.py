from typing import Union
from aiogram.types import InlineKeyboardButton as IButton
from aiogram.types import InlineKeyboardMarkup as IMarkup
from phrases import PHRASES_RU
from bot.bot_utils.models import PageCallBack, PostCallBack, HelpCallBack
from DB.models import Pagination


def page_keyboard(type_of_event: int, pagination: Pagination, user_id: int = 0) -> Union[IMarkup, None]:
    if pagination.total_pages <= 1:
        return None

    no_action = PageCallBack(type_of_event=-1).pack()

    past_button = IButton(
        text=PHRASES_RU.button.past_page,
        callback_data=PageCallBack(type_of_event=type_of_event, page=pagination.page - 1, user_id=user_id).pack()
    ) if pagination.has_prev else IButton(text=' ', callback_data=no_action)

    next_button = IButton(
        text=PHRASES_RU.button.next_page,
        callback_data=PageCallBack(type_of_event=type_of_event, page=pagination.page + 1, user_id=user_id).pack()
    ) if pagination.has_next else IButton(text=' ', callback_data=no_action)

    return IMarkup(inline_keyboard=[[
        past_button,
        IButton(text=f'{pagination.page}{PHRASES_RU.icon.page_separator}{pagination.total_pages}',
                callback_data=no_action),
        next_button
    ]])


def suggest_post(user_id: int, message_id: int) -> IMarkup:
    return IMarkup(inline_keyboard=[[
        IButton(text=PHRASES_RU.button.suggest_post,
                callback_data=PostCallBack(action=1, user_id=user_id,
                                           message_id=message_id).pack()),
        IButton(text=PHRASES_RU.button.anonymous_suggest_post,
                callback_data=PostCallBack(action=1, user_id=user_id,
                                           message_id=message_id, anonymous=True).pack())
    ]])


def publish_post(user_id: int) -> IMarkup:
    return IMarkup(inline_keyboard=[[IButton(text=PHRASES_RU.button.publish_post,
                                             callback_data=PostCallBack(action=2, user_id=user_id).pack())]])


def approval_post(user_id: int, message_id: int, anonymous: bool) -> IMarkup:
    return IMarkup(inline_keyboard=[
        [IButton(text=PHRASES_RU.button.publish_post,
                 callback_data=PostCallBack(action=2, user_id=user_id, message_id=message_id, anonymous=anonymous).pack()),
         IButton(text=PHRASES_RU.button.reject_post,
                 callback_data=PostCallBack(action=-1, user_id=user_id, message_id=message_id).pack())
         ]])


help_examples = IMarkup(inline_keyboard=[[
    IButton(text=PHRASES_RU.button.help_examples.example1, callback_data=HelpCallBack(action=1).pack()),
    IButton(text=PHRASES_RU.button.help_examples.example2, callback_data=HelpCallBack(action=2).pack()),
    IButton(text=PHRASES_RU.button.help_examples.example3, callback_data=HelpCallBack(action=3).pack())
]])
