import time
from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message
from app.core.config import settings


class ThrottlingMiddleware(BaseMiddleware):
    """
    Spam va ortiqcha so'rovlar yuborishdan himoyalovchi (Anti-Flood) oraliq qatlam.
    """

    def __init__(self, limit: float = None):
        self.limit = limit or settings.rate_limit
        self.last_requests: Dict[int, float] = {}

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        if not isinstance(event, Message):
            return await handler(event, data)

        user = event.from_user
        if not user:
            return await handler(event, data)

        user_id = user.id
        current_time = time.time()
        last_time = self.last_requests.get(user_id, 0)

        # Agar so'rovlar oralig'i limitdan kam bo'lsa
        if current_time - last_time < self.limit:
            self.last_requests[user_id] = current_time
            await event.answer("⚠️ <b>Iltimos, shoshilmang!</b>\nOldingi so'rovingiz tahlil qilinmoqda, biroz kuting...")
            return None

        self.last_requests[user_id] = current_time
        return await handler(event, data)
