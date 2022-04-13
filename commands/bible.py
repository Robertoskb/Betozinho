import requests
import discord
import re
import sys
import os
import json
import asyncio
from discord.ext import commands
from decouple import config
from unidecode import unidecode
from aiohttp import ClientSession

API = "https://www.abibliadigital.com.br/api"
HEADERS = {'Authorization': f'Beare {config("bible")}'}
COLOR = 0x00B115


class Bible(commands.Cog):
    '''Bíblia'''

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='books', help='Mostra todos os livros da Bíblia', description="opcionalmente VT ou NT")
    async def books(self, ctx, testament: str = ''):
        if not testament:
            embed = self.allBooks()

        elif testament.upper() in ['VT', 'NT']:
            embed = self.especificBooks(testament.upper())

        else:
            response = 'Tente digitar **-books** e opcionalmente **VT ou NT**'

            return await ctx.reply(response, mention_author=False)

        await ctx.reply(embed=embed, mention_author=False)

    def allBooks(self) -> discord.Embed:
        books = self.get_request(f'{API}/books')
        value = self.testaments_books(books)

        embed = discord.Embed(color=COLOR)
        embed.add_field(name='Antigo Testamento', value=value['VT'])
        embed.add_field(name='Novo Testamento', value=value['NT'])

        return embed

    def especificBooks(self, testament: str) -> discord.Embed:
        books = self.get_request(f'{API}/books')
        testaments = {'VT': 'Antigo Testamento', 'NT': 'Novo Testamento'}

        value = self.testaments_books(books)

        embed = discord.Embed(color=COLOR)
        embed.add_field(name=testaments[testament], value=value[testament])

        return embed

    def testaments_books(self, books: dict) -> dict:
        testaments = {'VT': '', 'NT': ''}
        for book in books:
            if book['testament'] == 'VT':
                testaments['VT'] += f'{book["name"]} | '
            else:
                testaments['NT'] += f'{book["name"]} | '

        return testaments

    @commands.command(name='book', help='Informações sobre um livro da Bíblia', description="Livro")
    async def book(self, ctx, book: str = ''):
        if book:
            embed = self.check_book(book)
            reply = ctx.reply(embed=embed, mention_author=False)

        else:
            response = 'Tente digitar **-book Livro**'
            reply = ctx.reply(response, mention_author=False)

        await reply

    def check_book(self, book: str) -> discord.Embed:
        book = self.get_request(f'{API}/books/{self.get_abbrev(book)}')

        if book.get('abbrev'):
            embed = self.bookInfos(book)

        else:
            embed = self.request_msg(book.get('msg'))

        return embed

    def bookInfos(self, book: dict) -> discord.Embed:
        testaments = {'VT': 'Antigo Testamento', 'NT': 'Novo Testamento'}

        embed = discord.Embed(color=COLOR)

        embed.add_field(name='Livro', value=book['name'], inline=False)
        embed.add_field(name='Testamento',
                        value=testaments[book['testament']], inline=False)
        embed.add_field(name='Grupo', value=book['group'], inline=False)
        embed.add_field(name='Capítulos', value=f"{book['chapters']} caps")
        embed.add_field(name='Autor', value=book['author'])

        return embed

    @commands.command(name='verse', help='Mostra um versículo escolhido', description="Livro Capítulo:Versículo")
    async def verse(self, ctx, book: str = '', chapter_verse: str = ''):
        pattern = re.compile('.:.').findall(chapter_verse)

        if book and pattern:
            embed = self.get_verse(book, chapter_verse)
            reply = ctx.reply(embed=embed, mention_author=False)

        else:
            response = 'Tente digitar **-verse Livro Capítulo:Versículo**'
            reply = ctx.reply(response, mention_author=False)

        await reply

    def get_verse(self, book: str, cv: str) -> discord.Embed:
        cv = cv.split(':')
        url = f'{API}/verses/nvi/{self.get_abbrev(book)}/{cv[0]}/{cv[1]}'
        verse = self.get_request(url)

        return self.check_verse(verse)

    def check_verse(self, verse) -> discord.Embed:
        if 'text' in verse:
            embed = self.embed_verse(verse)

        else:
            embed = self.request_msg(verse.get('msg'))

        return embed

    def embed_verse(self, verse: dict) -> discord.Embed:
        title = f"{verse['book']['name']} {verse['chapter']}:{verse['number']}"
        descr = verse['text']

        embed = discord.Embed(title=title, description=descr, color=COLOR)

        return embed

    @commands.command(name='randverse', help='Mostra um versículo aleatório', description="opcionalmente um Livro")
    async def randverse(self, ctx, book: str = ''):
        if not book:
            embed = self.get_random_verse()
            reply = ctx.reply(embed=embed, mention_author=False)

        else:
            embed = self.get_random_verse(f'/{self.get_abbrev(book)}')
            reply = ctx.reply(embed=embed, mention_author=False)

        await reply

    def get_random_verse(self, book: str = '') -> discord.Embed:
        url = f'{API}/verses/nvi{book}/random'
        verse = self.get_request(url)
        embed = self.check_randverse(verse)

        return embed

    def check_randverse(self, verse: dict) -> discord.Embed:
        if verse.get('text'):
            return self.create_embed_random_verse(verse)

        else:
            return self.request_msg(verse.get('msg'))

    def create_embed_random_verse(self, verse: dict) -> discord.Embed:
        title = f"{verse['book']['name']} {verse['chapter']}:{verse['number']}"
        embed = discord.Embed(
            title=title, description=verse['text'], color=COLOR)

        return embed

    @commands.command(name='chapter', help='Mostra todos os versículos de um capítulo', description="Livro Capítulo")
    async def chapter(self, ctx, book: str = '', chapter: str = ''):
        if ctx.channel.type == discord.ChannelType.private:
            return

        if book and chapter:
            embeds = self.get_chapter(book, chapter)
            reply = await ctx.reply(embed=embeds[0], mention_author=False)

            if len(embeds) > 1:
                await self.create_pages(ctx, reply, embeds)

        else:
            response = 'Tente digitar **-chapter Livro Capítulo**'
            await ctx.reply(response, mention_author=False)

    def get_chapter(self, book: str, chapter: str) -> list:
        url = f'{API}/verses/nvi/{self.get_abbrev(book)}/{chapter}'
        chap = self.get_request(url)
        embeds = self.check_chapter(chap)

        return embeds

    def check_chapter(self, chap: dict) -> list:
        if chap.get('verses'):
            embeds = self.get_embeds_verses(chap)

        else:
            embeds = [self.request_msg(chap.get('msg'))]

        return embeds

    def get_embeds_verses(self, verses: dict) -> list:
        verses_list = [v for v in verses['verses']]
        verses_lists = self.split_list(verses_list, 15)

        return self.create_embeds_verses(verses, verses_lists)

    def create_embeds_verses(self, verses: dict, verses_lists: list) -> list:
        embeds = []
        for lst in verses_lists:
            embed = self.chapter_header(verses_lists, verses, embeds)
            embed = self.chapter_main(embed, lst)

            embeds.append(embed)

        return embeds

    def chapter_header(self, verses_lists: list, verses: dict, embeds: list) -> discord.Embed:
        title = f"{verses['book']['name']} {verses['chapter']['number']}"
        descr = f'página {len(embeds)+1} de {len(verses_lists)}\n\n'
        embed = discord.Embed(
            title=title, description=descr, color=COLOR)

        return embed

    def chapter_main(self, embed: discord.Embed, lst: list) -> discord.Embed:
        text = ''
        for verse in lst:
            text += f"**{verse['number']}** {verse['text']}\n\n"

        embed.description += text

        return embed

    @commands.command(name='search', help='Pesquisa por palavra', description="Palavra(s)")
    async def search(self, ctx, *, search: str = ''):
        if ctx.channel.type == discord.ChannelType.private:
            return

        if search:
            reply = await self.loadingMessage(ctx)
            await self.editsearch(ctx, reply, search)

        else:
            response = 'Tente digitar **-search** e a(s) palavra(s) você quer pesquisar'
            await ctx.reply(response, mention_author=False)

    async def loadingMessage(self, ctx):
        loadembed = self.loadembed()
        reply = await ctx.reply(embed=loadembed, mention_author=False)

        return reply

    async def editsearch(self, ctx, reply, search):
        embeds = await self.get_embeds_search(search)
        await reply.edit(embed=embeds[0])

        if len(embeds) > 1:
            await self.create_pages(ctx, reply, embeds)

    async def get_embeds_search(self, search: str) -> list:
        verses = await self.post_request(search)
        embeds = self.check_search(verses, search)

        return embeds

    def loadembed(self) -> discord.Embed:
        title = 'Buscando 🔎'
        descr = 'Isso pode demorar alguns segundos'
        embed = discord.Embed(title=title, description=descr, color=COLOR)

        return embed

    def check_search(self, verses, search: str) -> list:
        if verses.get('verses'):
            embeds = self.create_embeds_search(verses, search)

        else:
            embeds = self.not_results(search)

        return embeds

    def not_results(self, search: str) -> list:
        title = 'Nada encontrado'
        descr = f'Nenhum resultado para **{search[:55]}...**'
        embed = discord.Embed(
            title=title, description=descr, color=COLOR)

        return [embed]

    def create_embeds_search(self, verses: list, search: str) -> list:
        verses_lists = self.split_list(verses['verses'], 5)

        embeds = []
        for lst in verses_lists[:100]:
            embed = self.result_header(embeds, verses_lists)
            embed = self.results_main(embed, lst, search)

            embeds.append(embed)

        return embeds

    def result_header(self, embeds: list, verses_lists: list) -> discord.Embed:
        descr = f'página {len(embeds)+1} de {len(verses_lists[:100])}'
        embed = discord.Embed(title='Resultados',
                              description=descr, color=COLOR)

        return embed

    def results_main(self, embed: discord.Embed, lst: list, search: str) -> discord.Embed:
        for info in lst:
            verse = self.highlight_search(info['text'], search)

            name = f"{info['book']['name']} {info['chapter']}:{info['number']}"
            value = f"{verse}\n\n"

            embed.add_field(name=name, value=value, inline=False)

        return embed

    def highlight_search(self, text: str, search: str) -> str:
        for w in search.split():
            case1 = f'**{w}' in text
            case2 = f'{w}**' in text

            if case1 or case2:
                continue
            else:
                text = text.replace(w, f'**{w}**')

        return text

    def split_list(self, lst: list, limit: int) -> list:
        newlist = [lst[i:i + limit] for i in range(0, len(lst), limit)]

        return newlist

    def get_request(self, url: str) -> dict:
        request = requests.get(url, headers=HEADERS)
        return request.json()

    def request_msg(self, msg: str) -> discord.Embed:
        msgs = {
            'Book not found': 'Livro não econtrado',
            'Chapter not found': 'Capítulo não econtrado',
            'Verse not found': 'Versículo não econtrado',
        }

        response = msgs.get(msg) or 'Erro desconhecido'
        embed = discord.Embed(title='Nada encontrado', description=response, color=COLOR)

        return embed

    async def post_request(self, search: str) -> dict:
        data = {"version": "nvi", "search": search}
        url = f'{API}/verses/search'

        async with ClientSession(trust_env=True) as Session:
            async with Session.post(url, headers=HEADERS, json=data) as request:
                return await request.json()

    async def create_pages(self, ctx, reply, embeds: list):
        await reply.add_reaction("◀️")
        await reply.add_reaction("▶️")

        def check(react, usr):
            return usr == ctx.author and str(react.emoji) in ["◀️", "▶️"]

        await self.timeout_pages(reply, embeds, check)

    async def timeout_pages(self, reply, embeds: list, check):
        cur_page = 0
        while True:
            try:
                reaction, user = await self.bot.wait_for("reaction_add", timeout=600, check=check)
                cur_page = await self.switch_pages(reply, embeds, reaction, user, cur_page)

            except asyncio.TimeoutError:
                await reply.remove_reaction("◀️", self.bot.user)
                await reply.remove_reaction("▶️", self.bot.user)

                break

    async def switch_pages(self, reply, embeds, reaction, user, cur_page: int) -> int:
        if str(reaction.emoji) == "▶️" and cur_page != len(embeds) - 1:
            cur_page += 1
            await reply.edit(embed=embeds[cur_page])
            await reply.remove_reaction(reaction, user)

        elif str(reaction.emoji) == "◀️" and cur_page > 0:
            cur_page -= 1
            await reply.edit(embed=embeds[cur_page])
            await reply.remove_reaction(reaction, user)

        else:
            await reply.remove_reaction(reaction, user)

        return cur_page

    def get_abbrev(self, book: str) -> dict:
        arq = os.path.join(sys.path[0], 'dicts/dictforbible.json')
        with open(arq, encoding='utf-8') as j:
            Dict = json.load(j)

        return Dict.get(unidecode(book).lower())

    async def cog_command_error(self, ctx, error):
        response = "Epa, entupigaitei X_X"
        await ctx.reply(response, mention_author=False)

        print(error)


def setup(bot):
    bot.add_cog(Bible(bot))
