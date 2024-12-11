from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.utils import markdown
from aiogram.enums import ChatAction

from routers.handlers.states import DocData
from routers.handlers.utils.utils import get_media_from_user
from keyboards.common_keyboards import get_start_kb
from db.db_ import managers
from db.queries import add_document

router = Router(name=__name__)


@router.message(DocData.doc, F.document)
async def handle_add_document_to_doc(message: types.Message, state: FSMContext):
    data = await get_media_from_user(message=message)
    ready_data = await state.update_data(document=data)
    ready_data.update({"user_id": message.from_user.id})
    await state.clear()
    await send_ready_data(message=message, data=ready_data)


async def send_ready_data(message: types.Message, data: dict):
    await add_document(manager=managers, data=data)
    text = markdown.text(
        "Информация о файле:",
        markdown.text("Название файла", markdown.hbold(data["name"])),
        markdown.text("Описание файла", markdown.hbold(data["description"])),
        sep="\n"
    )
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.UPLOAD_DOCUMENT
    )
    await message.reply_document(
        document=types.BufferedInputFile(
            file=data["document"],
            filename=f"{data['name']}"
        ),
        caption=text,
        reply_markup=get_start_kb()
    )


@router.message(DocData.doc)
async def handle_add_document_to_doc(message: types.Message):
    await message.answer(
        text="Отправь файл в сообщении"
    )
