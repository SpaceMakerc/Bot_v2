from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from routers.handlers.states import DocData, next_step_info, TypesOfInformation

router = Router(name=__name__)


@router.message(DocData.name, F.text)
async def handle_add_name_to_doc(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(DocData.description)
    await message.answer(
        text=next_step_info[TypesOfInformation.doc][1]["question_2"],
        reply_markup=types.ReplyKeyboardRemove()
    )


@router.message(DocData.name)
async def handle_add_name_to_doc_invalid_type(message: types.Message):
    await message.answer(
        text="Напиши название файла текстом"
    )
