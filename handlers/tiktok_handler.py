import re
import aiohttp
from bs4 import BeautifulSoup
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from redis_cache import get_file_id, set_file_id, delete_file_id, clear_redis_cache
import aiofiles
from aiogram.types import FSInputFile

router = Router()

TIKTOK_PATTERNS = [
    r'(?:https?:\/\/)?(?:www\.)?(?:tiktok\.com\/@[\w.-]+\/video\/\d+)',
    r'(?:https?:\/\/)?(?:www\.)?(?:tiktok\.com\/t\/[\w-]+)',
    r'(?:https?:\/\/)?(?:vm\.)?(?:tiktok\.com\/\w+)',
]

def is_tiktok_url(text: str) -> bool:
    return any(re.search(pattern, text) for pattern in TIKTOK_PATTERNS)

async def make_ssstik_request(url: str) -> str:
    headers = {
        'accept': '*/*',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'hx-current-url': 'https://ssstik.io/',
        'hx-request': 'true',
        'hx-target': 'target',
        'hx-trigger': '_gcaptcha_pt',
        'origin': 'https://ssstik.io',
        'referer': 'https://ssstik.io/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    data = {
        'id': url,
        'locale': 'en',
        'tt': 'a0xXVHMz'
    }

    async with aiohttp.ClientSession() as session:
        async with session.post('https://ssstik.io/abc?url=dl', 
                              headers=headers, 
                              data=data) as response:
            html_content = await response.text()
            
            soup = BeautifulSoup(html_content, 'html.parser')
            download_link = soup.find('a', {'class': 'without_watermark'})
            
            if download_link and 'href' in download_link.attrs:
                return download_link['href']
    return None

@router.message(F.text)
async def handle_tiktok_link(message: Message):
    if not is_tiktok_url(message.text):
        return

    file_id = await get_file_id(message.text)
    if file_id:
        try:
            await message.answer_video(video=file_id)
            return
        except:
            await delete_file_id(message.text)

    print(f'Processing TikTok link: {message.text}')
    download_url = await make_ssstik_request(message.text)
    if download_url:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(download_url) as resp:
                    if resp.status == 200:
                        async with aiofiles.open('temp_video.mp4', 'wb') as f:
                            await f.write(await resp.read())
                        video = FSInputFile('temp_video.mp4')
                        msg = await message.answer_video(video=video)
                        if msg.video:
                            await set_file_id(message.text, msg.video.file_id)
                    else:
                        await message.answer('Ошибка загрузки видео.')
        except Exception as e:
            print(f'Ошибка: {e}')
            await message.answer('Не удалось обработать видео.')
    else:
        await message.answer('Ссылка не найдена.')