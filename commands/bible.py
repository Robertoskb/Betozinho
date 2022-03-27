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

    @commands.command(name='books', help='Mostra os livros da Bíblia', description="opcionalmente VT ou NT")
    async def books(self, ctx, testament:str=None):
        
        if testament is None:
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
            
    
    def bookInfos(self, abbrev) -> discord.Embed:
        book = self.get_request(f'{API}/books/{abbrev}')
        testaments = {'VT':'Antigo Testamento', 'NT':'Novo Testamento'}

        embed = discord.Embed(color=0x00B115)
        
        embed.add_field(name='Livro', value=book['name'], inline=False)
        embed.add_field(name='Testamento', value=testaments[book['testament']], inline=False)
        embed.add_field(name='Grupo', value=book['group'], inline=False)
        embed.add_field(name='Capítulos', value=f"{book['chapters']} caps")
        embed.add_field(name='Autor', value=book['author'])

        return embed


    @commands.command(name='verse', help='Mostra versículos da Bíblia', description="Livro Capítulo:Versículo")
    async def verse(self, ctx, book:str='', chapter_verse:str=''):
        book = unidecode(book).lower()

        pattern = bool(re.compile('.:.').findall(chapter_verse))

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
        request = self.get_request(url)

        if 'text' in request:
            title = f"{request['book']['name']} {cv[0]}:{cv[1]}"
            descr = request['text']
        
        else:
            title = "Nada encontrado"
            descr = "Verifique se você digitou **Capítulo:Versículo** existentes"

        embed = discord.Embed(title=title, description=descr, color=0x00B115)
        
        return embed


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