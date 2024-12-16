from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboards.inline_keyboards.inline_button_information import ShowCBData, \
    ShowCategory


def get_start_showtime_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Фильмы",
        callback_data=ShowCBData(
            category=ShowCategory.film,
            pagination=None
        )
    ),
    builder.button(
        text="Сериалы",
        callback_data=ShowCBData(
            category=ShowCategory.serial,
            pagination=None
        )
    ),
    builder.button(
        text="Картинки",
        callback_data=ShowCBData(
            category=ShowCategory.picture,
            pagination=None
        )
    ),
    builder.button(
        text="Документы",
        callback_data=ShowCBData(
            category=ShowCategory.doc,
            pagination=None
        )
    )

    builder.adjust(2)

    return builder.as_markup()
