from aiogram.fsm.state import StatesGroup, State


class PostDetailsState(StatesGroup):
    category = State()
    link = State()
    cost = State()
    number_reviews = State()
    review_rating = State()
    card_reting = State()
    cart_conversion = State()
    order_conversion = State()
    redemption_percentage = State()
    slides = State()
    seo = State()  # SEO оптимизация
    revenue = State()  # Выручка за последние 3 месяца
    inventory_balances = State()  # Товарные остатки
    card_transfer_functionality = State()
    supplier_contacts = State()
    contacts = State()

