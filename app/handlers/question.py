import asyncio
from aiogram import Router, F
from aiogram.types import Message
from aiogram.enums import ChatAction

from app.core.logger import logger
from app.services.ai_service import AIService
from app.utils.formatter import format_analysis_result
from app.utils.text_splitter import split_message

question_router = Router(name="question")
ai_service = AIService()


@question_router.message(F.text)
async def handle_text_question(message: Message):
    """
    Foydalanuvchi yuborgan ixtiyoriy matnli savol yoki katta testlar to'plamini (hatto 20+ bo'lsa ham)
    to'liq O'zbek tilida tahlil qilish.
    """
    text = message.text.strip()

    if len(text) < 3:
        await message.answer("⚠️ Iltimos, savolni to'liqroq yozib yuboring.")
        return

    # Typing holati
    await message.bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)

    # Status xabari
    status_msg = await message.answer("⏳ Bajarilmoqda...")

    try:
        # AI orqali tahlil qilish
        analysis_data = await ai_service.analyze_text(text)

        # Matnni formatlash
        formatted_response = format_analysis_result(analysis_data)

        # Telegram limiti bo'yicha bo'laklarga ajratish
        chunks = split_message(formatted_response, max_chars=3900)

        # Status xabarini birinchi bo'lak bilan almashtirish
        try:
            await status_msg.edit_text(chunks[0], parse_mode="HTML")
        except Exception:
            await status_msg.edit_text(chunks[0])

        # Qolgan bo'laklar (masalan 20 ta test bo'lganda 2-3 ta xabar bo'ladi)
        for chunk in chunks[1:]:
            await asyncio.sleep(0.5)  # Telegram flood control uchun kichik pauza
            try:
                await message.answer(chunk, parse_mode="HTML")
            except Exception:
                await message.answer(chunk)

    except Exception as e:
        logger.error(f"Matnli savolni tahlil qilishda xatolik yuz berdi: {e}", exc_info=True)
        await status_msg.edit_text(
            "❌ <b>Tahlil qilishda nosozlik yuz berdi!</b>\n"
            "Iltimos, birozdan so'ng qayta urinib ko'ring yoki testlarni bo'lib yuboring.",
            parse_mode="HTML"
        )
