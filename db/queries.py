import logging

from sqlalchemy import select
import asyncio

from db.db_ import managers, SessionAsyncContextManager
from db.models import Users, FilmsDate, SerialDate

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
