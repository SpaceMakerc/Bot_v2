from aiogram import Router, F, types
from aiogram.filters.callback_data import CallbackQuery
from aiogram.utils import markdown

from keyboards.inline_keyboards.inline_button_information import (
    ShowCategory,
    ShowCBData,
    MediaAction,
    PictureCBData,
    PaginationCBPicture,
    PaginationPictureDirection
)
from db.db_ import managers
from db.queries import (
    get_pictures_by_user,
    get_picture_by_table_id,
    remove_picture_by_table_id
)
from keyboards.inline_keyboards.show_pictures_info_kb import (
    get_pictures_list,
    get_picture_details_kb
)
from routers.utils.utils import return_media_to_user, check_button_back

router = Router(name=__name__)


@router.callback_query(ShowCBData.filter(F.category == ShowCategory.picture))
async def handle_show_picture_button(
        callback_query: CallbackQuery,
        callback_data: ShowCBData
):
    user_id = int(callback_query.from_user.id)
    pictures = await get_pictures_by_user(manager=managers, user_id=user_id)
    await callback_query.answer()
    include_back = check_button_back(callback_data.pagination)

    if pictures:
        if callback_data.pagination is None:
            await callback_query.message.edit_text(
                text="Список твоих картинок",
                reply_markup=get_pictures_list(
                    pictures=pictures, include_back=include_back
                )
            )
        else:
            await callback_query.message.edit_text(
                text="Список твоих картинок",
                reply_markup=get_pictures_list(
                    pictures=pictures, include_back=include_back,
                    pagination=callback_data.pagination
                )
            )
    else:
        await callback_query.message.answer(
            text="У тебя ещё нет сохранённых картинок. Для того чтобы добавить"
                 " картинку, жми на /start или /survey и сохрани что-нибудь"
        )


@router.callback_query(PictureCBData.filter(F.action == MediaAction.details))
async def handle_show_picture_detail_button(
        callback_query: CallbackQuery,
        callback_data: PictureCBData
):
    table_id = callback_data.id
    data = await get_picture_by_table_id(manager=managers, table_id=table_id)
    await callback_query.answer()
    caption = markdown.text(
        markdown.hbold("Комментарий:"), data["comment"],
        markdown.hbold("Статус:"), data["status"],
        sep="\n"
    )
    picture = await return_media_to_user(bytes(data["picture"]))
    await callback_query.message.reply_document(
        document=types.BufferedInputFile(
            file=picture.getvalue(),
            filename=f"{data['comment']}.jpg"
        ),
        caption=caption,
    )
    await callback_query.message.answer(
        text=caption,
        reply_markup=get_picture_details_kb(picture_cb_data=callback_data)
    )


@router.callback_query(
    PaginationCBPicture.filter(F.move == PaginationPictureDirection.next)
)
async def handle_show_next_pictures_button(
        callback_query: CallbackQuery,
        callback_data: PaginationCBPicture
):
    user_id = int(callback_query.from_user.id)
    pictures = await get_pictures_by_user(manager=managers, user_id=user_id)
    await callback_query.answer()
    callback_data.pagination = callback_data.pagination + 3
    await callback_query.message.edit_text(
        text="Ещё список твоих картинок",
        reply_markup=get_pictures_list(
            pictures=pictures, pagination=callback_data.pagination,
            include_back=True
        )
    )


@router.callback_query(
    PaginationCBPicture.filter(F.move == PaginationPictureDirection.back)
)
async def handle_show_previous_pictures_button(
        callback_query: CallbackQuery,
        callback_data: PaginationCBPicture
):
    user_id = int(callback_query.from_user.id)
    pictures = await get_pictures_by_user(manager=managers, user_id=user_id)
    await callback_query.answer()
    callback_data.pagination = callback_data.pagination - 3
    include_back = check_button_back(callback_data.pagination)
    await callback_query.message.edit_text(
        text="Предыдущий список твоих картинок",
        reply_markup=get_pictures_list(
            pictures=pictures, pagination=callback_data.pagination,
            include_back=include_back
        )
    )


@router.callback_query(PictureCBData.filter(F.action == MediaAction.remove))
async def handle_remove_picture_button(
        callback_query: CallbackQuery,
        callback_data: PictureCBData
):
    picture = await remove_picture_by_table_id(
        manager=managers, table_id=callback_data.id
    )
    user_id = int(callback_query.from_user.id)
    await callback_query.answer(
        text=f"Картинка {picture.comment} удалён",
        show_alert=True,
    )
    pictures = await get_pictures_by_user(manager=managers, user_id=user_id)
    include_back = check_button_back(callback_data.pagination)
    await callback_query.message.answer(
        text=f"Список твоих картинок",
        reply_markup=get_pictures_list(
            pictures=pictures, pagination=callback_data.pagination,
            include_back=include_back
        )
    )
