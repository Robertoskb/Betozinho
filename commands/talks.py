import random
import json
import os
import sys
from discord.ext import commands


class Talks(commands.Cog):
    """Talks with user"""

    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_message(self, message) -> None:
        if message.author == self.bot.user: return

        await self.Raply(message)
        

    async def Raply(self, message):
        msgtype = self.MsgType(message) # Tipo da mensagem
        events = self.Responses(message) # Dicionário de respostas
        
        if msgtype in events: 
            # Se o tipo da mensagem mensagem estiver no dicionário respostas
            # O bot vai responder de acordo com tipo da mensagem recebida
            await message.reply(events[msgtype], mention_author=False)
            
                
    def MsgType(self, message) -> str: 
        # Verifica o tipo da mensagem 
        # Ex: 'oie' é do tipo 'hi'
        # Retorna o tipo 'hi' se a mensagem conter 'oie'
        # Se o tipo não existir, uma string vazia é retornada

        typesdict = self.BotDict('input') # Dicionário com os tipos de mensagens
        # Os tipos são as chaves
        # Cada tipo tem uma lista de mensagens correspondentes

        msg = message.content.lower()
        
        msgtype = ''
        for k, v in typesdict.items(): 
            for i in v:
                if f'"{i}"' in msg or f"'{i}'"in msg: continue
                if i in msg: msgtype = k 
                # Se a string da mensagem recebida conter uma string de uma chave 
                # O tipo da mensagem terá o valor da chave 


        return msgtype

    
    def Responses(self, message) -> dict:
        Dict = self.BotDict('responses') # Dicionário de respostas

        f = message.author.name
        for k, v in Dict.items(): 
            # Converte a lista de respostas em uma resposta aleatória
            Dict[k] = random.choice(v).format(f) 

        return Dict

    
    def BotDict(self, mode:str) -> dict:
        # Retorna um dicinário específico de um json
        with open(os.path.join(sys.path[0],'dict.json'), encoding='utf-8') as j:
            Dict = json.load(j)

        return Dict[mode]


def setup(bot):
    bot.add_cog(Talks(bot))