import sqlite3
from  datetime import datetime


__connection = None
__cursor = None

def get_connection():
    global __connection
    if __connection is None:
        __connection = sqlite3.connect('data.db')
    return __connection

def get_cursor():
    global __cursor
    if __cursor is None:
        __cursor = get_connection().cursor()
    return __cursor

