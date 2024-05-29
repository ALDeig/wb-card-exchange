from datetime import timedelta
from string import ascii_letters, digits

from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.src.services.data_collection.texts import DIGITS_ERROR
from app.src.services.date_utils import utc_date
from app.src.services.db.dao.card_dao import CardDao
from app.src.services.exceptions import NotValidateUrl, PostingNotAvailable
from app.src.services.wb.parser import get_card_name
from app.src.services.wb.url import check_url, get_article

CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
DAYS = 3


async def get_data_by_link(db: AsyncSession, url: str) -> tuple[int, str]:
    is_valid = check_url(url)
    if not is_valid:
        raise NotValidateUrl
    scu = get_article(url)
    if not await _check_posting_available(db, scu):
        raise PostingNotAvailable
    name = await get_card_name(scu)
    return scu, name


async def check_digit_message(msg: Message) -> int | None:
    text = (msg.text or "").replace(" ", "")
    try:
        number = int(text)
    except ValueError:
        await msg.answer(DIGITS_ERROR)
        return
    return number


async def check_float_message(msg: Message) -> float | None:
    text = (msg.text or "").replace(",", ".").replace(" ", "")
    try:
        data = float(text)
    except ValueError:
        await msg.answer(DIGITS_ERROR)
        return
    return data


async def _check_posting_available(session: AsyncSession, scu: int) -> bool:
    card = await CardDao(session).find_one_or_none(scu=scu)
    return card is None or card.last_posting_date <= utc_date() - timedelta(DAYS)


def check_telegram_nick(text: str | None) -> bool:
    if text is None or not text.startswith("@"):
        return False
    return all(char in {*ascii_letters, *digits, "_"} for char in text[1:])
    # for char in text[1:]:
    #     if char not in {*ascii_letters, *digits, "_"}:
    #         return False
    # return True


def check_category(text: str) -> bool:
    if text is None or not text.startswith("#"):
        return False
    for char in text[1:]:
        if char not in {*ascii_letters, *digits, *CYRILLIC_SYMBOLS, "_"}:
            return False
    return True
