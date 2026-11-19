import asyncio
import base64
import json
import re
import aiohttp
from typing import Any, Dict, Optional

from app.core.logger import logger
from app.core.prompts import SYSTEM_ANALYZER_PROMPT


class AIService:
    """
    Tashqi API kalitlarni talab qilmaydigan, to'liq mustaqil va bepul
    AI xizmati (Pollinations AI + OCR). Katta hajmdagi testlarni (20+) to'liq
    O'zbek tilida tahlil qilish uchun optimallashtirilgan.
    """

    def __init__(self):
        self.api_url = "https://text.pollinations.ai/"
        logger.info("AI Service muvaffaqiyatli ishga tushirildi (Kalitsiz bepul AI rejimi).")

    def _extract_and_parse_json(self, response_text: str) -> Dict[str, Any]:
        """
        AI javobidan JSON obyektini xavfsiz ajratib oladi.
        """
        text = response_text.strip()
        # Markdown kod bloklarini tozalash
        if text.startswith("```"):
            text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.MULTILINE)
            text = re.sub(r"```$", "", text, flags=re.MULTILINE)
            text = text.strip()

        try:
            data = json.loads(text)
            if isinstance(data, dict) and "questions" in data:
                return data
            elif isinstance(data, list):
                return {
                    "is_test_collection": len(data) > 1,
                    "total_questions": len(data),
                    "questions": data
                }
            return data
        except json.JSONDecodeError:
            # Regex orqali eng katta { ... } blokini olish
            match = re.search(r"(\{.*\})", text, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group(1))
                except Exception:
                    pass

            # Agar qat'iy JSON olinmasa, matnni bo'laklarga ajratib chiqarish
            return {
                "is_test_collection": False,
                "total_questions": 1,
                "questions": [
                    {
                        "number": 1,
                        "question_text": "Savollar to'plami",
                        "is_multiple_choice": False,
                        "selected_option": None,
                        "correct_answer": "Javoblar quyida keltirilgan",
                        "has_user_answer": False,
                        "user_answer": None,
                        "is_user_correct": None,
                        "explanation": text,
                        "is_unclear": False,
                        "unclear_reason": None
                    }
                ]
            }

    async def analyze_text(self, text: str) -> Dict[str, Any]:
        """
        Foydalanuvchi yuborgan savollarni (hatto 20+ ta test bo'lsa ham)
        to'liq O'zbek tilida tahlil qiladi.
        """
        user_prompt = (
            "Quyidagi barcha savol va testlarni DIQQAT BILAN, BIRORTASINI HAM TASHIRISh KETMASDAN, "
            "BARCHASINI 1-savoldan oxirigacha TO'LIQ O'ZBEK TILIDA tahlil qil, to'g'ri javoblarni aniqla, "
            "agar foydalanuvchi javob bergan bo'lsa uni tekshir va har biriga aniq tushuntirish berib, "
            f"belgilangan JSON formatida qaytar:\n\n{text}"
        )

        payload = {
            "messages": [
                {"role": "system", "content": SYSTEM_ANALYZER_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            "model": "openai",
            "jsonMode": True
        }

        try:
            # Katta hajmdagi testlar uchun timeout 120 soniya
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.api_url,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=120)
                ) as response:
                    if response.status == 200:
                        raw_result = await response.text()
                        return self._extract_and_parse_json(raw_result)
                    else:
                        logger.error(f"AI server xatolik kodi: {response.status}")
                        raise Exception(f"AI server javob bermadi (status: {response.status})")
        except Exception as e:
            logger.error(f"Matn tahlilida xatolik: {e}", exc_info=True)
            raise e

    async def _extract_text_from_image(self, image_bytes: bytes) -> str:
        """
        Bepul OCR xizmati orqali rasmdagi matnlarni o'qib oladi.
        """
        try:
            form = aiohttp.FormData()
            form.add_field("apikey", "helloworld")
            form.add_field("language", "eng")
            form.add_field("isOverlayRequired", "false")
            form.add_field(
                "file",
                image_bytes,
                filename="question.jpg",
                content_type="image/jpeg"
            )

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "https://api.ocr.space/parse/image",
                    data=form,
                    timeout=aiohttp.ClientTimeout(total=40)
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        parsed_results = data.get("ParsedResults", [])
                        if parsed_results:
                            extracted = parsed_results[0].get("ParsedText", "").strip()
                            if extracted:
                                return extracted
        except Exception as e:
            logger.warning(f"OCR jarayonida xatolik: {e}")

        return ""

    async def analyze_image(self, image_bytes: bytes, caption: Optional[str] = None) -> Dict[str, Any]:
        """
        Rasmdagi barcha testlar va savollarni o'qib, O'zbek tilida tahlil qiladi.
        """
        extracted_text = await self._extract_text_from_image(image_bytes)

        full_prompt_text = ""
        if extracted_text:
            full_prompt_text += f"Rasmdan o'qilgan savol va testlar:\n{extracted_text}\n\n"
        if caption:
            full_prompt_text += f"Foydalanuvchi izohi:\n{caption}\n"

        if not full_prompt_text.strip():
            return {
                "is_test_collection": False,
                "total_questions": 1,
                "questions": [
                    {
                        "number": 1,
                        "question_text": "Rasmli savol",
                        "is_multiple_choice": False,
                        "selected_option": None,
                        "correct_answer": "Savol matni aniqlanmadi",
                        "has_user_answer": False,
                        "user_answer": None,
                        "is_user_correct": None,
                        "explanation": "Rasmdagi yozuvlar aniq ko'rinmadi. Iltimos, rasmni tiniqroq tushirib qayta yuboring yoki savollarni matn qilib yozing.",
                        "is_unclear": True,
                        "unclear_reason": "Rasmdagi yozuvlar juda xira yoki o'qib bo'lmaydigan holatda."
                    }
                ]
            }

        return await self.analyze_text(full_prompt_text)
