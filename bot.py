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
        activity=discord.Game(name='-help', type=3)
    )

    print('Estou Pronto!')


def load_cogs():
    for file in os.listdir(os.path.join(sys.path[0], 'commands')):
        if file.endswith('.py'):
            if 'config' != file[:-3] != 'about':
                bot.load_extension(f'commands.{file[:-3]}')
    
    bot.load_extension('commands.config')
    bot.load_extension('commands.about')
    
    
load_cogs()

TOKEN = config("TOKEN1")
bot.run(TOKEN)
