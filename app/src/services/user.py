from sqlalchemy.ext.asyncio import AsyncSession

from app.src.services.db.dao.user_dao import UserDao
from app.src.services.db.dao.service_message_dao import ServiceMessageDao


async def save_user(
    session: AsyncSession, user_id: int, full_name: str, username: str | None
) -> None:
    await UserDao(session).insert_or_nothing(
        "id", id=user_id, full_name=full_name, username=username
    )


async def get_start_text(session: AsyncSession) -> str:
    text = await ServiceMessageDao(session).find_one_or_none(key="start")
    if text is None:
        return "Приветствие"
    return text.value
