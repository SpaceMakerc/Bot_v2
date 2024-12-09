from aiogram import Router

from routers.handlers.store_serial.add_genre import \
    router as router_serial_genre
from routers.handlers.store_serial.add_comment import \
    router as router_serial_comment
from routers.handlers.store_serial.add_name import router as router_serial_name

router = Router(name=__name__)

router.include_routers(
    router_serial_name,
    router_serial_comment,
    router_serial_genre
)
