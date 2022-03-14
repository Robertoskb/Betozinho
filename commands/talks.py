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
        self.send = None
        self.message = None
        self.create_task = self.bot.loop.create_task


    @commands.Cog.listener()
    async def on_message(self, message) -> None:
        if message.author == self.bot.user: return

        self.message = message
        self.send = lambda rsp: message.channel.send(
        rsp, reference=message, mention_author=False)
        
        self.Response()
        

    def Response(self):
        msgtype = self.MsgType()
        events = self.Responses()
        
        if msgtype in events:
            return self.create_task(self.send(events[msgtype]))
            
                
    def MsgType(self) -> str:
        typesdict = self.TypeNames()

        msg = self.message.content.lower()
        
        msgtype = ''
        for k, v in typesdict.items():
            for c, i in enumerate(typesdict[k]):
                if i in msg: msgtype = k

        return msgtype

    
    def Responses(self) -> dict:
        Random = lambda m, t: random.choice(self.BotDict(m, t)).format(self.message.author.name)

        events = {
            'laughs': 'hehe',
            'mua': 'muaa',
            'smilings' : Random('responses','smilings'),
            'ibackmoment': 'ok',
            'ileft': Random('responses','bye'),
            'sad': Random('responses','sad'),
            'hi': f'Oie, {self.message.author.name} ^^',
            'uuu': f'uuuu {self.message.author.name} 👀'
        }
        
        return events            

    def TypeNames(self) -> dict:

        Dict = {
            'uuu' : ['uuu'],
            'mua' : ['mua'],
            'laughs': self.BotDict('input','laughs'),
            'hi' : self.BotDict('input','hi'),
            'ibackmoment' : self.BotDict('input','ibackmoment'),
            'ileft' : self.BotDict('input','ileft'),
            'sad' : self.BotDict('input','sad'),
            'smilings' : self.BotDict('input','smilings'),          
        }

        return Dict

    
    def BotDict(self, mode, type) -> list:
        with open(os.path.join(sys.path[0],'dict.json'), encoding='utf-8') as j:
            Dict = json.load(j)

        return Dict[mode][type]


def setup(bot):
    bot.add_cog(Talks(bot))