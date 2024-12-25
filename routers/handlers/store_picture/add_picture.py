from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.utils import markdown
from aiogram.enums import ChatAction

from routers.handlers.states import PictureData
from routers.utils.utils import get_media_from_user
from keyboards.common_keyboards import get_start_kb
from db.db_ import managers
from db.queries import add_picture

router = Router(name=__name__)


@router.message(PictureData.picture, F.photo)
async def handle_add_picture_from_user(
        message: types.Message, state: FSMContext
):
    bytes_picture = await get_media_from_user(message=message)
    data = await state.update_data(picture=bytes_picture)
    data.update({"user_id": message.from_user.id})
    await state.clear()
    await send_ready_data(data=data, message=message)


@router.message(PictureData.picture)
async def handle_add_picture_from_user_invalid_type(message: types.Message):
    await message.answer(
        text="Пришли фото или картинку"
    )


async def send_ready_data(data: dict, message: types.Message):
    await add_picture(manager=managers, data=data)
    text = markdown.text(
        "Информация о картинке",
        markdown.text(
            "Комментарий к картинке:", markdown.hbold(data["comment"])
        ),
        markdown.text("Статус картинки:", markdown.hbold(data["status"])),
        sep="\n"
    )
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.UPLOAD_DOCUMENT
    )
    await message.reply_document(
        document=types.BufferedInputFile(
            file=data["picture"],
            filename=f"{data['comment']}.jpg"
        ),
        caption=text,
        reply_markup=get_start_kb()
    )
