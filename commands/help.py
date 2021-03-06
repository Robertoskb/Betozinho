import discord
from discord.ext import commands


class Help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help', aliases=['h'], help='The help command!', description='[command]')
    async def help(self, ctx, command_name: str = ''):
        embed = discord.Embed(title='Comando de Ajuda ^^', color=0x00B115)

        if not command_name:
            embed = self.command_list(embed)
        else:
            embed = self.specific_command(embed, command_name.lower())

        await ctx.channel.send(embed=embed)

    def command_list(self, embed: discord.Embed) -> discord.Embed:
        cogs = self.cogs()
        cogs.remove('Help')

        embed.description = ''
        for cog in cogs:
            embed.description += f"**-help {cog}**\n"

        return embed

    def specific_command(self, embed: discord.Embed, command_name: str) -> discord.Embed:
        cogs = self.cogs()
        embed.title = ''

        for cog in cogs:
            for command in self.bot.get_cog(cog).walk_commands():
                if command.hidden:
                    continue
                if command.parent is not None:
                    continue

                if command.name == command_name.lower():
                    command_help = f'**-{command.name}  {command.description}**'
                    embed.add_field(name=cog, value=command_help, inline=False)

                    return embed

        return self.specific_cog(embed, command_name)

    def specific_cog(self, embed: discord.Embed, cog_name: str) -> discord.Embed:
        command_list = ""
        for command in self.bot.get_cog(cog_name.capitalize()).walk_commands():
            if command.hidden:
                continue
            if command.parent is not None:
                continue

            command_list += f'**-{command.name}**  *{command.help}*\n'

        embed.add_field(name=cog_name.capitalize(), value=command_list, inline=False)
        embed.add_field(name='Help', value='**-help [comando]**', inline=False)

        return embed

    def cogs(self) -> list:
        cogs = [c for c in self.bot.cogs.keys()]
        remove = ['Talks']
        for r in remove:
            cogs.remove(r)

        return cogs

    async def cog_command_error(self, ctx, _):
        await self.help(ctx)


def setup(bot):
    bot.add_cog(Help(bot))
