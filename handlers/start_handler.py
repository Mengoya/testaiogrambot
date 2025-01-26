from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from db import get_user_by_id, create_or_get_user

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    user = await create_or_get_user(
        user_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        lang_code=message.from_user.language_code
    )
    username = user['username'] or 'Unknown'
    created_at_str = user['created_at'].strftime('%Y-%m-%d %H:%M:%S') if user['created_at'] else 'N/A'
    await message.answer(f"Hello, {username}!\nCreated at: {created_at_str}")