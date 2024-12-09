from aiogram.fsm.state import StatesGroup, State
from enum import Enum
from typing import Union

from routers.handlers.utils.utils import get_questions_to_states


class StartSurveyOptions(StatesGroup):
    type = State()


class FilmData(StatesGroup):
    name = State()
    comment = State()
    genre = State()


class SerialData(StatesGroup):
    name = State()
    comment = State()
    genre = State()


class PictureData(StatesGroup):
    name = State()
    comment = State()
    genre = State()


class DocData(StatesGroup):
    name = State()
    comment = State()
    genre = State()


class CancelSurvey(StatesGroup):
    type_survey = StartSurveyOptions
    film_survey = FilmData
    serial_survey = SerialData
    picture_survey = PictureData
    doc_survey = DocData


class TypesOfInformation(str, Enum):
    film = "Фильм"
    serial = "Сериал"
    picture = "Картинка"
    doc = "Документ"


class GenreName(str, Enum):
    comedy = "Комедия"
    horror = "Ужасы"
    drama = "Драма"
    fantastic = "Фантастика"
    fantasy = "Фэнтези"
    adventures = "Приключения"
    sit_com = "Сит ком"


question_data = get_questions_to_states()

next_step_info: dict[Union[TypesOfInformation, str],
                     tuple[State, dict]] = {
    TypesOfInformation.film: (
        FilmData.name, question_data[TypesOfInformation.film]),
    TypesOfInformation.serial: (
        SerialData.name, question_data[TypesOfInformation.serial]),
        # TypesOfInformation.picture: (
        #     PictureData.name, question_data[TypesOfInformation.picture]),
        # TypesOfInformation.doc: (
        #     DocData.name, question_data[TypesOfInformation.doc]),
    }
