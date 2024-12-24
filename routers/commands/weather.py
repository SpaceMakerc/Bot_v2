from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.utils import markdown

from keyboards.button_information import StartButtonNames
from keyboards.common_keyboards import get_start_kb
from routers.utils.weather_handler import share_weather

router = Router(name=__name__)


@router.message(Command("weather", prefix="/"))
@router.message(F.text == StartButtonNames.weather)
async def handle_weather_command(message: types.Message):
    data = await share_weather()
    await message.answer(
        text=markdown.text(
            markdown.hbold("Погода сегодня"),
            f"Температура: {data['temp']}\n"
            f"Ощущается как: {data['feel_like']}\n"
            f"Ветер: {data['wind']}\n"
            f"Описание: {data['desc']}\n",
            sep="\n"
        ),
        reply_markup=get_start_kb()
    )
