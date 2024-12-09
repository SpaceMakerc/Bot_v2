from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.utils import markdown

from routers.handlers.states import PictureData
from routers.handlers.utils.utils import get_photo_from_user
from keyboards.common_keyboards import get_start_kb

router = Router(name=__name__)


@router.message(PictureData.picture, F.photo)
async def handle_add_picture_from_user(
        message: types.Message, state: FSMContext
):
    bytes_picture = await get_photo_from_user(message=message)
    data = await state.update_data(picture=bytes_picture)
    await state.clear()
    await send_ready_data(data=data, message=message)


@router.message(PictureData.picture)
async def handle_add_picture_from_user_invalid_type(message: types.Message):
    await message.answer(
        text="Пришли фото или картинку"
    )


async def send_ready_data(data: dict, message: types.Message):
    text = markdown.text(
        "Инфа о картинке",
        markdown.text(
            "Комментарий к картинке:", markdown.hbold(data["comment"])
        ),
        markdown.text("Статус картинки:", markdown.hbold(data["status"])),
        sep="\n"
    )
    await message.reply_document(
        document=types.BufferedInputFile(
            file=data["picture"],
            filename=f"{data['comment']}.jpg"
        ),
        caption=text,
        reply_markup=get_start_kb()
    )
