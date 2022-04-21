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

def Settings(id: int, value: str):
	def filt(x): return x['id'] == id
	result = list(filter(filt, open_json(id)))
	check = check_index(result)
    
	return check.get(value)

def open_json(id):
	arq = os.path.join(sys.path[0], 'commands/utils/db.json')
	
	try:
		file = open(arq, 'r',encoding='utf-8')
		lst = json.load(file)

	except:
		file = open(arq, 'wt+',encoding='utf-8')
		ServerSettings(id).updateFile()
		lst = json.load(file)
	
	finally:
		file.close()
    
	return lst

def check_index(lst):
    try:
        item = lst[0]
    
    except IndexError:
        item = {}
    
    return item

class ServerSettings():

	def __init__(self, server):
		self.cursor = self.get_cursor()
		self.server = self.checkServer(server)

	def insert(self, row, value):
		self.cursor.execute(f"INSERT INTO {TABLE} ({row}) values ('{value}')")
		self.updateFile()

		return self.select(row, value)

	def update(self, values):
		self.cursor.execute(
			f"UPDATE {TABLE} SET {values} where id = {self.server}")

		self.updateFile()

		return self.select('id', self.server)
	
	def updateFile(self):
		self.cursor.execute(f"SELECT * from {TABLE}")

		arq = os.path.join(sys.path[0], 'commands/utils/db.json')
		with open(arq, 'w+', encoding='utf-8') as file:
			json.dump(self.cursor.fetchall(), file)

	def select(self, row, value):
		self.cursor.execute(f"SELECT * from {TABLE} WHERE {row}={value}")

		return self.cursor.fetchone()
		
	def reset(self):
		select = self.select('id', self.server)

		values = ' '
		for row in select.keys():
			if row == 'id': continue
			values += f'{row}=DEFAULT,'
		
		self.update(values[:-1])

		return self.select('id', self.server)
	
	def checkServer(self, server):
		select = self.select('id', server)
		
		if select is None:
			select = self.insert('id', server)
		
		return select.get('id')
	
	def get_cursor(self):
		try:
			cursor = con.cursor(buffered=True, dictionary=True)

		except:
			con.reconnect()
			cursor = con.cursor(buffered=True, dictionary=True)
		
		return cursor

if __name__ == '__main__':
	start = time.time()

	print(Settings(947912008957845524, 'talks'))

	server = ServerSettings(1)
	server.reset()
	

	end = time.time()

	print(f'Tempo de execução: {end - start}s')

_ = 947912008957845524