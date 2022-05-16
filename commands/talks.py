import discord
from commands.utils.talksutils import get_msg_type, responses
from discord.ext import commands
from commands.utils.serversettings import ServerSettings


class Talks(commands.Cog):
    """Talks with user"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if not self.check_settings(message):
            return

        msg_type = get_msg_type(message)
        events = responses(message)

        if events.get(msg_type):
            await message.reply(events[msg_type], mention_author=False)

    @staticmethod
    def check_settings(message) -> int:
        if message.channel.type == discord.ChannelType.private:
            return 1
        
        server = ServerSettings(message.guild.id)
        settings = server.get_settings('talks')
        
        return settings

    async def cog_command_error(self, _, error):
        print(error)


def setup(bot):
    bot.add_cog(Talks(bot))
