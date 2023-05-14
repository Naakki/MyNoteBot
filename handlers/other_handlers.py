from aiogram import Router
from aiogram.types import Message
from aiogram.filters.state import StateFilter
from aiogram.fsm.state import default_state

from config_data.config import Config, load_config
from filters.is_admin import IsAdmin
from lexicon.ru import RU

import logging


config: Config = load_config('config_data\.env')
logger = logging.getLogger()
router: Router = Router()

# Класс IsAdmin() проверяет id пользователя, если он в списке Бот отвечает
@router.message(IsAdmin(config.tg_bot.admin_ids), StateFilter(default_state))
async def send_answer(message: Message):
    logger.info(message.from_user.id)
    await message.answer(text=RU['other_answer'])

    