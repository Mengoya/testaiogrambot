import re
from aiogram import Router, F
from aiogram.types import Message

router = Router()

# YouTube URL patterns
YOUTUBE_PATTERNS = [
    r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com|youtu\.be)\/(?:watch\?v=)?([^\s&]+)',
]

def is_youtube_url(text: str) -> bool:
    return any(re.search(pattern, text) for pattern in YOUTUBE_PATTERNS)

@router.message(F.text)
async def handle_youtube_link(message: Message):
    if not is_youtube_url(message.text):
        return
    await message.answer('YouTube link detected!')