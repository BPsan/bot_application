import asyncio

from aiogram import Bot, Dispatcher
from app.handlers import router

import config


'''@dp.message()
async def cmd_start(message:Message):
    await message.answer('Привет')'''

async def main():
    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')