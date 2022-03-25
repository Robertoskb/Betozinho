import random
import json
import sys
import os
from discord.ext import commands

class Random(commands.Cog):
    '''Aleatórios'''             

    def __init__(self, bot):
        self.bot =  bot
    
    @commands.command(name='sort', help='Sorteia o que você escolher', description='item1, item2, item3...')
    async def sort(self, ctx, *, items:str = None):
        if items is None: response = "Nada para sortear '-'"
        else: response = self.sort_response(ctx, items)

        await ctx.reply(response, mention_author=False)
            
    def sort_response(self, ctx, items):
        List = items.split(',')
        ramdomItem = random.choice(List)

        ofenssive = self.BotDict('offensives')
        before = self.BotDict('before')

        if random.randint(1, 101) <= 5: rsp = ofenssive.format(ctx.author.name)
        else: rsp = before + ' ' + ramdomItem.strip()

        return rsp

    def BotDict(self, mode:str) -> list:
        with open(os.path.join(sys.path[0],'dicts/dictforsmart.json'), encoding='utf-8') as j:
            Dict = json.load(j)

        return random.choice(Dict[mode])


def setup(bot):
    bot.add_cog(Random(bot))