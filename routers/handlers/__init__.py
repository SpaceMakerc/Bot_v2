from aiogram import Router

from routers.handlers.store_film import router as store_films_router
from routers.handlers.handlers import router as handler_router

router = Router(name=__name__)

router.include_routers(
    handler_router,
    store_films_router
)
