import requests
import discord
import re
import sys
import os
import json
from discord.ext import commands
from decouple import config
from unidecode import unidecode

BIBLE = config('bible')
API = "https://www.abibliadigital.com.br/api"

class Bible(commands.Cog):
	'''Bíblia'''

	def __init__(self, bot):
		self.bot = bot

	@commands.command(name='books', help='Mostra todos os livros da Bíblia', description="opcionalmente VT ou NT")
	async def books(self, ctx, testament:str=''):
		
		if not testament:
			embed = self.get_books()
		
		elif testament.upper() in ['VT', 'NT']:
			embed = self.especificBooks(testament.upper())
		
		else:
			response = 'Tente digitar **-books** e opcionalmente **VT ou NT**'
			return await ctx.reply(response, mention_author=False)

		await ctx.reply(embed=embed, mention_author=False)

	
	def get_books(self) -> discord.Embed:
		books = self.get_request(f'{API}/books')

		vt = nt = ''
		for book in books:
			if book['testament'] == 'VT':
				vt += f'{book["name"]}\n'
			else: 
				nt += f'{book["name"]}\n'
		
		embed = discord.Embed(color=0x00B115)
		embed.add_field(name='Antigo Testamento', value=vt)
		embed.add_field(name='Novo Testamento', value=nt)

		return embed

	
	def especificBooks(self, testament) -> discord.Embed:
		books = self.get_request(f'{API}/books')
		testaments = {'VT':'Antigo Testamento', 'NT':'Novo Testamento'}

		value = ''
		for book in books:
			if book['testament'] == testament:
				value += f'{book["name"]}\n'

		embed = discord.Embed(color=0x00B115)
		embed.add_field(name=testaments[testament], value=value)

		return embed
		
	
	@commands.command(name='book', help='Informações de um livro Bíblia', description="Livro")
	async def book(self, ctx, book:str=''):
		
		book = unidecode(book).lower()
		books = self.BibleBooks()

		if book in books:
			abbrev = books[book]
			embed = self.bookInfos(abbrev)

			await ctx.reply(embed=embed, mention_author=False)
		
		else:
			response = 'Tente digitar **-book Livro** corretamente'
			
			await ctx.reply(response, mention_author=False)
			
	
	def bookInfos(self, abbrev:str) -> discord.Embed:
		book = self.get_request(f'{API}/books/{abbrev}')
		testaments = {'VT':'Antigo Testamento', 'NT':'Novo Testamento'}

		embed = discord.Embed(color=0x00B115)
		
		embed.add_field(name='Livro', value=book['name'], inline=False)
		embed.add_field(name='Testamento', value=testaments[book['testament']], inline=False)
		embed.add_field(name='Grupo', value=book['group'], inline=False)
		embed.add_field(name='Capítulos', value=f"{book['chapters']} caps")
		embed.add_field(name='Autor', value=book['author'])

		return embed


	@commands.command(name='verse', help='Mostra um versículo escolhido', description="Livro Capítulo:Versículo")
	async def verse(self, ctx, book:str='', chapter_verse:str=''):
		book = unidecode(book).lower()

		pattern = re.compile('.:.').findall(chapter_verse)

		books  = self.BibleBooks()

		if book in books and pattern:
			abbrev = books[book]
			embed = self.get_verse(abbrev, chapter_verse)

			await ctx.reply(embed=embed, mention_author=False)

		else:
			response = 'Tente digitar **-verse Livro Capítulo:Versículo** corretamente'

			await ctx.reply(response, mention_author=False)

		
	def get_verse(self, abbrev:str, cv:str) -> discord.Embed:
		cv = cv.split(':')
		url = f'{API}/verses/nvi/{abbrev}/{cv[0]}/{cv[1]}'
		verse = self.get_request(url)

		if 'text' in verse:
			title = f"{verse['book']['name']} {cv[0]}:{cv[1]}"
			descr = verse['text']
		
		else:
			title = "Nada encontrado"
			descr = "Verifique se você digitou **Capítulo:Versículo** existentes"

		embed = discord.Embed(title=title, description=descr, color=0x00B115)
		
		return embed


	@commands.command(name='chapter', help='Mostra todos os versículos de um capítulo', description="Livro Capítulo")
	async def chapter(self, ctx, book:str='', chapter:str=''):
		book = unidecode(book).lower()
		books = self.BibleBooks()

		if book in books and chapter:
			abbrev = books[book]
			embeds = self.get_chapter(abbrev, chapter)

			for embed in embeds:
				await ctx.reply(embed=embed, mention_author=False)

		else:
			response = 'Tente digitar **-chapter Livro Capítulo** corretamente'
			
			await ctx.reply(response, mention_author=False)


	def get_chapter(self, abbrev:str, chapter:str) -> list:
		url = f'{API}/verses/nvi/{abbrev}/{chapter}'
		chap = self.get_request(url)

		if 'verses' in chap:
			embeds = self.get_embeds_verses(chap)

			return embeds

		else:
			title = 'Capítulo não encontrado'
			descr = 'Digite um capítulo existente no livro'
			embed = discord.Embed(title=title, description=descr, color=0x00B115)

			return [embed]

				
	def get_embeds_verses(self, verses:dict) -> list:
		verses_list = [v for v in verses['verses']]

		verses_list = self.split_list(verses_list, 25)

		return self.create_embeds_verses(verses, verses_list)
	
  
	def create_embeds_verses(self, verses:dict, verses_list:list) -> list:
		embeds = []
		for lst in verses_list:
			title = f"{verses['book']['name']} {verses['chapter']['number']}"
			embed = discord.Embed(title=title, color=0x00B115)
			
			text = ''
			for verse in lst:
				text += f"**{verse['number']}** {verse['text']}\n\n"
			
			embed.description = text
			embeds.append(embed)
		
		return embeds


	def split_list(self, lst:list, limit:int) -> list:
		for i in range(0, len(lst), limit):
			yield lst[i:i+limit]


	@commands.command(name='search', help='Pesquisa por palavra', description="Palavra(s)")
	async def search(self, ctx, *, search:str=''):
		if search:
			embed = self.get_embed_search(search)
			await ctx.reply(embed=embed,  mention_author=False)

		else:
			response = 'Tente digitar **-search** e a(s) palavra(s) que queira pesquisar'
			await ctx.reply(response,  mention_author=False)

		
	def get_embed_search(self, search:str) -> discord.Embed:
		verses = self.post_request(search)

		if 'verses' in verses and verses['verses']:
			embed = self.create_embed_search(verses, search)

		else:
			title = 'Nada encontrado'
			descr = f'Nenhum resultado para **{search[:55]}...**'
			embed = discord.Embed(title=title, description=descr, color=0x00B115)

		return embed
	

	def create_embed_search(self, verses:list, search:str) -> discord.Embed:
		embed = discord.Embed(title='Resultados', color=0x00B115)
		
		for i in verses['verses'][:5]:
			verse = self.highlight_search(i['text'], search)
				
			name = f"{i['book']['name']} {i['chapter']}:{i['number']}"
			value = f"{verse}\n\n"

			embed.add_field(name=name, value=value, inline=False)
		
		return embed

	
	def highlight_search(self, text:str, search:str) -> str:
		for w in search.split():
			case1 = f'**{w}' in text
			case2 =  f'{w}**' in text

			if case1 or case2: continue
			else: text = text.replace(w, f'**{w}**')

		return text


	def post_request(self, search:str) -> dict:
		data = {"version": "nvi", "search": search}
		headers = {'Authorization': f'Beare {BIBLE}'}
		url = f'{API}/verses/search'
		
		request = requests.post(url, json=data, headers=headers)

		return request.json()


	def get_request(self, url:str) -> dict:
		headers = {'Authorization': f'Beare {BIBLE}'}

		return requests.get(url, headers=headers).json()


	def BibleBooks(self) -> dict:
		arq = os.path.join(sys.path[0],'dicts/dictforbible.json')
		with open(arq, encoding='utf-8') as j:
			Dict = json.load(j)

		return Dict

def setup(bot):
	bot.add_cog(Bible(bot)) 
