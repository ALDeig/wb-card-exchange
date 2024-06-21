from dataclasses import dataclass

from aiogram import Bot
from sqlalchemy.ext.asyncio import AsyncSession

from app.settings import settings
from app.src.services.data_collection.texts import create_post_text
from app.src.services.date_utils import utc_date
from app.src.services.db.dao.card_dao import CardDao
from app.src.services.db.dao.service_message_dao import ServiceMessageDao
from app.src.services.wb.photo import get_photo_url


@dataclass(slots=True, frozen=True)
class Card:
    """Собранные данные о карточке."""

    category: str
    link: str
    name: str
    scu: int
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
    supplier_contacts: str
    contacts: str


async def prepare_post(session: AsyncSession, card: Card) -> tuple[str, str, int]:
    caption = await ServiceMessageDao(session).find_one_or_none(key="caption")
    if caption:
        caption = caption.value
    photo = get_photo_url(str(card.scu))
    text = create_post_text(card, caption)
    await CardDao(session).insert_or_update(
        "scu", {"last_posting_date"}, scu=card.scu, last_posting_date=utc_date()
    )
    return photo, text, settings.CHANNEL_ID


async def send_post(bot: Bot, photo: str, text: str) -> None:
    await bot.send_photo(settings.CHANNEL_ID, photo, caption=text)
