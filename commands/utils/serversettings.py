import mysql.connector
import json
import os
import sys
import time
from decouple import config


con = mysql.connector.connect(host=config('host'), database=config('database'),
                              user=config('user'), password=config('password'),
                              autocommit=True, use_pure=True, raise_on_warnings=True)
TABLE = 'serversettings'


class ServerSettings():

    def __init__(self, server):
        self.cursor = self._get_cursor()
        self.server = self._checkServer(server)

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
            cursor = con.cursor(buffered=True, dictionary=True)

        except:
            con.reconnect()
            cursor = con.cursor(buffered=True, dictionary=True)

        return cursor


if __name__ == '__main__':
    start = time.time()
    
    server = ServerSettings(947912008957845524) 
    print(server.get_settings())

    server.cursor.close()

    end = time.time()

    print(f'Tempo de execução: {end - start}s')

_ = 947912008957845524
