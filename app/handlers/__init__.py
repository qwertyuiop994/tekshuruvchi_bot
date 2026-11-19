from aiogram import Router

from .start import start_router
from .photo import photo_router
from .question import question_router
from .errors import errors_router


def get_handlers_router() -> Router:
    """
    Barcha handler routerlarini bitta asosiy router ostida birlashtiradi.
    """
    main_router = Router(name="main_handlers")

    # Routerlar ketma-ketligi muhim:
    # 1. Boshqaruv va komandalar (start, help, menyu)
    # 2. Rasmlar (photo)
    # 3. Matnli savollar (question)
    # 4. Xatoliklar nazoratchisi (errors)
    main_router.include_router(start_router)
    main_router.include_router(photo_router)
    main_router.include_router(question_router)
    main_router.include_router(errors_router)

    return main_router


__all__ = ["get_handlers_router"]
