from pathlib import Path
from peewee import *


# Определяем базовую модель о которой будут наследоваться остальные
class BaseModel(Model):
    class Meta:
        database = SqliteDatabase(Path('database', 'notes.db'))

# Определяем модель исполнителя (таблица в БД)
class Note(BaseModel):
    note_id = AutoField(column_name='id')
    note_title = TextField(column_name='title', null=False)
    note_link = TextField(column_name='note', null=False)

    class Meta:
        db_table = 'Notes'
        ordered_by = 'id'
    

#   Получение одиночной записи
# note = Note.get(Note.note_id == 1)

#   Получение набора записей
# query = Note.select().where(Note.note_id < 10).limit(5).order_by(Note.note_id.desc())
# Note_selected = query.dicts().execute()
#   Получаем итерируемый объект peewee, который можем перебрать
 
#   Создание записи
# 1) Note.create(note_title='<SomeTitle>', note_link='<SomeLink>')

# 2) note = Note(note_title='<SomeTitle>', note_link='<SomeLink>')
# 2) note.save()

#   Обновление записи
# 1) note = Note(note_title='<SomeTitle>')
# 1) note.note_link = '<SomeLink>'
# 1) note.save()

# 2) query = Note.update(note_link='<SomeNewLink>').where(Note.note_id==4)
# 2) query.execute()