import asyncio
import sys
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand

from app.core.config import settings
from app.core.logger import logger
from app.handlers import get_handlers_router
from app.middlewares import ThrottlingMiddleware, LoggingMiddleware

# Telegram Bot Token (.env faylidan olinadi)
BOT_TOKEN = settings.bot_token


async def set_bot_commands(bot: Bot):
    """
    Telegram menyusidagi standart buyruqlar ro'yxatini sozlash.
    """
    commands = [
        BotCommand(command="start", description="Botni ishga tushirish"),
        BotCommand(command="help", description="Qo'llanma va yordam"),
    ]
    await bot.set_my_commands(commands)


async def main():
    """
    Botni ishga tushirishning asosiy kirish funksiyasi.
    """
    logger.info("Bot ishga tushirilmoqda...")

    # Tokenni aniqlash (.env dan yoki to'g'ridan-to'g'ri o'rnatilgan tokendan)
    token = settings.bot_token if (settings.bot_token and "9243857438:AAG6I6TWcrd2D82wSZ3BtFxV0ff6qln-Ii0" not in settings.bot_token) else BOT_TOKEN

    if not token:
        logger.critical("XATOLIK: BOT_TOKEN topilmadi!")
        sys.exit(1)

    # Bot va Dispatcher yaratish
    bot = Bot(
        token=token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()

    # Oraliq qatlamlarni (Middlewares) ulash
    dp.message.middleware(LoggingMiddleware())
    dp.message.middleware(ThrottlingMiddleware(limit=settings.rate_limit))

    # Handler routerlarini ulash
    main_router = get_handlers_router()
    dp.include_router(main_router)

    # Buyruqlar menyusini sozlash
    await set_bot_commands(bot)

    # Eski kutilayotgan yangilanishlarni tozalash va pollingni boshlash
    await bot.delete_webhook(drop_pending_updates=True)
    logger.info("Bot muvaffaqiyatli ishga tushdi va xabarlarni qabul qilishga tayyor! 🚀")

    try:
        await dp.start_polling(bot)
    finally:
        logger.info("Bot sessiyasi yopilmoqda...")
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot qo'lda to'xtatildi.")
