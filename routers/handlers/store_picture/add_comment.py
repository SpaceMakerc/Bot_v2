from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from routers.handlers.states import (PictureData, next_step_info,
                                     TypesOfInformation)
from keyboards.common_keyboards import get_picture_status_kb

router = Router(name=__name__)


@router.message(PictureData.comment, F.text)
async def handle_add_comment_to_picture(
        message: types.Message, state: FSMContext
):
    await state.update_data(comment=message.text)
    await state.set_state(PictureData.status)
    await message.answer(
        text=next_step_info[TypesOfInformation.picture][1]["question_2"],
        reply_markup=get_picture_status_kb()
    )


@router.message(PictureData.comment)
async def handle_add_comment_to_picture_invalid_type(message: types.Message):
    await message.answer(
        text="Напиши комментарий к картинке текстом"
    )
