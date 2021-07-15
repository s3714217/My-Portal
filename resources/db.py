import sqlite3
from datetime import datetime
import secrets
class GuestBookDatabase:

    def __init__(self):
        self.token_con = sqlite3.connect('token.db')

    def generate_token(self):
        return secrets.token_urlsafe(10)

    def initialize_guestbook(self):
        cur = self.guestbook_con.cursor()
        cur.execute(''' DROP TABLE if EXISTS guestbook ''')
        cur.execute(''' CREATE TABLE guestbook (date text, name text, message text); ''')
        self.guestbook_con.commit()
        cur.close()

    def new_guestbook_message(self, message):
        cur = self.guestbook_con.cursor()
        try:
            cur.execute(''' INSERT INTO guestbook (date,name,message)
                        VALUES(?,?,?); ''', (message[0],message[1],message[2]))
            self.guestbook_con.commit()
            cur.close()
        except sqlite3.OperationalError:
            self.initialize_guestbook()
            self.new_guestbook_message(message)

    def get_guestbook_message(self):
        return_data = []
        cur = self.guestbook_con.cursor()
        try:
            data = cur.execute(''' SELECT * FROM guestbook
                            ''')
            for d in data:
                return_data.append(d)
        except sqlite3.OperationalError:
            print("No table found!")
            return []
        return return_data

class TokenDatabase:

    def __init__(self):
        self.token_con = sqlite3.connect('token.db')

    def initialize_token(self):
        cur = self.token_con.cursor()
        cur.execute(''' DROP TABLE if EXISTS token ''')
        cur.execute(''' CREATE TABLE token (token text, created_date text); ''')
        self.token_con.commit()
        cur.close()

    def new_token(self):
        cur = self.token_con.cursor()
        try:
            token_list = self.get_token_list()
            token = self.generate_token()
            while self.token_validator(token_list, token) is False:
                token = self.generate_token()
         
            cur.execute(''' INSERT INTO token (token,created_date)
                        VALUES(?,?); ''', (token, datetime.now() ))
            self.token_con.commit()
            cur.close()
            return token
        except sqlite3.OperationalError:
            self.initialize_token()
            return self.new_token()
        
    def get_token_list(self):
        return_data = []
        cur = self.token_con.cursor()
        try:
            data = cur.execute(''' SELECT * FROM token
                            ''')
            for d in data:
                return_data.append(d)
            cur.close()
        except sqlite3.OperationalError:
           return []
        return return_data

    def token_validator(self, token_list, token):
        for t in token_list:
            if t == token:
                return False
        return True

    def remove_token(self, token):
        cur = self.token_con.cursor()
        cur.execute(''' DELETE FROM token
                                WHERE token = ?;
                            ''', [token] )
        self.token_con.commit()
        cur.close()

class UserDatabase:
    def __init__(self):
        self.token_con = sqlite3.connect('user.db')


