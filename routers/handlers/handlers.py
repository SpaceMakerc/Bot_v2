from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from aiogram.utils import markdown

from keyboards.button_information import StartButtonNames
from keyboards.common_keyboards import get_store_kb
from .states import StartSurveyOptions, TypesOfInformation, next_step_info

router = Router(name=__name__)


@router.message(Command("survey", prefix="/"), default_state)
@router.message(F.text == StartButtonNames.survey, default_state)
async def handle_start_survey(message: types.Message, state: FSMContext):
    await state.set_state(StartSurveyOptions.type)
    await message.answer(
        text="Хорошо, давай сохраним твою информацию. Сначала выбери "
             f"{markdown.hbold('тип данных')}:",
        reply_markup=get_store_kb()
    )


@router.message(StartSurveyOptions.type, F.text.cast(TypesOfInformation))
async def handle_type_of_information(message: types.Message, state: FSMContext):
    await state.update_data(type=message.text)
    next_step, question = next_step_info[message.text]
    await state.set_state(next_step)
    await message.answer(
        text=question['question_1']
    )
