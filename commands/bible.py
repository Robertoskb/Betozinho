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


    @commands.command(name='verse', help='Mostra versículos da Bíblia', description="Livro Capítulo:Versículo")
    async def verse(self, ctx, book:str='', chapter_verse:str=''):
        book = unidecode(book).lower()
        pattern = self.check_pattern('.:.', chapter_verse)

        if book in self.BibleBooks() and pattern:
            abbrev = self.BibleBooks()[book]
            embed = self.get_verse(abbrev, chapter_verse)

            await ctx.reply(embed=embed, mention_author = False)

        else:
            response = 'Por favor, tente digitar **-verse Livro Capítulo:Versículo** corretamente'

            await ctx.reply(response, mention_author = False)

        
    def get_verse(self, abbrev:str, cv:str) -> discord.Embed:
        cv = cv.split(':')
        url = f'{API}/verses/nvi/{abbrev}/{cv[0]}/{cv[1]}'
        request = self.get_request(url)

        if 'text' in request:
            title = f"{request['book']['name']} {cv[0]}:{cv[1]}"
            descr = request['text']
        
        else:
            title = "Nada encontrado"
            descr = "Verifique se você digitou **-verse Livro Capítulo:Versículos** existentes"

        embed = discord.Embed(title=title, description=descr, color=0x00B115)
        
        return embed


    def check_pattern(self, pattern:str, text:str) -> bool:
        return bool(re.compile(pattern).findall(text))


    def get_request(self, url:str) -> dict:
        return requests.get(url, headers={'Authorization': 'Beare {}'.format(BIBLE)}).json()


    def BibleBooks(self) -> str:
        arq = os.path.join(sys.path[0],'dicts/dictforbible.json')
        with open(arq, encoding='utf-8') as j:
            Dict = json.load(j)

        return Dict

    # async def CreateEmbeds(self, ctx, textlist, request):
    #     '''Envia versículos como mensagem no discord, a cada 25 versículos é 
    #        criada uma nova mensagem por conta da limitção de caracteres'''

    #     limit = 25
    #     newtextlist = [textlist[i:i + limit] for i in range(0, len(textlist), limit)]

    #     for list in newtextlist:
    #         response = '\n\n'.join(list)
            
    #         embed = discord.Embed(description=response, color = 0x00B115)
    #         embed.set_author(name=request['reference'], icon_url=ctx.author.avatar_url)

    #         await ctx.channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Bible(bot)) 