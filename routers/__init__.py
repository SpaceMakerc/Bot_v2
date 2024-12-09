from aiogram import Router

from .commands import router as commands_router
from .handlers import router as handlers_router

router = Router(name=__name__)

router.include_routers(
    commands_router,
    handlers_router
)
