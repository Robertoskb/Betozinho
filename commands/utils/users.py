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
        self.cursor.execute(f"INSERT INTO {TABLE} (id) values ({self.id})")
        
        select =self.select('id', self.id)
        if select:
            self.infos = select
        
        return self.select('id', self.id)

    def delete_user(self):
        self.cursor.execute(f"DELETE FROM {TABLE} WHERE id = {self.id}")
        rowcount = self.cursor.rowcount
        
        self.infos = self.select('id', self.id)

        return rowcount
    
    def get_rank(self, server_members):        
        select = self._select_members(server_members)
        ranks = sorted(select, key = lambda i: (i['level'], i['xp']), reverse = True)
        
        return ranks.index(self.infos) + 1
    
    def _select_members(self, server_members):
        select = f"SELECT * from {TABLE} WHERE id={self.infos['id']}"
        
        for member in server_members:
            select += f' || id = {member.id}' 
        self.cursor.execute(select)
        
        return self.cursor.fetchall()

    def _get_cursor(self):
        
        try:
            cursor = self.con.cursor(buffered=True, dictionary=True)

        except:
            self.con.reconnect()
            cursor = self.con.cursor(buffered=True, dictionary=True)

        return cursor
    
    def _get_con(self):
        con = mysql.connector.connect(
        host=config('host'), database=config('database'),
        user=config('user'), password=config('password'),
        autocommit=True, use_pure=True, raise_on_warnings=True)
        
        return con


if __name__ == "__main__":
    for i in range(700001):
        continue
    
    user = User(944347530660020314)
    
    print(user.get_rank([833810779257569350, 7121354631835581195]))
    # {'id': 944347530660020314, 'level': 1, 'xp': 0, 'description': 'Adotado! Ef 1:5'}
    # #944347530660020314 || 833810779257569350