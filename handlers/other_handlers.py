from aiogram import Router
from aiogram.types import Message

from lexicon.ru import RU

import logging


logger = logging.getLogger()

router: Router = Router()

@router.message()
async def send_answer(message: Message):
    logger.info(message.from_user.id)
    await message.answer(text=RU['other_answer'])

    