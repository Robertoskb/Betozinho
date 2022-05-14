import discord
from random import choice
from aiohttp import ClientSession
from discord.ext import commands
from googletrans import Translator


class Animes(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='bleach', help='Fatos de Bleach', description='Sem argumentos')
    async def bleach(self, ctx):
        facts = await self.get_request('bleach')
        embed = self.get_embed('Bleach', facts)

        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(name='bc', help='Fatos de Black Clover', description='Sem argumentos')
    async def black_clover(self, ctx):
        facts = await self.get_request('black_clover')
        embed = self.get_embed('Black Clover', facts)

        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(name='dbz', help='Fatos de Dragon Ball', description='Sem argumentos')
    async def dbz(self, ctx):
        facts = await self.get_request('dragon_ball')
        embed = self.get_embed('Dragon Ball', facts)

        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(name='jjk', help='Fatos de Jujutsu Kaisen', description='Sem argumentos')
    async def jujutsu_kaisen(self, ctx):
        facts = await self.get_request('jujutsu_kaisen')
        embed = self.get_embed('Jujutsu Kaisen', facts)

        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(name='fma', help='Fatos de FMA Brotherhood', description='Sem argumentos')
    async def fma_brotherhood(self, ctx):
        facts = await self.get_request('fma_brotherhood')
        embed = self.get_embed('FMA Brotherhood', facts)

        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(name='naruto', help='Fatos de Naruto', description='Sem argumentos')
    async def naruto(self, ctx):
        facts = await self.get_request('naruto')
        embed = self.get_embed('Naruto', facts)

        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(name='gintama', help='Fatos de Gintama', description='Sem argumentos')
    async def gintama(self, ctx):
        facts = await self.get_request('gintama')
        embed = self.get_embed('Gintama', facts)

        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(name='itachi', help='Fatos de Itachi Uchiha', description='Sem argumentos')
    async def itachi_uchiha(self, ctx):
        facts = await self.get_request('itachi_uchiha')
        embed = self.get_embed('Itachi Uchiha', facts)

        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(name='onep', help='Fatos de One Piece', description='Sem argumentos')
    async def one_piece(self, ctx):
        facts = await self.get_request('one_piece')
        embed = self.get_embed('One Piece', facts)

        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(name='ds', help='Fatos de Demon Slayer', description='Sem argumentos')
    async def demon_slayer(self, ctx):
        facts = await self.get_request('demon_slayer')
        embed = self.get_embed('Demon Slayer', facts)

        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(name='att', help='Fatos de Attack on Titan', description='Sem argumentos')
    async def attack_on_titan(self, ctx):
        facts = await self.get_request('attack_on_titan')
        embed = self.get_embed('Attack on Titan', facts)

        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(name='hxh', help='Fatos de Hunter x Hunter', description='Sem argumentos')
    async def hunter_x_hunter(self, ctx):
        facts = await self.get_request('hunter_x_hunter')
        embed = self.get_embed('Hunter x Hunter', facts)

        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(name='mha', help='Fatos de Boku no Hero Academia', description='Sem argumentos')
    async def boku_no_hero_academia(self, ctx):
        facts = await self.get_request('boku_no_hero_academia')
        embed = self.get_embed('Boku no Hero Academia', facts)

        await ctx.reply(embed=embed, mention_author=False)

    def get_embed(self, anime_name, facts):
        fact = choice(facts['data'])['fact']
        embed = discord.Embed(title=anime_name, color=0x00B115, description=self.translate(fact))
        embed.set_thumbnail(url=facts['img'])

        return embed

    @staticmethod
    async def get_request(anime_name):
        url = f'https://anime-facts-rest-api.herokuapp.com/api/v1/{anime_name}'

        async with ClientSession(trust_env=True) as Session:
            async with Session.get(url) as request:
                return await request.json()

    @staticmethod
    def translate(text): return Translator().translate(text=text, src='en', dest='pt').text

    async def cog_command_error(self, ctx, error):
        await ctx.reply("Ops, não consegui encontrar um fato '-'")

        print(error)


def setup(bot):
    bot.add_cog(Animes(bot))
