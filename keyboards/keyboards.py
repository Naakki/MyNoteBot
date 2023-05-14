from aiogram.types import KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from database.database import Note
from lexicon.ru import RU


def get_main_kb() -> ReplyKeyboardBuilder:

    note_list: KeyboardButton = KeyboardButton(text=RU['note_list'])
    edit_list: KeyboardButton = KeyboardButton(text=RU['edit_list'])

    main_kb_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
    main_kb_builder.add(note_list, edit_list)

    main_kb = main_kb_builder.as_markup(one_time_keyboard=True,
                                        resize_keyboard=True)
    return main_kb


def get_edit_list_kb() -> ReplyKeyboardBuilder:

    back_button: KeyboardButton = KeyboardButton(text=RU['back_button'])
    cancel_button: KeyboardButton = KeyboardButton(text=RU['cancel_button'])
    add_note: KeyboardButton = KeyboardButton(text=RU['add_note'])
    edit_note: KeyboardButton = KeyboardButton(text=RU['edit_note'])
    delete_note: KeyboardButton = KeyboardButton(text=RU['delete_note'])

    keyboard_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
    keyboard_builder.row(add_note, edit_note, 
                        delete_note, back_button, 
                        cancel_button, width=3)

    keyboard = keyboard_builder.as_markup(resize_keyboard=True)

    return keyboard

def select_inline_records() -> InlineKeyboardBuilder:
    
    keyboard_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    query = Note.select()

    for note in query.dicts().execute():
        keyboard_builder.row(InlineKeyboardButton(text=note['note_title'], 
                                                  callback_data=note['note_id']))
    keyboard = keyboard_builder.as_markup()

    return keyboard

def select_records() -> InlineKeyboardBuilder:
    
    keyboard_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    query = Note.select()

    for note in query.dicts().execute():
        keyboard_builder.row(InlineKeyboardButton(text=note['note_title'], 
                                                  callback_data=note['note_link']))
    keyboard = keyboard_builder.as_markup()

    return keyboard

def yes_no_kb() -> ReplyKeyboardBuilder:

    yes_button: KeyboardButton = KeyboardButton(text=RU['yes'])
    no_button: KeyboardButton = KeyboardButton(text=RU['no'])
    cancel_button: KeyboardButton = KeyboardButton(text=RU['cancel_button'])

    keyboard_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
    keyboard_builder.row(yes_button, no_button, cancel_button, width=2)

    keyboard = keyboard_builder.as_markup(one_time_keyboard=True,
                                          resize_keyboard=True)
    return keyboard

def what_to_edit_kb() -> InlineKeyboardBuilder:

    title_button: InlineKeyboardButton = InlineKeyboardButton(text=RU['title'], 
                                                              callback_data='title')
    note_button: InlineKeyboardButton = InlineKeyboardButton(text=RU['note'], 
                                                             callback_data='note')

    keyboard_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    keyboard_builder.add(title_button, note_button)

    keyboard = keyboard_builder.as_markup()

    return keyboard