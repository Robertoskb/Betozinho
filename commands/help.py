import discord
import math
from discord.ext import commands

class Help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help', aliases=['h', 'commands'], help='The help command!')
    async def help(self, ctx, cog='1'):
        embed = discord.Embed(
            title='Help Commands!',
            color=0x00B115)

        cogs = [c for c in self.bot.cogs.keys()]
        cogs.remove('Talks')

        totalPages = math.ceil(len(cogs) / 4)

        cog = int(cog)
        if totalPages < cog or cog < 1:
            await ctx.send(f'Número da página inválido: `{cog}`')
            return

        neededCogs = []
        for i in range(4):
            x = i + (int(cog) - 1) * 4

            try: neededCogs.append(cogs[x])
            except IndexError: pass


        for cog in neededCogs:
            commandList = ""
            for command in self.bot.get_cog(cog).walk_commands():
                if command.hidden: continue
                elif command.parent != None: continue
                
                if command.help == '': command.help = '...' 

                commandList += f'**-{command.name}**    *{command.help}*\n'
            commandList += '\n'


            embed.add_field(name=cog, value=f"{commandList}", inline=False)

        await ctx.channel.send(embed=embed)  


def setup(bot):
    bot.add_cog(Help(bot))