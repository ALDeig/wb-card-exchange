from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


kb_yes_no = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Да", callback_data="yes"),
            InlineKeyboardButton(text="Нет", callback_data="no"),
        ]
    ]
)

kb_new_lot = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Разместить следующий лот", callback_data="new_lot")]
    ]
)
