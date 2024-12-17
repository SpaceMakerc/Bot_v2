from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup

from keyboards.inline_keyboards.inline_button_information import (
    ShowCBData,
    ShowCategory,
    PictureCBData,
    MediaAction,
    PaginationPictureDirection,
    PaginationCBPicture,
)


def get_pictures_list(
        pictures, pagination: int = 3, include_back: bool = False
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="В исходное меню",
        callback_data=ShowCBData(
            category=ShowCategory.root,
        )
    )
    for picture in pictures:
        if pagination > picture > pagination - 4:
            builder.button(
                text=pictures[picture]["comment"],
                callback_data=PictureCBData(
                    action=MediaAction.details,
                    id=pictures[picture]["id"],
                    name=pictures[picture]["comment"],
                    pagination=pagination
                )
            )
    if include_back:
        builder.button(
            text="Назад",
            callback_data=PaginationCBPicture(
                move=PaginationPictureDirection.back,
                pagination=pagination
            ).pack()
        )
    if len(pictures) > pagination:
        builder.button(
            text="Следующие",
            callback_data=PaginationCBPicture(
                move=PaginationPictureDirection.next,
                pagination=pagination
            ).pack()
        )

    builder.adjust(1)
    return builder.as_markup()


def get_picture_details_kb(
        picture_cb_data: PictureCBData
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Вернуться к списку картинок",
        callback_data=ShowCBData(
            category=ShowCategory.picture,
            pagination=picture_cb_data.pagination
        )
    )
    builder.adjust(1)

    return builder.as_markup()
