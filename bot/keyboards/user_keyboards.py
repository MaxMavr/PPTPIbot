from aiogram.utils.keyboard import ReplyKeyboardMarkup as KMarkup
from aiogram.utils.keyboard import KeyboardButton as KButton
from phrases import PHRASES_RU
import random


def make_main():
    def __make_placeholder_appeal() -> str:
        items = PHRASES_RU.placeholder_appeal.items
        selected_items = random.sample(items, random.randint(1, len(items)))
        placeholder_appeal = '-'.join(selected_items) + '-' + PHRASES_RU.placeholder_appeal.ending
        return placeholder_appeal.capitalize()

    return KMarkup(
        keyboard=[[KButton(text=PHRASES_RU.button.main.suggest_post),
                   KButton(text=PHRASES_RU.button.main.admin_song)]],
        resize_keyboard=True,
        input_field_placeholder=__make_placeholder_appeal()
    )
