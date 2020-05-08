import db
import sqlite3
from utils import  serialize_datetime, deserialize_datetime
from datetime import datetime

def init_db(force: bool = False):

    # удалить таблицу user_message, если она существует
    if force:
        db.get_cursor().execute('DROP TABLE IF EXISTS user')

    db.get_cursor().execute('''
        CREATE TABLE IF NOT EXISTS user (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id     INTEGER NOT NULL,
            date_created    TEXT,
            age             INTEGER,
            sex             INTEGER,
            weight          REAL
        )
    ''')
    db.get_connection().commit()

def add_user(telegram_id: int, date_created: str):
    db.get_cursor().execute('INSERT INTO user (telegram_id, date_created) VALUES (?, ?)', (telegram_id, date_created))
    db.get_connection().commit()

def set_user_age(telegram_id, age: int):
    sql = '''
        UPDATE user
        SET age = ?
        WHERE telegram_id = ?
    '''
    db.get_cursor().execute(sql, (age, telegram_id))
    db.get_connection().commit()

def set_user_sex(telegram_id, sex: bool):
    sql = '''
        UPDATE user
        SET sex = ?
        WHERE telegram_id = ?
    '''
    sqlite3.register_adapter(bool, int)
    db.get_cursor().execute(sql, (sex, telegram_id))
    db.get_connection().commit()

def set_user_weight(telegram_id, weight: float):
    sql = '''
        UPDATE user
        SET weight = ?
        WHERE telegram_id = ?
    '''
    sqlite3.register_adapter(bool, int)
    db.get_cursor().execute(sql, (weight, telegram_id))
    db.get_connection().commit()

#
# if __name__ == '__main__':
#     init_db(force=False)
#     id = 353535
#     set_user_age(id, 27)