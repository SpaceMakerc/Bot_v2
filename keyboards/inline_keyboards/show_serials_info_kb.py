from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboards.inline_keyboards.inline_button_information import (
    ShowCategory,
    ShowCBData,
    MediaAction,
    SerialCBData,
    PaginationCBSerial,
    PaginationSerialDirection
)


def get_serial_list(
        serials, pagination: int = 3, include_back: bool = False
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="В исходное меню",
        callback_data=ShowCBData(
            category=ShowCategory.root,
        )
    )
    for serial in serials:
        if pagination > serial > pagination - 4:
            builder.button(
                text=serials[serial]["name"],
                callback_data=SerialCBData(
                    action=MediaAction.details,
                    id=serials[serial]["id"],
                    name=serials[serial]["name"],
                    pagination=pagination
                )
            )
    if include_back:
        builder.button(
            text="Назад",
            callback_data=PaginationCBSerial(
                move=PaginationSerialDirection.back,
                pagination=pagination
            ).pack()
        )
    if len(serials) > pagination:
        builder.button(
            text="Следующие",
            callback_data=PaginationCBSerial(
                move=PaginationSerialDirection.next,
                pagination=pagination
            ).pack()
        )

    builder.adjust(1)
    return builder.as_markup()


# TODO Here serial_cb_data for future delete or update serials
def get_serial_details_kb(serial_cb_data: SerialCBData) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Вернуться к списку фильмов",
        callback_data=ShowCBData(
            category=ShowCategory.serial,
            pagination=serial_cb_data.pagination
        )
    )
    builder.adjust(1)

    return builder.as_markup()
