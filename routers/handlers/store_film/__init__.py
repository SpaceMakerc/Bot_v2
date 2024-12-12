from aiogram import Router

from routers.handlers.store_film.add_name import router as router_film_name
from routers.handlers.store_film.add_comment import \
    router as router_film_comment
from routers.handlers.store_film.add_genre import router as router_film_genre

router = Router(name=__name__)

router.include_routers(
    router_film_name,
    router_film_comment,
    router_film_genre
)
