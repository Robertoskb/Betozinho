import mysql.connector
from decouple import config

TABLE = 'users'


class User:

    def __init__(self, id):
        self.id = id
        self.con = self._get_con()
        self.cursor = self._get_cursor()
        self.infos = self.select('id', self.id)
        
    def __del__(self):
        if self.con.is_connected():
            self.con.close()
            self.cursor.close()
            
    def select(self, row, value):
        self.cursor.execute(f"SELECT * from {TABLE} WHERE {row}={value}")

        return self.cursor.fetchone()

    def update_user(self, values):
        self.cursor.execute(
            f"UPDATE {TABLE} SET {values} where id = {self.id}")

        self.infos = self.select('id', self.id)

        return self.select('id', self.id)

    def create_user(self):
        if not self.select('id', self.id):
            self.cursor.execute(f"INSERT INTO {TABLE} (id) values ({self.id})")
            self.infos = self.select('id', self.id)
            
            return self.infos

    def delete_user(self):
        self.cursor.execute(f"DELETE FROM {TABLE} WHERE id = {self.id}")
        rowcount = self.cursor.rowcount
        
        self.infos = self.select('id', self.id)

        return rowcount
    
    def get_rank(self, server_members):        
        select = self._select_members(server_members)
        ranks = sorted(select, key=lambda i: (i['level'], i['xp']), reverse=True)
        
        return ranks.index(self.infos) + 1
    
    def _select_members(self, server_members):
        select = f"SELECT * from {TABLE} WHERE id={self.infos['id']}"
        
        for member in server_members:
            select += f' || id = {member.id}' 
        self.cursor.execute(select)
        
        return self.cursor.fetchall()
    
    def get_needed_xp(self):
        xp = self.infos['xp']

        if self.infos['level'] < 7:
            xp = f'{xp}/{self.infos["level"]*20000}'
            
        return xp

    def _get_cursor(self):
        try:
            cursor = self.con.cursor(buffered=True, dictionary=True)

        except:
            self.con.reconnect()
            cursor = self.con.cursor(buffered=True, dictionary=True)

        return cursor
    
    @staticmethod
    def _get_con():
        con = mysql.connector.connect(
        host=config('host'), database=config('database'),
        user=config('user'), password=config('password'),
        autocommit=True, use_pure=True, raise_on_warnings=True)
        
        return con