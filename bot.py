import asyncio
import logging
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from handlers import start_handler, tiktok_handler

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def main():
    await bot.set_my_commands([
        {"command": "start", "description": "Start the bot"},
        {"command": "clearcache", "description": "Clear cache"}
    ])
    
    dp.include_router(start_handler.router)
    dp.include_router(tiktok_handler.router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")