from sqlalchemy.ext.asyncio import (create_async_engine, async_sessionmaker)

from src.core import settings

engine = create_async_engine(url=settings.get_async_url())

async_session_maker = async_sessionmaker(
    bind=engine, autocommit=False, autoflush=False, expire_on_commit=False
)


class SessionAsyncContextManager:
    def __init__(self) -> None:
        self.session_factory = async_session_maker
        self.session = None

    async def __aenter__(self) -> None:
        self.session = self.session_factory()

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type is None:
            await self.session.commit()
        else:
            await self.session.rollback()

    # async def __aexit__(self, *args: object) -> None:
    #     await self.rollback()

    async def commit(self) -> None:
        await self.session.commit()
        await self.session.close()
        self.session = None

    async def rollback(self) -> None:
        await self.session.rollback()
        await self.session.close()
        self.session = None


managers = SessionAsyncContextManager()
