from aiogram import Router
from aiogram.types import ErrorEvent
from aiogram.exceptions import TelegramAPIError

from app.core.logger import logger

errors_router = Router(name="errors")


@errors_router.error()
async def global_error_handler(event: ErrorEvent):
    """
    Global xatoliklarni tutib qoluvchi va logga yozuvchi handler.
    """
    exception = event.exception
    update = event.update

    logger.error(f"Global xatolik ro'y berdi: {exception} | Update: {update}", exc_info=True)

    # Agar xabar yuborish imkoni bo'lsa, foydalanuvchiga xabar beramiz
    if update.message:
        try:
            await update.message.answer(
                "⚠️ <b>Kechirasiz, tizimda kutilmagan xatolik yuz berdi.</b>\n"
                "Iltimos, birozdan so'ng qayta urinib ko'ring.",
                parse_mode="HTML"
            )
        except TelegramAPIError as e:
            logger.warning(f"Foydalanuvchiga xatolik xabarini yuborishda muammo: {e}")
