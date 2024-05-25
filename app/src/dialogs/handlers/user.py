from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.src.dialogs.states import PostDetailsState
from app.src.services.data_collection import texts

# from app.src.services.data_collection.collection import prepare_post
from app.src.services.user import get_start_text, save_user

router = Router()


@router.message(Command("start"), flags={"db": True})
async def cmd_start(msg: Message, db: AsyncSession, state: FSMContext):
    await save_user(db, msg.chat.id, msg.chat.full_name, msg.chat.username)
    start_text = await get_start_text(db)
    # photo, text = await prepare_post(db)
    # await msg.answer_photo(photo, caption=text)
    # return
    await msg.answer(start_text)
    await msg.answer(texts.CATEGORY)
    await state.set_state(PostDetailsState.category)
