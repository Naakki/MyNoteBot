from ast import Call
import re
from aiogram import Router, F
from aiogram.filters import Command, CommandStart, StateFilter,Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State, default_state
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, CallbackQuery


from config_data.config import Config, load_config
from database.database import Note
from filters.is_admin import IsAdmin
from keyboards.keyboards import (get_main_kb, get_edit_list_kb, 
                                 select_inline_records, yes_no_kb,
                                 what_to_edit_kb, select_records)
from lexicon.ru import RU


router: Router = Router()
config: Config = load_config()
storage: MemoryStorage = MemoryStorage()

class AddNoteRecord(StatesGroup):
    title = State()
    link = State()

class EditNoteRecord(StatesGroup):
    choose_record = State()
    what_to_edit = State()
    edited_text = State()
    confirm = State()

class DeleteNoteRecord(StatesGroup):
    choose_record = State()
    confirm = State()

@router.message(CommandStart(), IsAdmin(config.tg_bot.admin_ids))
async def start(message: Message):
    await message.answer(text=RU['/start'])
    await message.answer(text=RU['choose_action'], reply_markup=get_main_kb())

@router.message(Command(commands=['help']), IsAdmin(config.tg_bot.admin_ids))
async def help(message: Message):
    await message.answer(text=RU['/help'], reply_markup=get_main_kb())

@router.message(Text(text=RU['note_list']), IsAdmin(config.tg_bot.admin_ids))
async def show_note_list(message: Message):
    await message.answer(text=RU['your_notes'], reply_markup=select_records())

@router.message(Text(text=RU['edit_list']), IsAdmin(config.tg_bot.admin_ids))
async def edit_note_list(message: Message):
    await message.answer(text=RU['choose_action'], reply_markup=get_edit_list_kb())

@router.message(Text(text=RU['back_button']), IsAdmin(config.tg_bot.admin_ids))
async def back_button(message: Message):
    await message.answer(text=RU['choose_action'], reply_markup=get_main_kb())

@router.message(Text(text=RU['cancel_button']), IsAdmin(config.tg_bot.admin_ids))
async def cancel_button(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text=RU['canceled'], reply_markup=get_edit_list_kb())

