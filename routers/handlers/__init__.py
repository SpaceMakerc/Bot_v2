from aiogram import Router

from routers.handlers.store_picture import router as store_picture_router
from routers.handlers.store_serial import router as store_serial_router
from routers.handlers.store_film import router as store_films_router
from routers.handlers.handlers import router as handler_router

router = Router(name=__name__)

router.include_routers(
    handler_router,
    store_films_router,
    store_serial_router,
    store_picture_router
)
