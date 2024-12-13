from sqlalchemy import MetaData, func, String, ForeignKey, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import BYTEA, ENUM
from typing import Annotated
from datetime import datetime
from enum import Enum

metadata = MetaData()

created_at = Annotated[datetime, mapped_column(server_default=func.now())]


class GenreFilms(Enum):
    comedy = "Комедия"
    horror = "Ужасы"
    drama = "Драма"
    fantastic = "Фантастика"
    fantasy = "Фэнтези"
    adventures = "Приключения"

    def __str__(self):
        return self.value


class GenreSerials(Enum):
    comedy = "Комедия"
    horror = "Ужасы"
    drama = "Драма"
    fantastic = "Фантастика"
    fantasy = "Фэнтези"
    adventures = "Приключения"
    sit_com = "Сит ком"

    def __str__(self):
        return self.value


class PictureGenre(str, Enum):
    plain = "Обычная"
    special = "Важная"

    def __str__(self):
        return self.value


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
    serials: Mapped[list["SerialDate"]] = relationship(
        back_populates="user"
    )
    pictures: Mapped[list["PictureData"]] = relationship(
        back_populates="user"
    )
    documents: Mapped[list["DocData"]] = relationship(
        back_populates="user"
    )


class FilmsDate(Base):
    __tablename__ = "user_films"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )
    name: Mapped[str] = mapped_column(String(100))
    comment: Mapped[str] = mapped_column(Text, nullable=True)
    genre: Mapped[GenreFilms] = mapped_column(
        ENUM(
            GenreFilms, create_type=False, name="filmsgenres",
            values_callable=lambda e: [field.value for field in e]
        ),
        nullable=False, default=GenreFilms.adventures
    )
    user: Mapped["Users"] = relationship(
        back_populates="films"
    )


class SerialDate(Base):
    __tablename__ = "user_serials"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )
    name: Mapped[str] = mapped_column(String(100))
    comment: Mapped[str] = mapped_column(Text, nullable=True)
    genre: Mapped[GenreSerials] = mapped_column(
        ENUM(
            GenreSerials, create_type=False, name="serialsgenres",
            values_callable=lambda e: [field.value for field in e]
        ),
        default=GenreSerials.sit_com, nullable=False
    )

    user: Mapped[Users] = relationship(
        back_populates="serials"
    )


class PictureData(Base):
    __tablename__ = "user_pictures"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )
    comment: Mapped[str] = mapped_column(Text, nullable=True)
    status: Mapped[PictureGenre] = mapped_column(
        ENUM(
            PictureGenre, create_type=False, name="picturesgenres",
            values_callable=lambda e: [field.value for field in e]
        ),
        default=PictureGenre.plain, nullable=False
    )
    picture: Mapped[bytes] = mapped_column(type_=BYTEA)

    user: Mapped["Users"] = relationship(
        back_populates="pictures"
    )


class DocData(Base):
    __tablename__ = "user_documents"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey(
        "users.id", ondelete="CASCADE")
    )
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(Text)
    document: Mapped[bytes] = mapped_column(type_=BYTEA)

    user: Mapped["Users"] = relationship(
        back_populates="documents"
    )
