from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.utils import markdown

from routers.handlers.states import FilmData, GenreFilmName
from keyboards.common_keyboards import get_start_kb, get_genre_options_kb

router = Router(name=__name__)


@router.message(FilmData.genre, F.text.cast(GenreFilmName))
async def handle_add_genre_to_film(message: types.Message, state: FSMContext):
    ready_data = await state.update_data(genre=message.text)
    await state.clear()
    await send_ready_data(message=message, ready_data=ready_data)


async def send_ready_data(message: types.Message, ready_data) -> None:
    text = markdown.text(
        "Информация о фильме:",
        markdown.text(
            "Наименование фильма:",markdown.hbold(ready_data["name"])),
        markdown.text(
            "Комментарий к фильму:",markdown.hbold(ready_data["comment"])),
        markdown.text(
            "Жанр фильма:",markdown.hbold(ready_data["genre"])),
        sep="\n"
        )
    await message.answer(
        text=text,
        reply_markup=get_start_kb()
    )


@router.message(FilmData.genre)
async def handle_add_genre_to_film_invalid_type(message: types.Message):
    await message.answer(
        text="Выбери из имеющихся вариантов",
        reply_markup=get_genre_options_kb()
    )
