import asyncio
import os
import sys
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand

from app.core.logger import logger
from app.handlers import get_handlers_router
from app.middlewares import ThrottlingMiddleware, LoggingMiddleware


async def set_bot_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Botni ishga tushirish"),
        BotCommand(command="help", description="Qo'llanma va yordam"),
    ]
    await bot.set_my_commands(commands)


async def main():
    logger.info("Bot ishga tushirilmoqda...")

    # Tokenni faqat muhit o'zgaruvchisidan olish (Railway, .env yoki tizim)
    token = os.environ.get("BOT_TOKEN", "").strip()

    if not token:
        logger.critical(
            "XATOLIK: BOT_TOKEN topilmadi!\n"
            "Railway'da: Variables bo'limiga kirib BOT_TOKEN ni qo'shing.\n"
            "Lokalda: .env fayliga BOT_TOKEN=<token> yozing."
        )
        sys.exit(1)

    logger.info("Bot token muvaffaqiyatli aniqlandi.")

    bot = Bot(
        token=token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()

    dp.message.middleware(LoggingMiddleware())
    dp.message.middleware(ThrottlingMiddleware(
        limit=float(os.environ.get("RATE_LIMIT", "1.5"))
    ))

    main_router = get_handlers_router()
    dp.include_router(main_router)

    await set_bot_commands(bot)
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
