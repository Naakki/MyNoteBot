from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from lexicon.ru import RU


note_list: KeyboardButton = KeyboardButton(text=RU['note_list'])
edit_list: KeyboardButton = KeyboardButton(text=RU['edit_list'])

main_kb_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
main_kb_builder.add(note_list, edit_list)

main_kb = main_kb_builder.as_markup(one_time_keyboard=True,
                                    resize_keyboard=True)