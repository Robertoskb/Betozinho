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
        Random = lambda mode, type: random.choice(self.BotDict(mode, type)).format(self.message.author.name)

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
            'laughs': ['hehe', 'hihi', 'haha'],
            'hi' : ['oie', 'oi betozinho', 'olá betozinho', 'ola betozinho'],
            'ibackmoment' : self.BotDict('input','ibackmoment'),
            'ileft' : self.BotDict('input','ileft'),
            'sad' : self.BotDict('input','sad'),
            'smilings' : self.BotDict('input','smilings'),          
        }

        return Dict

    
    def BotDict(self, mode, type) -> list:
        Dict = {
            'input': {
                'ibackmoment':['já volto','ja volto',
                'daqui a pouco volto', 'daqui a pouco eu volto'], 

                'ileft':['tchau betozinho','chau betozinho','xau betozinho', 'bye betozinho','baie betozinho',
                'bai betozinho','vou sair', 'preciso sair', 'tenho que sair'], 

                'sad':['bua',';-;',':(','):',':<','>:','😦','😕','😣',
                '😓','😔','🙁','☹️','😞','😟','😥','🥲','😢','😭'],

                'smilings':['^^',':b',':p','(:',':)',':>','<:','🙂','😁','😄','😎'],
            },

            'responses':{
                'bye':['Tchau {}', 'Baie {}', 'Bai bai {}', 'Bye bye {}', 'Chau {}', 'Xau {}'],

                'sad':['Vai chorar?', '🙁', 'Não fique triste {}', ';-;'],

                'smilings':['^^',':p',':b','(:','🙂','😁','😄','😎']

            }

        }

        return Dict[mode][type]


def setup(bot):
    bot.add_cog(Talks(bot))