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
        if message.author == self.bot.user:
            return

        msgtype = self.get_MsgType(message)
        events = self.Responses(message)

        if msgtype in events:
            response = events[msgtype]

            await message.reply(response, mention_author=False)

    def get_MsgType(self, message) -> str:
        typesdict = self.BotDict('input')
        msg = message.content.lower()

        msgtype = self.CheckMsgType(typesdict, msg)

        return msgtype

    def CheckMsgType(self, typesdict, msg):
        msgtype = ''
        for Type, lst in typesdict.items():
            for item in lst:
                case1 = f'"{item}"' in msg
                case2 = f"'{item}'" in msg

                if case1 or case2: continue
                if item in msg: msgtype = Type

        return msgtype

    def Responses(self, message) -> dict:
        Dict = self.BotDict('responses')

        author = message.author.name
        for k, v in Dict.items():
            Dict[k] = random.choice(v).format(author)

        return Dict

    def BotDict(self, mode: str) -> dict:
        arq = os.path.join(sys.path[0], 'dicts/dictfortalks.json')
        with open(arq, encoding='utf-8') as j:
            Dict = json.load(j)

        return Dict[mode]


def setup(bot):
    bot.add_cog(Talks(bot))
