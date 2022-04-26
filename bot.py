import discord
import os
import sys
from discord.ext import commands
from decouple import config

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot('-', help_command=None, intents=intents)


@bot.event
async def on_ready():
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Game(name='Minecraft', type=3)
    )

    print('Estou Pronto!')

def load_cogs(bot):
    for file in os.listdir(os.path.join(sys.path[0],'commands')):
        if file.endswith('.py'):
            cog = file[:-3]
            if cog != 'config':
                bot.load_extension(f'commands.{cog}')
    
    bot.load_extension('commands.config')
    
    
load_cogs(bot)

TOKEN = config("TOKEN")
bot.run(TOKEN)
