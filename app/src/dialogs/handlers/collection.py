from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.src.dialogs.keyboards.collection import kb_new_lot, kb_yes_no
from app.src.dialogs.states import PostDetailsState
from app.src.services.data_collection import texts
from app.src.services.data_collection.checkers import (
    check_category,
    check_digit_message,
    check_float_message,
    check_telegram_nick,
    check_url_and_limit,
)
from app.src.services.data_collection.collection import Card, prepare_post
from app.src.services.exceptions import NotValidateUrl, PostingNotAvailable

router = Router()


@router.callback_query(F.data == "new_lot", F.message.as_("msg"))
async def btn_new_log(call: CallbackQuery, msg: Message, state: FSMContext):
    await call.answer()
    await msg.answer(texts.CATEGORY)
    await state.set_state(PostDetailsState.category)


@router.message(PostDetailsState.category, F.text.as_("text"))
async def get_category(msg: Message, text: str, state: FSMContext):
    if not check_category(text):
        await msg.answer(texts.CATEGORY)
        return
    await state.update_data(category=msg.text)
    await msg.answer(texts.LINK)
    await state.set_state(PostDetailsState.link)


@router.message(PostDetailsState.link, flags={"db": True})
async def get_link(msg: Message, state: FSMContext, db: AsyncSession):
    try:
        scu = await check_url_and_limit(db, msg.text or "")
    except NotValidateUrl:
        await msg.answer(texts.LINK_ERROR)
        return
    except PostingNotAvailable:
        await msg.answer(texts.LIMIT_ERROR)
        return
    await state.update_data(link=msg.text, scu=scu)
    await msg.answer(texts.COST)
    await state.set_state(PostDetailsState.cost)


@router.message(PostDetailsState.cost)
async def get_cost(msg: Message, state: FSMContext):
    cost = await check_digit_message(msg)
    if cost is not None:
        await state.update_data(cost=cost)
        await state.set_state(PostDetailsState.number_reviews)
        await msg.answer(texts.NUMBER_REVIEWS)


@router.message(PostDetailsState.number_reviews)
async def get_number_reviews(msg: Message, state: FSMContext):
    reviews = await check_digit_message(msg)
    if reviews is not None:
        await state.update_data(number_reviews=reviews)
        await state.set_state(PostDetailsState.review_rating)
        await msg.answer(texts.REVIEW_RATING)


@router.message(PostDetailsState.review_rating)
async def get_review_rating(msg: Message, state: FSMContext):
    data = await check_float_message(msg)
    if data is not None:
        await state.update_data(review_rating=data)
        await state.set_state(PostDetailsState.card_reting)
        await msg.answer(texts.CARD_RETING)


@router.message(PostDetailsState.card_reting)
async def get_card_reting(msg: Message, state: FSMContext):
    data = await check_float_message(msg)
    if data is not None:
        await state.update_data(card_reting=data)
        await state.set_state(PostDetailsState.cart_conversion)
        await msg.answer(texts.CART_CONVERSION)


@router.message(PostDetailsState.cart_conversion)
async def get_cart_conversion(msg: Message, state: FSMContext):
    data = await check_float_message(msg)
    if data is not None:
        await state.update_data(cart_conversion=data)
        await state.set_state(PostDetailsState.order_conversion)
        await msg.answer(texts.ORDER_CONVERSION)


@router.message(PostDetailsState.order_conversion)
async def get_order_conversion(msg: Message, state: FSMContext):
    data = await check_float_message(msg)
    if data is not None:
        await state.update_data(order_conversion=data)
        await state.set_state(PostDetailsState.redemption_percentage)
        await msg.answer(texts.REDEMPTION_PERCENTAGE)


@router.message(PostDetailsState.redemption_percentage)
async def get_redemption_percentage(msg: Message, state: FSMContext):
    data = await check_float_message(msg)
    if data is not None:
        await state.update_data(redemption_percentage=data)
        await state.set_state(PostDetailsState.slides)
        await msg.answer(texts.SLIDES, reply_markup=kb_yes_no)


@router.callback_query(PostDetailsState.slides, F.message.as_("msg"))
async def get_slides(call: CallbackQuery, msg: Message, state: FSMContext):
    await call.answer()
    await state.update_data(slides="Да" if call.data == "yes" else "Нет")
    await state.set_state(PostDetailsState.seo)
    await msg.answer(texts.SEO, reply_markup=kb_yes_no)


@router.callback_query(PostDetailsState.seo, F.message.as_("msg"))
async def get_seo(call: CallbackQuery, msg: Message, state: FSMContext):
    await call.answer()
    await state.update_data(seo="Да" if call.data == "yes" else "Нет")
    await state.set_state(PostDetailsState.revenue)
    await msg.answer(texts.REVENUE)


@router.message(PostDetailsState.revenue)
async def get_revenue(msg: Message, state: FSMContext):
    data = await check_digit_message(msg)
    if data is not None:
        await state.update_data(revenue=data)
        await state.set_state(PostDetailsState.inventory_balances)
        await msg.answer(texts.INVENTORY_BALANCES)


@router.message(PostDetailsState.inventory_balances)
async def get_inventory_balances(msg: Message, state: FSMContext):
    data = await check_digit_message(msg)
    if data is not None:
        await state.update_data(inventory_balances=data)
        await state.set_state(PostDetailsState.card_transfer_functionality)
        await msg.answer(texts.CARD_TRANSFER_FUNCTIONALITY, reply_markup=kb_yes_no)


@router.callback_query(
    PostDetailsState.card_transfer_functionality, F.message.as_("msg")
)
async def get_card_transfer_functionality(
    call: CallbackQuery, msg: Message, state: FSMContext
):
    await call.answer()
    await state.update_data(
        card_transfer_functionality="Да" if call.data == "yes" else "Нет"
    )
    await state.set_state(PostDetailsState.contacts)
    await msg.answer(texts.CONTACTS)


@router.message(PostDetailsState.contacts, flags={"db": True})
async def get_contact(msg: Message, bot: Bot, state: FSMContext, db: AsyncSession):
    if not check_telegram_nick(msg.text):
        await msg.answer(texts.CONTACTS_ERROR)
        return
    data = await state.update_data(contacts=msg.text)
    data = Card(**data)
    photo, text, channel_id = await prepare_post(db, data)
    await msg.answer(texts.END_MESSAGE, reply_markup=kb_new_lot)
    await bot.send_photo(channel_id, photo, caption=text)
    await state.clear()
