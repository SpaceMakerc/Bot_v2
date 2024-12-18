from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboards.inline_keyboards.inline_button_information import (
    ShowCBData,
    ShowCategory,
    FilmCDData,
    MediaAction,
    PaginationFilmDirection,
    PaginationCBFilm
)


def get_film_list(
        films, pagination: int = 3, include_back: bool = False
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="В исходное меню",
        callback_data=ShowCBData(
            category=ShowCategory.root,
        )
    )
    for film in films:
        if pagination > film > pagination - 4:
            builder.button(
                text=films[film]["name"],
                callback_data=FilmCDData(
                    action=MediaAction.details,
                    id=films[film]["id"],
                    # name=films[film]["name"],
                    pagination=pagination
                )
            )
    if include_back:
        builder.button(
            text="Назад",
            callback_data=PaginationCBFilm(
                move=PaginationFilmDirection.back,
                pagination=pagination
            ).pack()
        )
    if len(films) > pagination:
        builder.button(
            text="Следующие",
            callback_data=PaginationCBFilm(
                move=PaginationFilmDirection.next,
                pagination=pagination
            ).pack()
        )

    builder.adjust(1)
    return builder.as_markup()


def get_film_details_kb(film_cb_data: FilmCDData) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Вернуться к списку фильмов",
        callback_data=ShowCBData(
            category=ShowCategory.film,
            pagination=film_cb_data.pagination
        )
    )
    builder.button(
        text="Удалить файл",
        callback_data=FilmCDData(
            action=MediaAction.remove,
            id=film_cb_data.id,
            # name=film_cb_data.name,
            pagination=film_cb_data.pagination
        )
    )
    builder.adjust(1)

    return builder.as_markup()
