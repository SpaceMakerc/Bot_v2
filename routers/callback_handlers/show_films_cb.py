from aiogram import Router, F
from aiogram.types.callback_query import CallbackQuery
from aiogram.utils import markdown

from db.db_ import managers
from db.queries import get_user_films_by_user, get_user_film_by_table_id
from keyboards.inline_keyboards.inline_button_information import (
    ShowCBData,
    ShowCategory,
    PaginationCBFilm,
    PaginationDirection,
    FilmCDData,
    FilmActions
)
from keyboards.inline_keyboards.show_information_kb import (
    get_film_list,
    get_start_showtime_kb,
    get_film_details_kb
)

router = Router(name=__name__)


@router.callback_query(ShowCBData.filter(F.category == ShowCategory.film))
async def handle_show_films_button(
        callback_query: CallbackQuery,
        callback_data: ShowCBData
):
    user_id = int(callback_query.from_user.id)
    films = await get_user_films_by_user(manager=managers, user_id=user_id)
    include_back = (
        False if callback_data.pagination == 3 or callback_data.pagination is
        None else True
    )

    await callback_query.answer()
    if films:
        if callback_data.pagination is None:
            await callback_query.message.edit_text(
                text="Список твоих фильмов:",
                reply_markup=get_film_list(
                    films=films, include_back=include_back
                )
            )
        else:
            await callback_query.message.edit_text(
                text="Список твоих фильмов:",
                reply_markup=get_film_list(
                    films=films, pagination=callback_data.pagination,
                    include_back=include_back
                )
            )
    else:
        await callback_query.message.answer(
            text="У тебя ещё нет сохранённых фильмов. Для того чтобы добавить"
                 " фильм, жми на /start или /survey и сохрани что-нибудь"
        )


@router.callback_query(ShowCBData.filter(F.category == ShowCategory.root))
async def handle_back_to_start_button(callback_query: CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_text(
        text="Давай посмотрим что у тебя есть. Выбери категорию",
        reply_markup=get_start_showtime_kb()
    )


@router.callback_query(FilmCDData.filter(F.action == FilmActions.details))
async def handle_show_detail_button(
        callback_query: CallbackQuery,
        callback_data: FilmCDData
):
    table_id = callback_data.id
    data = await get_user_film_by_table_id(manager=managers, table_id=table_id)
    await callback_query.answer()
    message_text = markdown.text(
        markdown.hbold("Название:"), data["name"],
        markdown.hbold("Комментарий:"), data["comment"],
        markdown.hbold("Жанр:"), data["genre"],
        sep="\n"
    )
    await callback_query.message.edit_text(
        text=message_text,
        reply_markup=get_film_details_kb(film_cb_data=callback_data)
    )


@router.callback_query(
    PaginationCBFilm.filter(F.move == PaginationDirection.next)
)
async def handle_show_next_films_button(
        callback_query: CallbackQuery,
        callback_data: PaginationCBFilm
):
    user_id = int(callback_query.from_user.id)
    films = await get_user_films_by_user(manager=managers, user_id=user_id)
    await callback_query.answer()
    callback_data.pagination = callback_data.pagination + 3
    await callback_query.message.edit_text(
        text="Ещё список твоих фильмов",
        reply_markup=get_film_list(
            films=films, pagination=callback_data.pagination, include_back=True)
    )


@router.callback_query(
    PaginationCBFilm.filter(F.move == PaginationDirection.back)
)
async def handle_show_previous_films_button(
        callback_query: CallbackQuery,
        callback_data: PaginationCBFilm
):
    user_id = int(callback_query.from_user.id)
    films = await get_user_films_by_user(manager=managers, user_id=user_id)
    await callback_query.answer()
    callback_data.pagination = callback_data.pagination - 3
    include_back = False if callback_data.pagination == 3 else True
    await callback_query.message.edit_text(
        text="Предыдущий список твоих фильмов",
        reply_markup=get_film_list(
            films=films, pagination=callback_data.pagination,
            include_back=include_back
        )
    )
