from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.utils import markdown

from routers.handlers.states import DocData
from routers.handlers.utils.utils import get_media_from_user
from keyboards.common_keyboards import get_start_kb

router = Router(name=__name__)


@router.message(DocData.doc, F.document)
async def handle_add_document_to_doc(message: types.Message, state: FSMContext):
    data = await get_media_from_user(message=message)
    ready_data = await state.update_data(document=data)
    await state.clear()
    await send_ready_data(message=message, data=ready_data)


async def send_ready_data(message: types.Message, data: dict):
    text = markdown.text(
        "Информация о файле:",
        markdown.text("Название файла", markdown.hbold(data["name"])),
        markdown.text("Описание файла", markdown.hbold(data["description"])),
        sep="\n"
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
