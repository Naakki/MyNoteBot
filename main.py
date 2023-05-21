from aiogram import Bot, Dispatcher
from aiogram.types import Message
from pathlib import Path

from config_data.config import Config, load_config
from handlers import user_handlers, other_handlers

import asyncio
import logging

# Инициализируем логгер
logger = logging.getLogger(__name__)

async def main():
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s \n'
               '[%(asctime)s] - %(name)s - %(message)s \n'
    )

    logger.info('Starting bot')

    config: Config = load_config(Path('config_data','.env'))  # Подгружаем конфиг

    bot: Bot = Bot(token=config.tg_bot.token,
                   parse_mode='HTML',
                   session=config.server.proxy)
    dp: Dispatcher = Dispatcher()

    # Регистрируем роутеры
    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())