import re
import yt_dlp
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
    
    try:
        with yt_dlp.YoutubeDL() as ydl:
            info = ydl.extract_info(message.text, download=False)
            
            # Print video info to console
            print("\n=== YouTube Video Info ===")
            print(f"Title: {info['title']}")
            print(f"Duration: {info['duration']} seconds")
            print(f"Views: {info['view_count']}")
            print(f"Channel: {info['channel']}")
            print(f"Upload date: {info['upload_date']}")
            print("=======================\n")
            
            # Reply to user
            await message.reply(
                f"📹 Found video:\n"
                f"Title: {info['title']}\n"
                f"Channel: {info['channel']}"
            )
    except Exception as e:
        print(f"Error processing YouTube URL: {e}")
        await message.reply("Sorry, couldn't process this YouTube link")