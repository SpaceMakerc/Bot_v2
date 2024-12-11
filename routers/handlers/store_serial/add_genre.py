from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.utils import markdown

from routers.handlers.states import (SerialData, GenreName, TypesOfInformation)
from keyboards.common_keyboards import get_start_kb, get_genre_options_kb
from db.queries import add_serial
from db.db_ import managers

router = Router(name=__name__)


@router.message(SerialData.genre, F.text.cast(GenreName))
async def handle_add_genre_to_serial(message: types.Message, state: FSMContext):
    ready_data = await state.update_data(genre=message.text)
    ready_data.update({"user_id": message.from_user.id})
    await state.clear()
    await send_ready_data(data=ready_data, message=message)


async def send_ready_data(data: dict, message: types.Message):
    await add_serial(manager=managers, data=data)
    text = markdown.text(
        "Информация по сериалу",
        markdown.text("Наименование сериала:", markdown.hbold(data["name"])),
        markdown.text(
            "Комментарий к сериалу:", markdown.hbold(data["comment"])
        ),
        markdown.text("Жанр сериала:", markdown.hbold(data["genre"])),
        sep="\n",
    )
    await message.answer(
        text=text,
        reply_markup=get_start_kb()
    )


@router.message(SerialData.genre)
async def handle_add_genre_to_serial(message: types.Message):
    await message.answer(
        text="Выбери из имеющихся вариантов жанр сериала",
        reply_markup=get_genre_options_kb(TypesOfInformation.serial)
    )
