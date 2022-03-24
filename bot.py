import discord
from discord.ext import commands
from discord import activity
from decouple import config

bot = commands.Bot('-', help_command=None)


@bot.event
async def on_ready():
    activity = discord.Game(name='Minecraft', type=3)
    await bot.change_presence(status=discord.Status.online, activity=activity)
    
    print('Estou Pronto!')

bot.load_extension('commands.talks')
bot.load_extension('commands.music')
bot.load_extension('commands.bible')
bot.load_extension('commands.gifs')

bot.load_extension('commands.help')

TOKEN = config("TOKEN")
bot.run(TOKEN)