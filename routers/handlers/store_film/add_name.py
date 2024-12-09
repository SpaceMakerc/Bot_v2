from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from routers.handlers.states import FilmData, next_step_info, TypesOfInformation

router = Router(name=__name__)


@router.message(FilmData.name, F.text)
async def handle_add_name_to_film(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(FilmData.comment)
    await message.answer(
        text=next_step_info[TypesOfInformation.film][1]["question_2"],
        reply_markup=types.ReplyKeyboardRemove()
    )


@router.message(FilmData.name)
async def handle_add_name_to_film_invalid_type(message: types.Message):
    await message.reply(
        text="Напиши название фильма текстом"
    )
