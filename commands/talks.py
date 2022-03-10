import random
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
        events = self.Events()
        
        if msgtype in events:
            return self.create_task(events[msgtype]())
            
                
    def MsgType(self) -> str:
        typesdict = self.TypeNames()

        msg = self.message.content.lower()
        
        msgtype = ''
        for k, v in typesdict.items():
            for c, i in enumerate(typesdict[k]):
                if i in msg: msgtype = k

        return msgtype

    
    def Events(self) -> dict:
        Random = lambda fd, fi: random.choice(self.ListMap(fd, fi)).format(self.message.author.name)

        events = {
            'laughs': lambda: self.send('hehe'),
            'smilings' : lambda: self.send(Random('responses','smilings')),
            'ibackmoment': lambda: self.send('ok'),
            'ileft': lambda: self.send(Random('responses','bye')),
            'sad': lambda: self.send(Random('responses','sad')),
            'hi': lambda: self.send(f'Oie, {self.message.author.name} ^^'),
            'uuu': lambda: self.send(f'uuuu {self.message.author.name} 👀')
        }
        
        return events    
        

    def TypeNames(self) -> dict:
        Dict = {
            'uuu' : ['uuu'],
            'laughs': ['hehe', 'hihi', 'haha'],
            'hi' : ['oie', 'oi betozinho', 'olá betozinho', 'ola betozinho'],
            'ibackmoment' : self.ListMap('dict','ibackmoment'),
            'ileft' : self.ListMap('dict','ileft'),
            'sad' : self.ListMap('dict','sad'),
            'smilings' : self.ListMap('dict','smilings'),          
        }

        return Dict

    def ListMap(self, fd, fi) -> list:
        Replace = lambda x: x.replace('\n', '')
        ReadLines = lambda fd, fi : open(f'{fd}\{fi}.txt', encoding='utf-8').readlines()
        ListMap = lambda fd, fi: list(map(Replace, ReadLines(fd, fi)))

        return ListMap(fd, fi)


def setup(bot):
    bot.add_cog(Talks(bot))