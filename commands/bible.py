import discord
import re
from discord.ext import commands
from commands.utils.pages import Pages
from commands.utils.bibleutils import BibleUtils
from commands.utils.userlevels import UserLevel

API = "https://www.abibliadigital.com.br/api"
COLOR = 0x00B115


class Bible(commands.Cog, BibleUtils):
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

    @staticmethod
    def testaments_books(books: dict) -> dict:
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
            embed = self.get_book_infos(book)
            reply = ctx.reply(embed=embed, mention_author=False)

        else:
            response = 'Tente digitar **-book Livro**'
            reply = ctx.reply(response, mention_author=False)

        await reply

    def get_book_infos(self, book) -> discord.Embed:
        book = self.get_request(f'{API}/books/{self.get_abbrev(book)}')
        embed = self.general_check(book, 'abbrev', self.bookInfos)

        return embed

    @staticmethod
    def bookInfos(book: dict) -> discord.Embed:
        testaments = {'VT': 'Antigo Testamento', 'NT': 'Novo Testamento'}

        embed = discord.Embed(color=COLOR)

        embed.add_field(name='Livro', value=book['name'], inline=False)
        embed.add_field(name='Testamento', value=testaments[book['testament']], inline=False)
        embed.add_field(name='Grupo', value=book['group'], inline=False)
        embed.add_field(name='Capítulos', value=f"{book['chapters']} caps")
        embed.add_field(name='Autor', value=book['author'])

        return embed

    @commands.command(name='verse', help='Mostra um versículo escolhido', description="Livro Capítulo:Versículo")
    async def verse(self, ctx, book: str = '', chapter_verse: str = ''):
        pattern = re.compile('\d:\d').findall(chapter_verse)

        if book and pattern:
            embed = self.get_verse(self.get_lang(ctx), book, chapter_verse)
            await ctx.reply(embed=embed, mention_author=False)
            UserLevel(ctx.author.id).give_xp(70)

        else:
            response = 'Tente digitar **-verse Livro Capítulo:Versículo**'
            await ctx.reply(response, mention_author=False)

    def get_verse(self, lang, book: str, cv: str) -> discord.Embed:
        url = f'{API}/verses/{lang}/{self.get_abbrev(book)}/{cv.replace(":", "/")}'
        verse = self.get_request(url)
        embed = self.general_check(verse, 'text', self.embed_verse)

        return embed

    @staticmethod
    def embed_verse(verse: dict) -> discord.Embed:
        title = f"{verse['book']['name']} {verse['chapter']}:{verse['number']} ({verse['book']['version'].upper()})"
        descr = verse['text']

        embed = discord.Embed(title=title, description=descr, color=COLOR)

        return embed

    @commands.command(name='randverse', help='Mostra um versículo aleatório', description="opcionalmente um Livro")
    async def randverse(self, ctx, book: str = ''):
        if not book:
            embed = self.get_random_verse(self.get_lang(ctx))
            await ctx.reply(embed=embed, mention_author=False)
            UserLevel(ctx.author.id).give_xp(70)

        else:
            embed = self.get_random_verse(self.get_lang(ctx), f'/{self.get_abbrev(book)}')
            await ctx.reply(embed=embed, mention_author=False)

    def get_random_verse(self, lang, book: str = '') -> discord.Embed:
        url = f'{API}/verses/{lang}{book}/random'
        verse = self.get_request(url)
        embed = self.general_check(verse, 'text', self.embed_verse)

        return embed

    @commands.guild_only()
    @commands.command(name='chapter', help='Mostra todos os versículos de um capítulo', description="Livro Capítulo")
    async def chapter(self, ctx, book: str = '', chapter: str = ''):
        if book and chapter:
            embeds = self.get_chapter(self.get_lang(ctx), book, chapter)
            reply = await ctx.reply(embed=embeds[0], mention_author=False)

            UserLevel(ctx.author.id).give_xp(7000)

            if len(embeds) > 1:
                pages = Pages(self.bot, ctx, reply, embeds)
                await pages.create_pages()

        else:
            response = 'Tente digitar **-chapter Livro Capítulo**'
            await ctx.reply(response, mention_author=False)

    def get_chapter(self, lang, book: str, chapter: str) -> list:
        url = f'{API}/verses/{lang}/{self.get_abbrev(book)}/{chapter}'
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

    @staticmethod
    def chapter_header(verses_lists: list, verses: dict, embeds: list) -> discord.Embed:
        title = f"{verses['book']['name']} {verses['chapter']['number']} ({verses['book']['version'].upper()})"
        descr = f'página {len(embeds)+1} de {len(verses_lists)}\n\n'
        embed = discord.Embed(
            title=title, description=descr, color=COLOR)

        return embed

    @staticmethod
    def chapter_main(embed: discord.Embed, lst: list) -> discord.Embed:
        for verse in lst:
            embed.description += f"**{verse['number']}** {verse['text']}\n\n"

        return embed

    @commands.guild_only()
    @commands.command(name='search', help='Pesquisa por palavra', description="Palavra(s)")
    async def search(self, ctx, *, search: str = ''):
        if search:
            reply = await self.loadingMessage(ctx)
            UserLevel(ctx.author.id).give_xp(10)

            await self.editsearch(ctx, reply, search)

        else:
            response = 'Tente digitar **-search** e a(s) palavra(s) você quer pesquisar'
            await ctx.reply(response, mention_author=False)

    async def loadingMessage(self, ctx):
        loadembed = self.loadembed()
        reply = await ctx.reply(embed=loadembed, mention_author=False)

        return reply

    async def editsearch(self, ctx, reply, search):
        embeds = await self.get_embeds_search(ctx, search)
        await reply.edit(embed=embeds[0])

        if len(embeds) > 1:
            pages = Pages(self.bot, ctx, reply, embeds)
            await pages.create_pages()

    async def get_embeds_search(self, ctx, search: str) -> list:
        lang = self.get_lang(ctx)
        verses = await self.post_request(lang, search)
        embeds = self.check_search(verses, search, lang)

        return embeds

    @staticmethod
    def loadembed() -> discord.Embed:
        title = 'Buscando 🔎'
        descr = 'Isso pode demorar alguns segundos'
        embed = discord.Embed(title=title, description=descr, color=COLOR)

        return embed

    def check_search(self, verses: dict, search: str, lang: str) -> list:
        if verses.get('verses'):
            embeds = self.create_embeds_search(verses, search, lang)

        else:
            embeds = self.not_results(search)

        return embeds

    @staticmethod
    def not_results(search: str) -> list:
        title = 'Nada encontrado'
        descr = f'Nenhum resultado para **{search[:55]}...**'
        embed = discord.Embed(
            title=title, description=descr, color=COLOR)

        return [embed]

    def create_embeds_search(self, verses: dict, search: str, lang: str) -> list:
        verses_lists = self.split_list(verses['verses'], 5)

        embeds = []
        for lst in verses_lists[:100]:
            embed = self.result_header(embeds, verses_lists, lang)
            embed = self.results_main(embed, lst, search)

            embeds.append(embed)

        return embeds

    @staticmethod
    def result_header(embeds: list, verses_lists: list, lang: str) -> discord.Embed:
        descr = f'página {len(embeds)+1} de {len(verses_lists[:100])}'
        embed = discord.Embed(title=f"Resultados em {lang.upper()}", description=descr, color=COLOR)

        return embed

    def results_main(self, embed: discord.Embed, lst: list, search: str) -> discord.Embed:
        for info in lst:
            verse = self.highlight_search(info['text'], search)

            name = f"{info['book']['name']} {info['chapter']}:{info['number']}"
            value = f"{verse}\n\n"

            embed.add_field(name=name, value=value, inline=False)

        return embed

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            return
        
        response = "Epa, entupigaitei X_X"
        await ctx.reply(response, mention_author=False)

        print(error)


def setup(bot):
    bot.add_cog(Bible(bot))
