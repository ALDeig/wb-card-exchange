from sqlalchemy.ext.asyncio import AsyncSession

from app.src.services.date_utils import utc_date
from app.src.services.db.dao.service_message_dao import ServiceMessageDao
from app.src.services.db.dao.user_dao import UserDao


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


async def update_last_active(session: AsyncSession, user_id: int) -> None:
    await UserDao(session).update({"last_active": utc_date()}, id=user_id)
