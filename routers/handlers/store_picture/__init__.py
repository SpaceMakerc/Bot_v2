from aiogram import Router

from routers.handlers.store_picture.add_comment import \
    router as router_picture_comment
from routers.handlers.store_picture.add_status import \
    router as router_picture_status
from routers.handlers.store_picture.add_picture import \
    router as router_picture_picture

router = Router(name=__name__)

router.include_routers(
    router_picture_comment,
    router_picture_status,
    router_picture_picture
)
