from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from routers.handlers.states import (SerialData, next_step_info,
                                     TypesOfInformation)
from keyboards.common_keyboards import get_genre_options_kb

router = Router(name=__name__)


@router.message(SerialData.comment, F.text)
async def handle_add_comment_to_serial(
        message: types.Message, state: FSMContext
):
    await state.update_data(comment=message.text)
    await state.set_state(SerialData.genre)
    await message.answer(
        text=next_step_info[TypesOfInformation.serial][1]["question_3"],
        reply_markup=get_genre_options_kb(TypesOfInformation.serial)
    )


@router.message(SerialData.comment)
async def handle_add_comment_to_serial_invalid_type(message: types.Message):
    await message.answer(
        text="Напши комментарий текстом",
    )
