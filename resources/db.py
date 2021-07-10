import sqlite3
from datetime import datetime

class Database:

    def __init__(self):
        self.con = sqlite3.connect('guestbook.db')

    def initialize_guestbook(self):
        cur = self.con.cursor()
        cur.execute(''' DROP TABLE if EXISTS guestbook ''')
        cur.execute(''' CREATE TABLE guestbook (date text, name text, message text); ''')
        self.con.commit()
        cur.close()

    def new_guestbook_message(self, message):
        cur = self.con.cursor()
        try:
            cur.execute(''' INSERT INTO guestbook (date,name,message)
                        VALUES(?,?,?); ''', (message[0],message[1],message[2]))
            self.con.commit()
            cur.close()
        except sqlite3.OperationalError:
            self.initialize_guestbook()
            self.new_guestbook_message(message)

    def get_guestbook_message(self):
        return_data = []
        cur = self.con.cursor()
        try:
            data = cur.execute(''' SELECT * FROM guestbook
                            ''')
            for d in data:
                return_data.append(d)
        except sqlite3.OperationalError:
            print("No table found!")
            return []
        return return_data
