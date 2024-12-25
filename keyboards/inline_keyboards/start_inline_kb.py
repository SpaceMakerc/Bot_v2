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
        )
    ),
    builder.button(
        text="Сериалы",
        callback_data=ShowCBData(
            category=ShowCategory.serial,
        )
    ),
    builder.button(
        text="Картинки",
        callback_data=ShowCBData(
            category=ShowCategory.picture,
        )
    ),
    builder.button(
        text="Документы",
        callback_data=ShowCBData(
            category=ShowCategory.doc,
        )
    )

    builder.adjust(2)

    return builder.as_markup()
