from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message
from app.core.logger import logger


class LoggingMiddleware(BaseMiddleware):
    """
    Foydalanuvchi so'rovlarini konsol loglarida qayd etib boruvchi oraliq qatlam.
    """

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        if isinstance(event, Message) and event.from_user:
            user = event.from_user
            content_type = event.content_type
            logger.info(
                f"[ID:{user.id}] @{user.username or 'unknown'} ({user.full_name}) -> {content_type}"
            )

        return await handler(event, data)
