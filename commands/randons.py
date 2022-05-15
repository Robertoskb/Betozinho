import discord
import json
import sys
import os
from discord.ext import commands
from random import randint, choice
from commands.utils.fakeinfos import get_fake_infos


class Randons(commands.Cog):
    """Aleatórios"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='sort', help='sorteia o que você escolher', description='item1, item2, item3...')
    async def sort(self, ctx, *, items: str = ''):
        response = "Nada para sortear '-'" if not items else self.sort_item(ctx, items)

        await ctx.reply(response, mention_author=False)

    def sort_item(self, ctx, items) -> str:
        return self.sort_response(ctx, choice(items.split(',')))

    def sort_response(self, ctx, item: str) -> str:
        offensive = self.bot_dict('offensives').format(ctx.author.name)
        pacific = f'{self.bot_dict("before")} {item.strip()}'

        return offensive if randint(1, 101) <= 5 else pacific

    @commands.command(name='faker', help='criar um fake', description='opcionalmente @user')
    async def faker(self, ctx, mention: discord.User = None):
        user = mention or ctx.author
        embed = await self.get_embed_faker(user)

        await ctx.reply(embed=embed, mention_author=False)

    @staticmethod
    async def get_embed_faker(user):
        embed = discord.Embed(color=0x00B115, description='')
        embed.set_thumbnail(url=user.avatar_url)

        for k, v in get_fake_infos().items():
            embed.description += f'{k}: **{v}**\n\n'

        return embed

    @staticmethod
    def bot_dict(mode: str) -> str:
        arq = os.path.join(sys.path[0], 'dicts/dictforsmart.json')

        with open(arq, encoding='utf-8') as j:
            d = json.load(j)

        return choice(d[mode])

    @faker.error
    async def faker_handler(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await self.faker(ctx)


def setup(bot):
    bot.add_cog(Randons(bot))
