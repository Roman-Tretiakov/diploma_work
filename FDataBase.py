import math
import sqlite3
import time


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def get_menu(self):
        sql = "SELECT * FROM mainmenu"
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res:
                return res
        except Exception as e:
            print(f"Read from DB error: {e.args}")
        return []

    def add_post(self, title, text):
        try:
            tm = math.floor((time.time()))
            self.__cur.execute("INSERT INTO posts VALUES (NULL, ?, ?, ?)", (title, text, tm))
            self.__db.commit()
        except sqlite3.Error as e:
            print(f"Failed to add post in DB: {e.args}")
            return False

        return True
