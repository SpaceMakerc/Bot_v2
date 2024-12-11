from sqlalchemy import MetaData, func, String, ForeignKey, Text, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import Annotated
from datetime import datetime
from enum import Enum

metadata = MetaData()

created_at = Annotated[datetime, mapped_column(server_default=func.now())]


class Base(DeclarativeBase):
    metadata = metadata


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    created_at: Mapped[created_at]

    films: Mapped[list["FilmsDate"]] = relationship(
        back_populates="user"
    )


class GenreFilms(str, Enum):
    comedy = "Комедия"
    horror = "Ужасы"
    drama = "Драма"
    fantastic = "Фантастика"
    fantasy = "Фэнтези"
    adventures = "Приключения"
    sit_com = "Сит ком"


class FilmsDate(Base):
    __tablename__ = "user_films"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )
    name: Mapped[str] = mapped_column(String(100))
    comment: Mapped[str] = mapped_column(Text, nullable=True)
    genre: Mapped[GenreFilms] = mapped_column(
        default=GenreFilms.adventures
    )

    user: Mapped["Users"] = relationship(
        back_populates="films"
    )
