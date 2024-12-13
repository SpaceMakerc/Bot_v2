import logging
from sqlalchemy import select
from typing import Optional

from db.db_ import SessionAsyncContextManager
from db.models import Users, FilmsDate, SerialDate, PictureData, DocData

logger = logging.getLogger(name=__name__)


async def check_user_exists(manager: SessionAsyncContextManager, data: dict):
    stmt = select(Users.id).where(Users.id == data["id"])
    async with manager:
        query = await manager.session.execute(stmt)
        user = query.one_or_none()
        if user:
            return
    await add_user(manager=manager, data=data)


async def add_user(manager: SessionAsyncContextManager, data: dict):
    try:
        async with manager:
            user = Users(id=data["id"], username=data["username"])
            manager.session.add(user)
            await manager.session.commit()
            logger.info("User %s was added", data["id"])
    except Exception as er:
        logger.warning("User %s was NOT added. Info %s", data["id"], er)


async def add_film(manager: SessionAsyncContextManager, data: dict):
    # TODO add checking on films in database in order to not add the same
    try:
        async with manager:
            film = FilmsDate(
                user_id=data["user_id"], name=data["name"],
                comment=data["comment"], genre=data["genre"]
            )
            manager.session.add(film)
            await manager.session.commit()
            logger.info(
                "Film: %s was added to %s", data["name"], data["user_id"]
            )
    except Exception as er:
        logger.warning(
            "Film %s was NOT added to %s. Info %s", data["name"],
            data["user_id"], er
        )


async def add_serial(manager: SessionAsyncContextManager, data: dict):
    try:
        async with manager:
            serial = SerialDate(
                user_id=data["user_id"], name=data["name"],
                comment=data["comment"], genre=data["genre"]
            )
            manager.session.add(serial)
            await manager.session.commit()
            logger.info(
                "Serial %s was added to %s", data["name"], data["user_id"]
            )
    except Exception as er:
        logging.warning(
            "Serial %s was NOT added to %s. Info %s", data["name"],
            data["user_id"], er
        )


async def add_picture(manager: SessionAsyncContextManager, data: dict):
    try:
        async with manager:
            picture = PictureData(
                user_id=data["user_id"], comment=data["comment"],
                status=data["status"], picture=data["picture"]
            )
            manager.session.add(picture)
            await manager.session.commit()
            logger.info(
                "Picture %s was added to %s", data["status"], data["user_id"]
            )
    except Exception as er:
        logger.warning(
            "Picture %s was NOT added to %s. Info %s", data["status"],
            data["user_id"], er
        )


async def add_document(manager: SessionAsyncContextManager, data: dict):
    try:
        async with manager:
            document = DocData(
                user_id=data["user_id"], name=data["name"],
                description=data["description"], document=data["document"]
            )
            manager.session.add(document)
            await manager.session.commit()
            logger.info(
                "Document %s was added to %s", data["name"], data["user_id"]
            )
    except Exception as er:
        logger.warning(
            "Document %s was NOT added to %s. Info %s", data["name"],
            data["user_id"], er
        )


async def get_user_films_by_user(
        manager: SessionAsyncContextManager, user_id: int
) -> Optional[dict]:
    data = dict()
    count = 0
    try:
        async with manager:
            query = select(
                FilmsDate.id.label("id"),
                FilmsDate.name.label("name")
            ).where(FilmsDate.user_id == user_id)
            db_info = await manager.session.execute(query)
            films = db_info.all()
            if films is None:
                return None
            for film in films:
                data[count] = {
                    "id": film.id,
                    "name": film.name,
                }
                count += 1
        return data
    except Exception as er:
        logger.warning("Exception while getting films from db. info: %s", er)


async def get_user_film_by_table_id(
        manager: SessionAsyncContextManager, table_id: int
) -> Optional[dict]:
    data = dict()
    try:
        async with manager:
            query = select(
                FilmsDate.name.label("name"),
                FilmsDate.comment.label("comment"),
                FilmsDate.genre.label("genre")
            ).where(FilmsDate.id == table_id)
            db_info = await manager.session.execute(query)
            films = db_info.all()
            if films is None:
                return None
            for film in films:
                data.update(
                    {
                        "name": film.name,
                        "comment": film.comment,
                        "genre": film.genre
                    }
                )
        return data
    except Exception as er:
        logger.warning("Exception while getting films from db. info: %s", er)
