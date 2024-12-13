from aiogram import Router

from routers.callback_handlers.show_films_cb import router as show_info_router

router = Router(name=__name__)

router.include_routers(
    show_info_router
)
