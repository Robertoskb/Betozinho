import re
import mysql.connector
from decouple import config

con = mysql.connector.connect(host=config('host'), database=config('database'),
                              user=config('user'), password=config('password'),
                              autocommit=True, use_pure=True, raise_on_warnings=True)
TABLE = 'users'


class User:

    def __init__(self, id):
        self.id = id
        self.cursor = self._get_cursor()
        self.infos = self._get_user()

    def select(self, row, value):
        self.cursor.execute(f"SELECT * from {TABLE} WHERE {row}={value}")

        return self.cursor.fetchone()

    def update_user(self, values):
        self.cursor.execute(
            f"UPDATE {TABLE} SET {values} where id = {self.id}")

        self.infos = self._get_user()

        return self.select('id', self.id)

    def create_user(self):
        if not self._get_user():
            self.cursor.execute(f"INSERT INTO {TABLE} (id) values ({self.id})")
            self.infos = self._get_user()
            
            return self.select('id', self.id)

    def delete_user(self):
        self.cursor.execute(f"DELETE FROM {TABLE} WHERE id = {self.id}")
        rowcount = self.cursor.rowcount
        self.infos = self._get_user()

        return rowcount

    def _get_cursor(self):
        try:
            cursor = con.cursor(buffered=True, dictionary=True)

        except:
            con.reconnect()
            cursor = con.cursor(buffered=True, dictionary=True)

        return cursor

    def _get_user(self):
        self.cursor.execute(f"SELECT * from {TABLE} WHERE id = {self.id}")

        return self.select('id', self.id)


if __name__ == "__main__":
    user = User(944347530660020314)

    print(user.infos) # {'id': 944347530660020314, 'level': 1, 'xp': 0, 'description': 'Adotado! Ef 1:5'}

    user.cursor.close()
