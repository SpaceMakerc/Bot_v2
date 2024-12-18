from aiogram.filters.callback_data import CallbackData

from enum import Enum
from typing import Union


class ShowCategory(Enum):
    film = "Фильм"
    serial = "Сериал"
    picture = "Картинка"
    doc = "Документ"
    root = "Исходное меню"


class ShowCBData(CallbackData, prefix="category"):
    category: ShowCategory
    pagination: Union[None, int] = None


class MediaAction(Enum):
    details = "Детали"
    remove = "Удалить"


class FilmCDData(CallbackData, prefix="films"):
    action: MediaAction
    id: int
    pagination: Union[None, int]


class PaginationFilmDirection(Enum):
    next = "Следующие"
    back = "Предыдущие"


class PaginationCBFilm(CallbackData, prefix="film_pag"):
    move: PaginationFilmDirection
    pagination: int


class SerialCBData(CallbackData, prefix="serials"):
    action: MediaAction
    id: int
    pagination: Union[None, int]


class PaginationSerialDirection(Enum):
    next = "Следующие"
    back = "Предыдущие"


class PaginationCBSerial(CallbackData, prefix="serial_pag"):
    move: PaginationSerialDirection
    pagination: int


class PictureCBData(CallbackData, prefix="pictures"):
    action: MediaAction
    id: int
    name: str
    pagination: Union[None, int]


class PaginationPictureDirection(Enum):
    next = "Следующие"
    back = "Предыдущие"


class PaginationCBPicture(CallbackData, prefix="picture_pag"):
    move: PaginationPictureDirection
    pagination: int


class DocumentCBData(CallbackData, prefix="documents"):
    action: MediaAction
    id: int
    name: str
    pagination: Union[None, int]


class PaginationDocumentDirection(Enum):
    next = "Следующие"
    back = "Предыдущие"


class PaginationCBDocument(CallbackData, prefix="document_pag"):
    move: PaginationDocumentDirection
    pagination: int
