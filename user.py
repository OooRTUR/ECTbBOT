import db
import sqlite3
from utils import serialize_datetime, deserialize_datetime
from datetime import datetime


def init_db(force: bool = False):
    # удалить таблицу user_message, если она существует
    if force:
        db.get_cursor().execute('DROP TABLE IF EXISTS user')

    db.get_cursor().execute('''
        CREATE TABLE IF NOT EXISTS user (
            id                  INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id         INTEGER NOT NULL,
            datetime_created    TEXT,
            datetime_last       TEXT,
            age                 INTEGER,
            sex                 INTEGER,
            weight              REAL,
            UNIQUE(telegram_id)
        )
    ''')
    db.get_connection().commit()


def set_lasttime(telegram_id: int, dt_last: str, force_commit: bool = True):
    sql = '''
        UPDATE user
        SET datetime_last = ?
        WHERE telegram_id = ?
    '''
    db.get_cursor().execute(sql, (dt_last, telegram_id))
    if force_commit: db.get_connection().commit()


def add_user(telegram_id: int, dt_created: str):
    print('1')
    db.get_cursor().execute('INSERT OR IGNORE INTO user (telegram_id, datetime_created) VALUES (?, ?)', (telegram_id, dt_created))
    print('2')
    set_lasttime(telegram_id, dt_created, False)
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


if __name__ == '__main__':
    init_db(force=True)
    # id = 5432132
    # add_user(id, serialize_datetime(datetime.now()))
    # set_user_age(id, 27)
