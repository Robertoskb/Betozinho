import discord
from discord.ext import commands
from commands.utils.repo import get_news, get_bot_version


class About(commands.Cog):

    def __int__(self, bot):
        self.bot = bot

    @commands.command(name='version', help='Informações sobre a minha versão', description='sem argumentos')
    async def version(self, ctx):
        embed = self.get_embed_version()

        await ctx.reply(embed=embed, mention_author=False)

    @staticmethod
    def get_embed_version():
        embed = discord.Embed(title=f'Sobre a versão {get_bot_version()} ^^', color=0x00B115)

        for k, v in get_news().items():
            if not v:
                continue
            embed.add_field(name=k, value=v, inline=False)

        return embed


def setup(bot):
    bot.add_cog(About(bot))
