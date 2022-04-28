import discord
from discord.ext import commands


class Help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help', aliases=['h'], help='The help command!', description='[command]')
    async def help(self, ctx, command_name: str = ''):
        embed = discord.Embed(title='Comando de Ajuda ^^', color=0x00B115)

        if not command_name:
            embed = self.commandList(embed)
        else:
            embed = self.especificCommand(embed, command_name.lower())

        await ctx.channel.send(embed=embed)

    def commandList(self, embed: discord.Embed) -> discord.Embed:
        cogs = self.cogs()
        cogs.remove('Help')

        for cog in cogs:
            embed.add_field(name=cog, value=self.bot.cogs[cog].__doc__)
        embed.add_field(name='Help', value='**-help [Categoria]**', inline=False)

        return embed

    def especificCommand(self, embed: discord.Embed, command_name: str) -> discord.Embed:
        cogs = self.cogs()
        embed.title = ''

        commandhelp = ""
        for cog in cogs:
            for command in self.bot.get_cog(cog).walk_commands():
                if command.hidden: continue
                if command.parent != None: continue

                if command.name == command_name.lower():
                    commandhelp = f'**-{command.name}  {command.description}**'
                    embed.add_field(name=cog, value=commandhelp, inline=False)

                    return embed

        return self.especificCog(embed, command_name)

    def especificCog(self, embed: discord.Embed, cog_name: str) -> discord.Embed:
        commandList = ""
        for command in self.bot.get_cog(cog_name.capitalize()).walk_commands():
            if command.hidden: continue
            if command.parent != None: continue

            commandList += f'**-{command.name}**  *{command.help}*\n'

        embed.add_field(name=cog_name.capitalize(), value=commandList, inline=False)
        embed.add_field(name='Help', value='**-help [comando]**', inline=False)

        return embed

    def cogs(self) -> list:
        cogs = [c for c in self.bot.cogs.keys()]
        remove = ['Talks']
        for r in remove:
            cogs.remove(r)

        return cogs

    async def cog_command_error(self, _, error):
        if isinstance(error, AttributeError):
            pass
        else:
            print(error)


def setup(bot):
    bot.add_cog(Help(bot))
