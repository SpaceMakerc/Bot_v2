from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from routers.handlers.states import FilmData, next_step_info, TypesOfInformation
from keyboards.common_keyboards import get_genre_options_kb

router = Router(name=__name__)


@router.message(FilmData.comment, F.text)
async def handle_add_comment_to_film(message: types.Message, state: FSMContext):
    await state.update_data(comment=message.text)
    await state.set_state(FilmData.genre)
    await message.answer(
        text=next_step_info[TypesOfInformation.film][1]["question_3"],
        reply_markup=get_genre_options_kb()
    )


@router.message(FilmData.comment)
async def handle_add_comment_to_film_invalid_type(message: types.Message):
    await message.answer(
        text="Напиши комментарий текстом"
    )
