from aiogram import Router, F
from aiogram.types.callback_query import CallbackQuery
from aiogram.utils import markdown

from keyboards.inline_keyboards.inline_button_information import (
    ShowCBData,
    ShowCategory,
    SerialCBData,
    MediaAction,
    PaginationCBSerial,
    PaginationSerialDirection
)
from keyboards.inline_keyboards.show_serials_info_kb import (
    get_serial_list,
    get_serial_details_kb
)
from keyboards.inline_keyboards.start_inline_kb import get_start_showtime_kb
from db.queries import get_serials_by_user, get_serial_by_table_id
from db.db_ import managers

router = Router(name=__name__)


@router.callback_query(ShowCBData.filter(F.category == ShowCategory.serial))
async def handle_show_serial_button(
        callback_query: CallbackQuery,
        callback_data: ShowCBData
):
    user_id = int(callback_query.from_user.id)
    serials = await get_serials_by_user(manager=managers, user_id=user_id)
    await callback_query.answer()
    include_back = (
        False if callback_data.pagination == 3 or callback_data.pagination is
        None else True
    )
    if serials:
        if callback_data.pagination is None:
            await callback_query.message.edit_text(
                text="Список твоих сериалов",
                reply_markup=get_serial_list(
                    serials=serials, include_back=include_back
                )
            )
        else:
            await callback_query.message.edit_text(
                text="Список твоих сериалов",
                reply_markup=get_serial_list(
                    serials=serials, include_back=include_back,
                    pagination=callback_data.pagination
                )
            )
    else:
        await callback_query.message.answer(
            text="У тебя ещё нет сохранённых сериалов. Для того чтобы добавить"
                 " сериал, жми на /start или /survey и сохрани что-нибудь"
        )


@router.callback_query(ShowCBData.filter(F.category == ShowCategory.root))
async def handle_back_to_start_button(callback_query: CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_text(
        text="Давай посмотрим что у тебя есть. Выбери категорию",
        reply_markup=get_start_showtime_kb()
    )


@router.callback_query(SerialCBData.filter(F.action == MediaAction.details))
async def handle_show_detail_button(
        callback_query: CallbackQuery,
        callback_data: SerialCBData
):
    table_id = callback_data.id
    data = await get_serial_by_table_id(manager=managers, table_id=table_id)
    await callback_query.answer()
    message_text = markdown.text(
        markdown.hbold("Название:"), data["name"],
        markdown.hbold("Комментарий:"), data["comment"],
        markdown.hbold("Жанр:"), data["genre"],
        sep="\n"
    )
    await callback_query.message.edit_text(
        text=message_text,
        reply_markup=get_serial_details_kb(serial_cb_data=callback_data)
    )


@router.callback_query(
    PaginationCBSerial.filter(F.move == PaginationSerialDirection.next)
)
async def handle_show_next_films_button(
        callback_query: CallbackQuery,
        callback_data: PaginationCBSerial
):
    user_id = int(callback_query.from_user.id)
    serials = await get_serials_by_user(manager=managers, user_id=user_id)
    await callback_query.answer()
    callback_data.pagination = callback_data.pagination + 3
    await callback_query.message.edit_text(
        text="Ещё список твоих сериалов",
        reply_markup=get_serial_list(
            serials=serials, pagination=callback_data.pagination,
            include_back=True
        )
    )


@router.callback_query(
    PaginationCBSerial.filter(F.move == PaginationSerialDirection.back)
)
async def handle_show_previous_films_button(
        callback_query: CallbackQuery,
        callback_data: PaginationCBSerial
):
    user_id = int(callback_query.from_user.id)
    serials = await get_serials_by_user(manager=managers, user_id=user_id)
    await callback_query.answer()
    callback_data.pagination = callback_data.pagination - 3
    include_back = False if callback_data.pagination == 3 else True
    await callback_query.message.edit_text(
        text="Предыдущий список твоих сериалов",
        reply_markup=get_serial_list(
            serials=serials, pagination=callback_data.pagination,
            include_back=include_back
        )
    )
