from aiogram import Router
from aiogram.filters import Command, CommandStart, Text
from aiogram.types import Message

from keyboards.keyboards import main_kb
from lexicon.ru import RU


router: Router = Router()

@router.message(CommandStart())
async def start(message: Message):
    await message.answer(text=RU['/start'], reply_markup=main_kb)

@router.message(Command(commands=['help']))
async def help(message: Message):
    await message.answer(text=RU['/help'], reply_markup=main_kb)

@router.message(Text(text=RU['note_list']))
async def show_note_list(message: Message):
    await message.answer(text=RU['your_notes'])

@router.message(Text(text=RU['edit_list']))
async def edit_note_list(message: Message):
    await message.answer(text=RU['choose_action'])
