from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboards.inline_keyboards.inline_button_information import (
    ShowCBData,
    ShowCategory,
    FilmCDData,
    FilmActions,
    PaginationDirection,
    PaginationCBFilm
)


def get_start_showtime_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Фильмы",
        callback_data=ShowCBData(category=ShowCategory.film).pack()
    ),
    builder.button(
        text="Сериалы",
        callback_data=ShowCBData(category=ShowCategory.serial).pack()
    ),
    builder.button(
        text="Картинки",
        callback_data=ShowCBData(category=ShowCategory.picture).pack()
    ),
    builder.button(
        text="Документы",
        callback_data=ShowCBData(category=ShowCategory.doc).pack()
    )

    builder.adjust(2)

    return builder.as_markup()


def get_film_list(
        films, pagination: int = 3, include_back: bool = False
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="В исходное меню",
        callback_data=ShowCBData(category=ShowCategory.root).pack()
    )
    for film in films:
        if pagination > film > pagination - 4:
            builder.button(
                text=films[film]["name"],
                callback_data=FilmCDData(
                    action=FilmActions.details,
                    id=films[film]["id"],
                    name=films[film]["name"],
                )
            )
    if include_back:
        builder.button(
            text="Назад",
            callback_data=PaginationCBFilm(
                move=PaginationDirection.back,
                pagination=pagination
            ).pack()
        )
    if len(films) > pagination:
        builder.button(
            text="Следующие",
            callback_data=PaginationCBFilm(
                move=PaginationDirection.next,
                pagination=pagination
            ).pack()
        )

    builder.adjust(1)
    return builder.as_markup()


# TODO Here film_cb_data for future delete or update films
def get_film_details_kb(film_cb_data: FilmCDData) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Вернуться к списку фильмов",
        callback_data=ShowCBData(category=ShowCategory.film)
    )
    builder.adjust(1)

    return builder.as_markup()
