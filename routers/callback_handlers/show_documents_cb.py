from aiogram import Router, F, types
from aiogram.types import CallbackQuery
from aiogram.utils import markdown

from keyboards.inline_keyboards.inline_button_information import (
    ShowCategory,
    ShowCBData,
    DocumentCBData,
    MediaAction,
    PaginationCBDocument,
    PaginationDocumentDirection
)
from keyboards.inline_keyboards.show_documents_info_kb import (
    get_documents_list,
    get_document_details_kb
)
from db.db_ import managers
from db.queries import get_documents_by_user, get_document_by_table_id
from routers.handlers.utils.utils import check_button_back, return_media_to_user

router = Router(name=__name__)


@router.callback_query(ShowCBData.filter(F.category == ShowCategory.doc))
async def handle_show_doc_button(
        callback_query: CallbackQuery,
        callback_data: ShowCBData
):
    user_id = int(callback_query.from_user.id)
    documents = await get_documents_by_user(manager=managers, user_id=user_id)
    await callback_query.answer()
    include_back = check_button_back(callback_data.pagination)

    if documents:
        if callback_data.pagination is None:
            await callback_query.message.edit_text(
                text="Список твоих документов",
                reply_markup=get_documents_list(
                    documents=documents, include_back=include_back
                )
            )
        else:
            await callback_query.message.edit_text(
                text="Список твоих документов",
                reply_markup=get_documents_list(
                    documents=documents, include_back=include_back,
                    pagination=callback_data.pagination
                )
            )
    else:
        await callback_query.message.answer(
            text="У тебя ещё нет сохранённых документов. Для того чтобы "
                 "добавить документ, жми на /start или /survey и сохрани "
                 "что-нибудь"
        )


@router.callback_query(DocumentCBData.filter(F.action == MediaAction.details))
async def handle_show_document_detail_button(
        callback_query: CallbackQuery,
        callback_data: DocumentCBData
):
    table_id = callback_data.id
    data = await get_document_by_table_id(manager=managers, table_id=table_id)
    await callback_query.answer()
    caption = markdown.text(
        markdown.hbold("Название:"), data["name"],
        markdown.hbold("Описание:"), data["description"],
        sep="\n"
    )
    document = await return_media_to_user(bytes(data["document"]))
    await callback_query.message.reply_document(
        document=types.BufferedInputFile(
            file=document.getvalue(),
            filename=f"{data['name']}"
        ),
        caption=caption,
    )
    await callback_query.message.answer(
        text=caption,
        reply_markup=get_document_details_kb(doc_cb_data=callback_data)
    )


@router.callback_query(
    PaginationCBDocument.filter(F.move == PaginationDocumentDirection.next)
)
async def handle_show_next_document_button(
        callback_query: CallbackQuery,
        callback_data: PaginationCBDocument
):
    user_id = int(callback_query.from_user.id)
    documents = await get_documents_by_user(manager=managers, user_id=user_id)
    await callback_query.answer()
    callback_data.pagination = callback_data.pagination + 3
    await callback_query.message.edit_text(
        text="Ещё список твоих документов",
        reply_markup=get_documents_list(
            documents=documents, pagination=callback_data.pagination,
            include_back=True
        )
    )


@router.callback_query(
    PaginationCBDocument.filter(F.move == PaginationDocumentDirection.back)
)
async def handle_show_previous_document_button(
        callback_query: CallbackQuery,
        callback_data: PaginationCBDocument
):
    user_id = int(callback_query.from_user.id)
    documents = await get_documents_by_user(manager=managers, user_id=user_id)
    await callback_query.answer()
    callback_data.pagination = callback_data.pagination - 3
    include_back = check_button_back(callback_data.pagination)
    await callback_query.message.edit_text(
        text="Предыдущий список твоих документов",
        reply_markup=get_documents_list(
            documents=documents, pagination=callback_data.pagination,
            include_back=include_back
        )
    )
