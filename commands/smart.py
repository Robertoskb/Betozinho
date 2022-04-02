import json
import sys
import os
from discord.ext import commands
from random import randint, choice


class Random(commands.Cog):
    '''Aleatórios'''

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='sort', help='Sorteia o que você escolher', description='item1, item2, item3...')
    async def sort(self, ctx, *, items: str = ''):
        if not items:
            response = "Nada para sortear '-'"

        else:
            response = self.sort_item(ctx, items)

        await ctx.reply(response, mention_author=False)

    def sort_item(self, ctx, items) -> str:
        List = items.split(',')
        item = choice(List)

        return self.sort_response(ctx, item)

    def sort_response(self, ctx, item: str) -> str:
        ofenssive = self.BotDict('offensives')
        before = self.BotDict('before')

        ofenssive = ofenssive.format(ctx.author.name)
        parcific = f'{before} {item.strip()}'

        if randint(1, 101) <= 5:
            return ofenssive

        else:
            return parcific

    def BotDict(self, mode: str) -> list:
        arq = os.path.join(sys.path[0], 'dicts/dictforsmart.json')
        with open(arq, encoding='utf-8') as j:
            Dict = json.load(j)

        return choice(Dict[mode])


def setup(bot):
    bot.add_cog(Random(bot))