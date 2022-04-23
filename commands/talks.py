from http import server
import discord
import random
import json
import os
import sys
from awaits.awaitable import awaitable
from discord.ext import commands
from commands.utils.serversettings import ServerSettings


class Talks(commands.Cog):
    """Talks with user"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        if not await self.check_settings(message):
            return

        msgtype = self.get_MsgType(message)
        events = self.Responses(message)

        if events.get(msgtype):
            await message.reply(events[msgtype], mention_author=False)

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

                if case1 or case2:
                    continue
                if item in msg:
                    msgtype = Type

        return msgtype

    def Responses(self, message) -> dict:
        Dict = self.BotDict('responses')

        author = message.author.display_name
        for k, v in Dict.items():
            Dict[k] = random.choice(v).format(author)

        return Dict

    def BotDict(self, mode: str) -> dict:
        arq = os.path.join(sys.path[0], 'dicts/dictfortalks.json')
        with open(arq, encoding='utf-8') as j:
            Dict = json.load(j)

        return Dict[mode]


    @awaitable
    def check_settings(self, message) -> int:
        if message.channel.type == discord.ChannelType.private:
            return 1
        
        server = ServerSettings(message.guild.id)
        settings = server.get_settings('talks')
        server.cursor.close()
        
        return settings

    async def cog_command_error(self, _, error):
        print(error)


def setup(bot):
    bot.add_cog(Talks(bot))
