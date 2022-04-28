import mysql.connector
from decouple import config
import time


TABLE = 'serversettings'


class ServerSettings():

    def __init__(self, server):
        self.con = self._get_con()
        self.cursor = self._get_cursor()
        self.server = self._checkServer(server)
    
    def __del__(self):
        if self.con.is_connected():
            self.con.close()
            self.cursor.close()

    def insert(self, row, value):
        self.cursor.execute(f"INSERT INTO {TABLE} ({row}) values ({value})")
        
        return self.select(row, value)

    def update(self, values):
        self.cursor.execute(
            f"UPDATE {TABLE} SET {values} where id = {self.server}")

        return self.select('id', self.server)

    def select(self, row, value):
        self.cursor.execute(f"SELECT * from {TABLE} WHERE {row}={value}")

        return self.cursor.fetchone()
    
    def get_settings(self, row=None):
        select = self.select('id', self.server)
        
        get = select if row is None else select.get(row)
        
        return get

    def reset(self):
        select = self.select('id', self.server)
        defaults = self._get_defaults(select)
        
        self.update(defaults)
        
        return self.select('id', self.server)

    def _get_defaults(self, select):
        values = ' '
        for row in select.keys():
            if row == 'id':
                continue
            values += f'{row} = DEFAULT,'
        
        return values[:-1]

    def _checkServer(self, server):
        select = self.select('id', server)

        if select is None:
            select = self.insert('id', server)

        return select.get('id')

    def _get_cursor(self):
        try:
            cursor = self.con.cursor(buffered=True, dictionary=True)

        except:
            self.con.reconnect()
            cursor = self.con.cursor(buffered=True, dictionary=True)

        return cursor
    
    def _get_con(self):
        con = mysql.connector.connect(host=config('host'), database=config('database'),
        user=config('user'), password=config('password'),
        autocommit=True, use_pure=True, raise_on_warnings=True)
        
        return con
