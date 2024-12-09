from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from routers.handlers.states import (SerialData, TypesOfInformation,
                                     next_step_info)

router = Router(name=__name__)


@router.message(SerialData.name, F.text)
async def handle_add_name_to_serial(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(SerialData.comment)
    await message.answer(
        text=next_step_info[TypesOfInformation.serial][1]["question_2"],
        reply_markup=types.ReplyKeyboardRemove()
    )


@router.message(SerialData.name)
async def handle_add_name_to_serial_invalid_type(message: types.Message):
    await message.answer(
        text="Напиши название сериала текстом"
    )
