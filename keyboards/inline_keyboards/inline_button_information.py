from aiogram.filters.callback_data import CallbackData

from enum import Enum


class ShowCategory(Enum):
    film = "Фильм"
    serial = "Сериал"
    picture = "Картинка"
    doc = "Документ"
    root = "Исходное меню"


class ShowCBData(CallbackData, prefix="category"):
    category: ShowCategory


class FilmActions(Enum):
    details = "Детали"
    remove = "Удалить"


class FilmCDData(CallbackData, prefix="films"):
    action: FilmActions
    id: int
    name: str


class PaginationDirection(Enum):
    next = "Следующие"
    back = "Предыдущие"


class PaginationCBFilm(CallbackData, prefix="film_pag"):
    move: PaginationDirection
    pagination: int
