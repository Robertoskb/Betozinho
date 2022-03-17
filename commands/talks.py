import random
import json
import os
import sys
from discord.ext import commands


class Talks(commands.Cog):
    """Talks with user"""

    __slots__ = ('bot', 'send', 'message', 'create_task')

    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_message(self, message) -> None:
        if message.author == self.bot.user: return

        await self.Raply(message)
        

    async def Raply(self, message):
        msgtype = self.MsgType(message)
        events = self.Responses(message)
        
        if msgtype in events:
            await message.reply(events[msgtype], mention_author=False)
            
                
    def MsgType(self, message) -> str:
        typesdict = self.BotDict('input')

        msg = message.content.lower()
        
        msgtype = ''
        for k, v in typesdict.items():
            for c, i in enumerate(typesdict[k]):
                if i in msg: msgtype = k

        return msgtype

    
    def Responses(self, message) -> dict:
        Dict = self.BotDict('responses') 

        f = message.author.name
        for k, v in Dict.items():
            Dict[k] = random.choice(v).format(f)

        return Dict

    
    def BotDict(self, mode:str) -> dict:
        with open(os.path.join(sys.path[0],'dict.json'), encoding='utf-8') as j:
            Dict = json.load(j)

        return Dict[mode]


def setup(bot):
    bot.add_cog(Talks(bot))