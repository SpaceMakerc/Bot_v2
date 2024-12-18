import logging
from sqlalchemy import select, update, and_
from sqlalchemy.sql import false, true
from typing import Optional

from db.db_ import AsyncSessionContextManager
from db.models import Users, FilmsDate, SerialDate, PictureData, DocData

logger = logging.getLogger(name=__name__)


async def check_user_exists(manager: AsyncSessionContextManager, data: dict):
    stmt = select(Users.id).where(Users.id == data["id"])
    async with manager:
        query = await manager.session.execute(stmt)
        user = query.one_or_none()
        if user:
            return
    await add_user(manager=manager, data=data)


async def add_user(manager: AsyncSessionContextManager, data: dict):
    try:
        async with manager:
            user = Users(id=data["id"], username=data["username"])
            manager.session.add(user)
            await manager.session.commit()
            logger.info("User %s was added", data["id"])
    except Exception as er:
        logger.warning("User %s was NOT added. Info %s", data["id"], er)


async def add_film(manager: AsyncSessionContextManager, data: dict):
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


async def add_serial(manager: AsyncSessionContextManager, data: dict):
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


async def add_picture(manager: AsyncSessionContextManager, data: dict):
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


async def add_document(manager: AsyncSessionContextManager, data: dict):
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
        manager: AsyncSessionContextManager, user_id: int
) -> Optional[dict]:
    data = dict()
    count = 0
    try:
        async with manager:
            query = select(
                FilmsDate.id.label("id"),
                FilmsDate.name.label("name")
            ).where(and_(
                FilmsDate.user_id == user_id, FilmsDate.is_deleted == false()
            ))
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
        manager: AsyncSessionContextManager, table_id: int
) -> Optional[dict]:
    data = dict()
    try:
        async with manager:
            query = select(
                FilmsDate.name.label("name"),
                FilmsDate.comment.label("comment"),
                FilmsDate.genre.label("genre")
            ).where(and_(
                FilmsDate.id == table_id, FilmsDate.is_deleted == false()
            ))
            db_info = await manager.session.execute(query)
            film = db_info.first()
            if film is None:
                return None
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


async def get_serials_by_user(
        manager: AsyncSessionContextManager,
        user_id: int
):
    data = dict()
    count = 0
    try:
        async with manager:
            query = select(
                SerialDate.id.label("id"),
                SerialDate.name.label("name")
            ).where(and_(
                SerialDate.user_id == user_id, SerialDate.is_deleted == false())
            )
            db_info = await manager.session.execute(query)
            serials = db_info.all()
            if serials is None:
                return None
            for serial in serials:
                data[count] = {
                    "id": serial.id,
                    "name": serial.name
                }
                count += 1
            return data
    except Exception as er:
        logger.warning(f"Exception while getting serial from db. info: %s", er)


async def get_serial_by_table_id(
        manager: AsyncSessionContextManager, table_id: int
):
    data = dict()
    try:
        async with manager:
            query = select(
                SerialDate.name.label("name"),
                SerialDate.comment.label("comment"),
                SerialDate.genre.label("genre")
            ).where(SerialDate.id == table_id)
            db_info = await manager.session.execute(query)
            serial = db_info.first()
            if serial is None:
                return None
            data.update(
                {
                    "name": serial.name,
                    "comment": serial.comment,
                    "genre": serial.genre
                }
            )
            return data
    except Exception as er:
        logger.warning("Exception while getting serial from db. info: %s", er)


async def get_pictures_by_user(
        manager: AsyncSessionContextManager, user_id: int
):
    count = 0
    data = dict()
    try:
        async with manager:
            query = select(
                PictureData.id.label("id"),
                PictureData.comment.label("comment")
            ).where(PictureData.user_id == user_id)
            db_info = await manager.session.execute(query)
            pictures = db_info.all()
            if pictures:
                for picture in pictures:
                    data[count] = {
                        "id": picture.id,
                        "comment": picture.comment
                    }
                    count += 1
            return data
    except Exception as er:
        logger.warning("Exception while getting pictures from db. info: %s", er)


async def get_picture_by_table_id(
        manager: AsyncSessionContextManager,
        table_id: int
):
    data = dict()
    try:
        async with manager:
            query = select(
                PictureData.comment.label("comment"),
                PictureData.status.label("status"),
                PictureData.picture.label("picture")
            ).where(PictureData.id == table_id)
            db_info = await manager.session.execute(query)
            pictures = db_info.all()
            if pictures is None:
                return None
            for picture in pictures:
                data.update(
                    {
                        "comment": picture.comment,
                        "status": picture.status,
                        "picture": picture.picture
                    }
                )
            return data
    except Exception as er:
        logger.warning("Exception while getting picture from db. info: %s", er)


async def get_documents_by_user(
        manager: AsyncSessionContextManager, user_id: int
):
    count = 0
    data = dict()
    try:
        async with manager:
            query = select(
                DocData.id.label("id"),
                DocData.name.label("name")
            ).where(DocData.user_id == user_id)
            db_info = await manager.session.execute(query)
            documents = db_info.all()
            if documents:
                for doc in documents:
                    data[count] = {
                        "id": doc.id,
                        "name": doc.name
                    }
                    count += 1
            return data
    except Exception as er:
        logger.warning("Exception while getting documents from db. info: %s",
                       er)


async def get_document_by_table_id(
        manager: AsyncSessionContextManager,
        table_id: int
):
    data = dict()
    try:
        async with manager:
            query = select(
                DocData.name.label("name"),
                DocData.description.label("description"),
                DocData.document.label("document")
            ).where(DocData.id == table_id)
            db_info = await manager.session.execute(query)
            documents = db_info.all()
            if documents is None:
                return None
            for doc in documents:
                data.update(
                    {
                        "name": doc.name,
                        "description": doc.description,
                        "document": doc.document
                    }
                )
            return data
    except Exception as er:
        logger.warning("Exception while getting document from db. info: %s", er)


async def remove_film_by_table_id(
        manager: AsyncSessionContextManager,
        table_id: int
):
    try:
        async with manager:
            query = update(FilmsDate).where(
                FilmsDate.id == table_id
            ).values(
                is_deleted=true()
            ).returning(FilmsDate)
            db_info = await manager.session.execute(query)
            film = db_info.scalars().first()
            await manager.session.commit()
            logger.info("Film %s was deleted", table_id)
            return film
    except Exception as er:
        logger.warning("Film %s was NOT deleted. INFO - %s", table_id, er)


async def remove_serial_by_table_id(
        manager: AsyncSessionContextManager,
        table_id: int
):
    try:
        async with manager:
            query = update(SerialDate).where(
                SerialDate.id == table_id
            ).values(
                is_deleted=true()
            ).returning(SerialDate)
            db_info = await manager.session.execute(query)
            film = db_info.scalars().first()
            await manager.session.commit()
            logger.info("Serial %s was deleted", table_id)
            return film
    except Exception as er:
        logger.warning("Serial %s was NOT deleted. INFO - %s", table_id, er)
