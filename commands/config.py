import discord
from discord.ext import commands
from commands.utils.serversettings import ServerSettings

class Config(commands.Cog):
    """Configurações"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='talks', help='Ativar ou Desativar minhas respostas', description='on/off')
    async def talks(self, ctx, on_off: str = ''):
        if ctx.channel.type == discord.ChannelType.private:
            return

        on_off = on_off.lower()
        if not on_off in ['on', 'off']:
            response = 'Digite on ou off'

        else:
            self.update(ctx, f'talks = {dict(on=1, off=0)[on_off]}')
            response = f'As respostas foram {dict(on="**ativadas**", off="**desativadas**")[on_off]}'

        await ctx.reply(response, mention_author=False)

    @commands.command(name='biblev', help='Mudar linguagem da bíblia', description='sigla da linguagem')
    async def biblev(self, ctx, version: str = ''):
        if ctx.channel.type == discord.ChannelType.private:
            return

        versions = ['NVI', 'RA', 'ACF', 'KJV', 'BBE', 'RVR', 'APEE']
        if not version.upper() in versions:
            response = f'Digite uma versão entre {", ".join(versions)}'

        else:
            self.update(ctx, f'biblelang = "{version.lower()}"')
            response = f'Versão redefinida para {version.upper()}'

        await ctx.reply(response, mention_author=False)

    @commands.command(name='reset', help='Resetar as minhas configurações', description='Sem argumentos')
    async def reset(self, ctx):
        ServerSettings(ctx.guild.id).reset()

        response = 'Configurações redefinidas'
        await ctx.reply(response, mention_author=False)

    def update(self, ctx, values):
        server = ServerSettings(ctx.guild.id)
        server.update(values)

    async def cog_command_error(self, ctx, error):
        response = 'Algum erro ao atualizar as configurações'
        await ctx.reply(response, mention_author=False)

        print(error)


def setup(bot):
    bot.add_cog(Config(bot))
