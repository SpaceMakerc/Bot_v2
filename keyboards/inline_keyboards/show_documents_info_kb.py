from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboards.inline_keyboards.inline_button_information import (
    ShowCategory,
    ShowCBData,
    MediaAction,
    DocumentCBData,
    PaginationDocumentDirection,
    PaginationCBDocument
)


def get_documents_list(
        documents, pagination: int = 3, include_back: bool = False
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="В исходное меню",
        callback_data=ShowCBData(
            category=ShowCategory.root,
        )
    )
    for doc in documents:
        if pagination > doc > pagination - 4:
            builder.button(
                text=documents[doc]["name"],
                callback_data=DocumentCBData(
                    action=MediaAction.details,
                    id=documents[doc]["id"],
                    pagination=pagination
                )
            )
    if include_back:
        builder.button(
            text="Назад",
            callback_data=PaginationCBDocument(
                move=PaginationDocumentDirection.back,
                pagination=pagination
            ).pack()
        )
    if len(documents) > pagination:
        builder.button(
            text="Следующие",
            callback_data=PaginationCBDocument(
                move=PaginationDocumentDirection.next,
                pagination=pagination
            ).pack()
        )

    builder.adjust(1)
    return builder.as_markup()


def get_document_details_kb(
        doc_cb_data: DocumentCBData
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Вернуться к списку документов",
        callback_data=ShowCBData(
            category=ShowCategory.doc,
            pagination=doc_cb_data.pagination
        )
    )
    builder.button(
        text="Удалить документ",
        callback_data=DocumentCBData(
            id=doc_cb_data.id,
            action=MediaAction.remove,
            pagination=doc_cb_data.pagination
        )
    )
    builder.adjust(1)

    return builder.as_markup()
