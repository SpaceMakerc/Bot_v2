from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from .button_information import (StartButtonNames, StoreButtonNames,
                                 GenreButtonName, PictureStatusButtonName)


def get_start_kb() -> ReplyKeyboardMarkup:
    button_weather = KeyboardButton(text=StartButtonNames.weather)
    button_help = KeyboardButton(text=StartButtonNames.help)
    button_store_info = KeyboardButton(text=StartButtonNames.survey)
    button_outlet = KeyboardButton(text=StartButtonNames.outlet)

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [button_weather, button_help],
            [button_store_info, button_outlet]
        ],
        resize_keyboard=True
    )
    return keyboard


def get_store_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.button(text=StoreButtonNames.film)
    builder.button(text=StoreButtonNames.serial)
    builder.button(text=StoreButtonNames.picture)
    builder.button(text=StoreButtonNames.doc)

    builder.adjust(2)

    return builder.as_markup(resize_keyboard=True)


def get_genre_options_kb(
        media: str = StoreButtonNames.film
) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.button(text=GenreButtonName.comedy)
    builder.button(text=GenreButtonName.horror)
    builder.button(text=GenreButtonName.drama)
    builder.button(text=GenreButtonName.fantasy)
    builder.button(text=GenreButtonName.fantastic)
    builder.button(text=GenreButtonName.adventures)
    if media != StoreButtonNames.film:
        builder.button(text=GenreButtonName.sit_com)
    builder.adjust(2)

    return builder.as_markup(resize_keyboard=True)


def get_picture_status_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.button(text=PictureStatusButtonName.plain)
    builder.button(text=PictureStatusButtonName.special)

    builder.adjust(1)

    return builder.as_markup(resize_keyboard=True)
