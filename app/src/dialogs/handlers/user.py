from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.src.dialogs.keyboards.collection import kb_new_lot
from app.src.services.user import get_start_text, save_user

router = Router()


@router.message(Command("start"), flags={"db": True})
async def cmd_start(msg: Message, db: AsyncSession, state: FSMContext):
    await state.clear()
    await save_user(db, msg.chat.id, msg.chat.full_name, msg.chat.username)
    start_text = await get_start_text(db)
    await msg.answer(start_text, reply_markup=kb_new_lot)
