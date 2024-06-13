from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.src.services.data_collection.collection import Card

DIGITS_ERROR = "Введите информацию цифрами"

CATEGORY = (
    "Впишите категорию товара через #, например #блузки. Если два слова то "
    "через нижнее подчеркивание #мужские_рубашки"
)
LINK = "Ссылка на карточку:"
LINK_ERROR = "Введите ссылку на карточку товара"
COST = "Впишите цифрами стоимость карточки"
COST_ERROR = "Введите стоимость цифрами"
NUMBER_REVIEWS = "Количество отзывов:"
REVIEW_RATING = "Рейтинг по отзывам:"
CARD_RETING = "Рейтинг карточки:"
CART_CONVERSION = "Конверсия в корзину, %:"
ORDER_CONVERSION = "Конверсия в заказ, %:"
REDEMPTION_PERCENTAGE = "Процент выкупа, %:"
SLIDES = "Слайды с исходниками:"
SEO = "SEO оптимизация:"
REVENUE = "Выручка за последние 3 месяца:"
INVENTORY_BALANCES = "Товарные остатки¸ шт."
CARD_TRANSFER_FUNCTIONALITY = "Функционал передачи карточки"
CONTACTS = "Впишите свой ник в Телеграмм"
CONTACTS_ERROR = "Введите ник Телеграмм"

LIMIT_ERROR = "Размещение лота на одну и ту же карточку товара 1 раз в 3 дня"
END_MESSAGE = (
    "Ваш лот размещён на @stockcardwb. По вопросам работы сервиса пишите @seohandmade"
)
DEFAULT_CAPTION = "📌Для размещения лота перейдите в бот @stockcardwb_bot"


def create_post_text(data: "Card", caption: str | None) -> str:
    text = f"""
<b>Категория:</b> {data.category}
<b>Ссылка на карточку:</b> {data.link}
<b>Наименование товара:</b> {data.name}
<b>Стоимость¸ руб.:</b> {data.cost}
<b>Количество отзывов:</b> {data.number_reviews}
<b>Рейтинг по отзывам:</b> {data.review_rating}
<b>Рейтинг карточки:</b> {data.card_reting}
<b>Конверсия в корзину, %:</b> {data.cart_conversion}
<b>Конверсия в заказ, %:</b> {data.order_conversion}
<b>Процент выкупа, %:</b> {data.redemption_percentage}
<b>Слайды с исходниками:</b> {data.slides}
<b>SEO оптимизация:</b> {data.seo}
<b>Выручка за последние 3 месяца:</b> {data.revenue}
<b>Товарные остатки¸ шт.:</b> {data.inventory_balances}
<b>Функционал передачи карточки:</b> {data.card_transfer_functionality}
<b>Контакты:</b> {data.contacts}

{caption or DEFAULT_CAPTION}
"""
    return text.strip()
