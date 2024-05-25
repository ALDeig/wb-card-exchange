from dataclasses import dataclass
from datetime import date, timedelta
from string import ascii_letters, digits

from aiogram import Bot
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.settings import settings
from app.src.services.data_collection.texts import DIGITS_ERROR, create_post_text
from app.src.services.db.dao.card_dao import CardDao
from app.src.services.wb.photo import get_photo_url
from app.src.services.wb.url import get_article

DAYS = 3


@dataclass(slots=True, frozen=True)
class Card:
    category: str
    link: str
    cost: int
    number_reviews: int
    review_rating: int
    card_reting: int
    cart_conversion: int
    order_conversion: int
    redemption_percentage: int
    slides: str
    seo: str
    revenue: int
    inventory_balances: int
    card_transfer_functionality: str
    contacts: str


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
    if text is None:
        return False
    for char in text:
        if char not in [*ascii_letters, *digits, "_"]:
            return False
    return True


# card = Card(
#     category="#adsfdf",
#     link="https://www.wildberries.ru/catalog/150320604/detail.aspx",
#     cost=123,
#     number_reviews=2,
#     review_rating=3,
#     card_reting=3,
#     cart_conversion=3,
#     order_conversion=3,
#     redemption_percentage=3,
#     slides="Да",
#     seo="Да",
#     revenue=3,
#     inventory_balances=3,
#     card_transfer_functionality="Нет",
#     contacts="aldeig"
# )


async def prepare_post(session: AsyncSession, card: Card) -> tuple[str, str, int]:
    scu = get_article(card.link)
    photo = get_photo_url(str(scu))
    text = create_post_text(card)
    await CardDao(session).insert_or_update(
        "scu", {"last_posting_date"}, scu=scu, last_posting_date=date.today()
    )
    return photo, text, settings.CHANNEL_ID


async def send_post(bot: Bot, photo: str, text: str) -> None:
    await bot.send_photo(settings.CHANNEL_ID, photo, caption=text)
