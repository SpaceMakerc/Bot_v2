from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from routers.handlers.states import (PictureData, PictureStatus, next_step_info,
                                     TypesOfInformation)
from keyboards.common_keyboards import get_picture_status_kb

router = Router(name=__name__)


@router.message(PictureData.status, F.text.cast(PictureStatus))
async def handle_add_status_to_picture(
        message: types.Message, state: FSMContext
):
    await state.update_data(status=message.text)
    await state.set_state(PictureData.picture)
    await message.answer(
        text=next_step_info[TypesOfInformation.picture][1]["question_3"],
        reply_markup=types.ReplyKeyboardRemove()
    )


@router.message(PictureData.status)
async def handle_add_status_to_picture_invalid(message: types.Message):
    await message.answer(
        text="Выбери из вариантов ниже",
        reply_markup=get_picture_status_kb()
    )