# Хендлеры для добавления записи
@router.message(Text(text=RU['add_note']), IsAdmin(config.tg_bot.admin_ids))
async def add_title(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(AddNoteRecord.title)
    await message.answer(text=RU['press_title'])

@router.message(StateFilter(AddNoteRecord.title))
async def add_link(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(AddNoteRecord.link)
    await message.answer(text=RU['press_link'])

@router.message(StateFilter(AddNoteRecord.link))
async def add_record(message: Message,state: FSMContext):
    await state.update_data(link=message.text)
    data = await state.get_data()

    Note.create(note_title=data['title'], note_link=data['link'])

    await state.clear()
    await message.answer(text=f"{RU['data_added']} \n"
                              f"{data['title']} -> {data['link']}",
                         reply_markup=get_edit_list_kb())

# Хендлеры для изменения Записи
@router.message(Text(text=RU['edit_note']), IsAdmin(config.tg_bot.admin_ids))
async def get_record_to_edit(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(EditNoteRecord.choose_record)
    await message.answer(text=RU['choose_record_to_edit'], reply_markup=select_inline_records())

@router.callback_query(StateFilter(EditNoteRecord.choose_record))
async def get_record_to_edit(callback: CallbackQuery, state: FSMContext):
    note = Note.select().where(Note.note_id == callback.data).dicts().execute()[0]

    await state.update_data(choose_record=callback.data)
    await state.set_state(EditNoteRecord.what_to_edit)
    await callback.message.delete()
    await callback.message.answer(text=f"{RU['what_to_edit']}\n\n"
                                       f"{RU['title']}: {note['note_title']}\n"
                                       f"{RU['note']}: {note['note_link']}",
                                  reply_markup=what_to_edit_kb())
    
@router.callback_query(StateFilter(EditNoteRecord.what_to_edit))
async def what_to_edit(callback: CallbackQuery, state: FSMContext):
    await state.update_data(what_to_edit=callback.data)
    await state.set_state(EditNoteRecord.edited_text)
    await callback.message.delete()
    await callback.message.answer(text=f"{RU[callback.data]}:")

@router.message(StateFilter(EditNoteRecord.edited_text))
async def confirm_edit_record(message: Message, state: FSMContext):
    await state.update_data(edited_text=message.text)

    data = await state.get_data()
    await state.set_state(EditNoteRecord.confirm)
    note = Note.select().where(Note.note_id == data['choose_record']).dicts().execute()[0]

    if data['what_to_edit'] == 'title':
        title = data['edited_text']
        note = note['note_link']
    elif data['what_to_edit'] == 'note':
        title = note['note_title']
        note = data['edited_text']

    await message.answer(text=f"{RU['r_y_sure_to_edit']}:\n\n"
                              f"{RU['title']}: {title}\n"
                              f"{RU['note']}: {note}",
                         reply_markup=yes_no_kb())
    
@router.message(StateFilter(EditNoteRecord.confirm), Text(text=RU['yes']))
async def edit_record(message: Message, state: FSMContext):
    data = await state.get_data()
    
    note = Note.select().where(Note.note_id == data['choose_record']).dicts().execute()[0]

    if data['what_to_edit'] == 'title':
        title = data['edited_text']
        note = note['note_link']
    elif data['what_to_edit'] == 'note':
        title = note['note_title']
        note = data['edited_text']

    query = (Note
             .update({Note.note_title: title, 
                      Note.note_link: note})
             .where(Note.note_id == data['choose_record']))
    query.execute()

    await state.clear()
    await message.answer(text=RU['record_edited'], reply_markup=get_edit_list_kb())

@router.message(StateFilter(EditNoteRecord.confirm), Text(text=RU['no']))
async def not_edit_record(message: Message, state: FSMContext):
    await state.set_state(EditNoteRecord.choose_record)
    await message.answer(text=RU['choose_record_to_edit'], reply_markup=select_inline_records())

# Хендлеры для удаления записи
@router.message(Text(text=RU['delete_note']), IsAdmin(config.tg_bot.admin_ids))
async def get_record_to_delete(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(DeleteNoteRecord.choose_record)
    await message.answer(text=RU['choose_record_to_delete'], reply_markup=select_inline_records())

@router.callback_query(StateFilter(DeleteNoteRecord.choose_record))
async def choose_record_to_delete(callback: CallbackQuery, state: FSMContext):
    note = Note.select().where(Note.note_id == callback.data).dicts().execute()[0]

    await state.update_data(choose_record=callback.data)
    await state.set_state(DeleteNoteRecord.confirm)
    await callback.message.delete()
    await callback.message.answer(text=f"{RU['r_y_sure_to_delete']}:\n\n"
                                       f"{RU['title']}: {note['note_title']}\n"
                                       f"{RU['note']}: {note['note_link']}", 
                                  reply_markup=yes_no_kb()) 

@router.message(StateFilter(DeleteNoteRecord.confirm), Text(text=RU['yes']))
async def confirm_record_to_delete_yes(message: Message, state: FSMContext):
    id_to_delete = await state.get_data()

    note = Note.get(Note.note_id == id_to_delete['choose_record'])
    note.delete_instance()

    await state.clear()
    await message.answer(text=RU['record_deleted'], reply_markup=get_edit_list_kb())

@router.message(StateFilter(DeleteNoteRecord.confirm), Text(text=RU['no']))
async def confirm_record_to_delete_no(message: Message, state: FSMContext):
    await state.set_state(DeleteNoteRecord.choose_record)
    await message.answer(text=RU['choose_record_to_delete'], reply_markup=select_inline_records())
