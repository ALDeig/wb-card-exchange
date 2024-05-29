import asyncio

from aiogram.exceptions import (
    TelegramBadRequest,
    TelegramForbiddenError,
    TelegramNotFound,
    TelegramRetryAfter,
    TelegramUnauthorizedError,
)
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.src.services.admin.texts import AMOUNT_USERS, READY
from app.src.services.date_utils import utc_date
from app.src.services.db.dao.service_message_dao import ServiceMessageDao
from app.src.services.db.dao.user_dao import UserDao


async def update_service_message(session: AsyncSession, title: str, text: str) -> str:
    """Обновление сервисного сообщения."""
    await ServiceMessageDao(session).insert_or_update(
        "key", {"value"}, key=title, value=text
    )
    return READY


async def mailing(session: AsyncSession, msg: Message):
    """Рассылка пользователям."""
    user_dao = UserDao(session)
    users = await user_dao.find_all()
    for user in users:
        result = await _try_send(msg, user.id)
        if not result:
            await user_dao.delete(id=user.id)


async def _try_send(msg: Message, user_id: int) -> bool:
    """Попытка отправить сообщение пользователю."""
    try:
        await msg.copy_to(user_id)
    except (
        TelegramBadRequest,
        TelegramForbiddenError,
        TelegramUnauthorizedError,
        TelegramNotFound,
    ):
        return False
    except TelegramRetryAfter as er:
        await asyncio.sleep(er.retry_after)
        await _try_send(msg, user_id)
    return True


async def get_count_users(session: AsyncSession, *, is_active: bool) -> str:
    """Количество пользователей."""
    if is_active:
        today = utc_date()
        count = await UserDao(session).count(last_active=today)
    else:
        count = await UserDao(session).count()
    return AMOUNT_USERS.format(count=count)
