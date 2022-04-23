import discord
from discord.ext import commands
from decouple import config

bot = commands.Bot('-', help_command=None)


@bot.event
async def on_ready():
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Game(name='Minecraft', type=3)
    )

    print('Estou Pronto!')

bot.load_extension('commands.talks')
bot.load_extension('commands.bible')
bot.load_extension('commands.gifs')
bot.load_extension('commands.smart')
bot.load_extension('commands.profiles')

bot.load_extension('commands.config')
bot.load_extension('commands.help')

TOKEN = config("TOKEN")
bot.run(TOKEN)
