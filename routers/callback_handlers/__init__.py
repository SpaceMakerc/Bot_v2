from aiogram import Router

from routers.callback_handlers.show_serials_cb import router as show_serials_router
from routers.callback_handlers.show_films_cb import router as show_films_router

router = Router(name=__name__)

router.include_routers(
    show_films_router,
    show_serials_router
)
