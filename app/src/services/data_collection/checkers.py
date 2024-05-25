from datetime import date, timedelta
from string import ascii_letters, digits

from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.src.services.data_collection.collection import DAYS
from app.src.services.data_collection.texts import DIGITS_ERROR
from app.src.services.db.dao.card_dao import CardDao


async def check_digit_message(msg: Message) -> int | None:
    if msg.text is None or not msg.text.replace(" ", "").isdigit():
        await msg.answer(DIGITS_ERROR)
        return
    return int(msg.text)


async def check_float_message(msg: Message) -> float | None:
    text = (msg.text or "").replace(",", ".").replace(" ", "")
    try:
        data = float(text)
    except ValueError:
        await msg.answer(DIGITS_ERROR)
        return
    return data


async def check_posting_avalible(session: AsyncSession, scu: int) -> bool:
    card = await CardDao(session).find_one_or_none(scu=scu)
    if card is None or card.last_posting_date < date.today() - timedelta(DAYS):
        return True
    return False


def check_telegram_nick(text: str | None) -> bool:
    if text is None or text.startswith("@"):
        return False
    for char in text[1:]:
        if char not in [*ascii_letters, *digits, "_"]:
            return False
    return True


def check_category(text: str) -> bool:
    if text is None or text.startswith("#"):
        return False
    for char in text[1:]:
        if char not in [*ascii_letters, *digits, "_"]:
            return False
    return True