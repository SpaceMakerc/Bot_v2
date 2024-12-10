from aiogram import Router

from routers.handlers.store_document.add_name import router as router_doc_name
from routers.handlers.store_document.add_description import \
    router as router_description
from routers.handlers.store_document.add_document import \
    router as router_document

router = Router(name=__name__)

router.include_routers(
    router_doc_name,
    router_description,
    router_document
)
