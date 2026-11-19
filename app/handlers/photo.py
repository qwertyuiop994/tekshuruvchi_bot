import io
from aiogram import Router, F
from aiogram.types import Message
from aiogram.enums import ChatAction

from app.core.logger import logger
from app.services.ai_service import AIService
from app.utils.formatter import format_analysis_result
from app.utils.text_splitter import split_message

photo_router = Router(name="photo")
ai_service = AIService()


@photo_router.message(F.photo)
async def handle_photo_question(message: Message):
    """
    Foydalanuvchi yuborgan rasm (va rasm tagidagi izoh)dagi savollarni qabul qilish va tahlil qilish.
    """
    # Eng yuqori sifatdagi rasmni tanlab olish
    photo = message.photo[-1]
    caption = message.caption

    # Typing / uploading holatini ko'rsatish
    await message.bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)

    # Status xabari
    status_msg = await message.answer("⏳ Bajarilmoqda...")

    try:
        # Rasmni xotiraga yuklab olish
        file_in_memory = io.BytesIO()
        await message.bot.download(photo, destination=file_in_memory)
        image_bytes = file_in_memory.getvalue()

        # AI orqali rasmni tahlil qilish
        analysis_data = await ai_service.analyze_image(image_bytes=image_bytes, caption=caption)

        # Natijani chiroyli formatlash
        formatted_response = format_analysis_result(analysis_data)

        # Telegram xabar chegarasi bo'yicha bo'laklash
        chunks = split_message(formatted_response, max_chars=4000)

        # Status xabarini yangilash
        try:
            await status_msg.edit_text(chunks[0], parse_mode="HTML")
        except Exception:
            await status_msg.edit_text(chunks[0])

        # Agar qo'shimcha xabarlar bo'lsa
        for chunk in chunks[1:]:
            try:
                await message.answer(chunk, parse_mode="HTML")
            except Exception:
                await message.answer(chunk)

    except Exception as e:
        logger.error(f"Rasmni tahlil qilishda xatolik yuz berdi: {e}", exc_info=True)
        await status_msg.edit_text(
            "❌ <b>Rasmni tahlil qilib bo'lmadi!</b>\n"
            "Rasm sifati past bo'lishi yoki savollar aniq ko'rinmagan bo'lishi mumkin. "
            "Iltimos, rasmni aniqroq qilib qayta yuboring yoki savolni matn shaklida yozing.",
            parse_mode="HTML"
        )
