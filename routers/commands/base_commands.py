from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command
from aiogram.utils import markdown

from keyboards.common_keyboards import get_start_kb
from keyboards.button_information import StartButtonNames
from db.db_ import managers
from db.queries import check_user_exists

router = Router(name=__name__)


@router.message(CommandStart())
async def handle_start_command(message: types.Message):
    data = {
        "id": message.from_user.id,
        "username": message.from_user.full_name
    }
    await check_user_exists(manager=managers, data=data)
    await message.answer(
        text=markdown.text(
            markdown.text(
                "Привет,",
                markdown.hbold(message.from_user.full_name),
                "👋"
            ),
            "Как я могу тебе помочь?",
            sep="\n"
        ),
        reply_markup=get_start_kb()
    )


@router.message(F.text == StartButtonNames.help)
@router.message(Command("help", prefix="/"))
async def handle_help_command(message: types.Message):
    await message.answer(
        text="Это бот, который может сохранить информацию для тебя. "
             "Например фильм, аудио, файл, фразу...\nА также могу показать "
             "погоду",
        reply_markup=get_start_kb()
    )
