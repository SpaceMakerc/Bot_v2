from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from routers.handlers.states import DocData, next_step_info, TypesOfInformation

router = Router(name=__name__)


@router.message(DocData.description, F.text)
async def handle_add_description_to_doc(
        message: types.Message, state: FSMContext
):
    await state.update_data(description=message.text)
    await state.set_state(DocData.doc)
    await message.answer(
        text=next_step_info[TypesOfInformation.doc][1]["question_3"]
    )


@router.message(DocData.description)
async def handle_add_description_to_doc_invalid_type(message: types.Message):
    await message.answer(
        text="Добавь описание текстом"
    )
