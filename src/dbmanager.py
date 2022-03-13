from sqlite3 import Error, connect
from logging import info
from datetime import datetime
from json import loads, dumps


class DbManager:
    db = None

    def __init__(self):
        DbManager.db = connect('workpixil.db', check_same_thread=False)
        DbManager.db.isolation_level = None

    @staticmethod
    def close_db():
        DbManager.db.close()

    @staticmethod
    def row_to_dict(cursor, row):
        data = {}
        for idx, col in enumerate(cursor.description):
            data[str.lower(col[0])] = row[idx]
        return data

    @staticmethod
    def select(query):
        try:
            cur = DbManager.db.cursor()
            cur.row_factory = DbManager.row_to_dict
            info("ESEGUO LA QUERY: %s", query)
            cur.execute(str(query))
            result = cur.fetchall()
        except Error:
            DbManager.db.rollback()
            raise
        return result

    @staticmethod
    def insert_or_update(query):
        try:
            cur = DbManager.db.cursor()
            info("ESEGUO LA QUERY: %s", query)
            cur.execute(str(query))
            DbManager.db.commit()
        except Error:
            DbManager.db.rollback()
            raise

    @staticmethod
    def multiple_statement(query):
        try:
            cur = DbManager.db.cursor()
            cur.executescript(str(query))
            DbManager.db.commit()
        except Error:
            DbManager.db.rollback()
            raise