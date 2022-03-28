import requests
import discord
from discord.ext import commands
from decouple import config

KAWAII:str = config('kawaii')


class Gifs(commands.Cog):
    '''Gifs'''

    def __init__(self, bot):
        self.bot = bot
        

    @commands.command(name='slap', help='Dar um tapa no seu amiguinho', description='@user')
    async def slap(self, ctx, mention: discord.User=None):
        if mention is None:
            return await ctx.reply('Você precisa mencionar alguém', mention_author=False)      
            
        else:
            desc = f'**{ctx.author.name}** deu um tapa em **{mention.name}** D:'
            embed = self.create_embed('slap', desc)

            await ctx.channel.send(embed=embed)


    @commands.command(name='hug', help='Dar um abraço no seu amiguinho', description='@user')
    async def hug(self, ctx, mention: discord.User=None):
        if mention is None:
            return await ctx.reply('Você precisa mencionar alguém', mention_author=False)
            
        else:
            desc = f'**{ctx.author.name}** deu um abraço em **{mention.name}**'
            embed = self.create_embed('hug', desc)

            await ctx.channel.send(embed=embed)
    
    
    @commands.command(name='pat', help='Dar um cafuné no seu amiguinho', description='@user')
    async def pat(self, ctx, mention: discord.User=None):
        if mention is None:
            return await ctx.reply('Você precisa mencionar alguém', mention_author=False)        
            
        else:
            desc = f'**{ctx.author.name}** deu um cafuné em **{mention.name}** ^^'
            embed = self.create_embed('pat', desc)

            await ctx.channel.send(embed=embed)

    @commands.command(name='amazing', help='Incrível', description='sem argumentos')
    async def amazing(self, ctx):
        desc = f'**{ctx.author.name}** ^^'
        embed = self.create_embed('Amazing', desc)
        
        await ctx.channel.send(embed=embed)

    
    @commands.command(name='cry', help='Vai chorar?', description='sem argumentos')
    async def cry(self, ctx):
        desc = f'**{ctx.author.name}** está chorando :<'
        embed = self.create_embed('cry', desc)
        
        await ctx.channel.send(embed=embed)

    
    @commands.command(name='coffee', help='Cafézinho', description='@user')
    async def coffe(self, ctx, mention: discord.User=None):
        if mention is None:
            desc = f"**{ctx.author.name}** está tomando café"
            embed = self.create_embed('coffee', desc)
        
        else:
            desc = f"**{ctx.author.name}** está tomando café com **{mention.name}**"
            embed = self.create_embed('coffee', desc)
        
        await ctx.channel.send(embed=embed)

    
    @commands.command(name='cute', help='Cute', description='sem argumentos')
    async def cute(self, ctx):
        desc = f"**{ctx.author.name}** ^^"
        embed = self.create_embed('cute', desc)

        await ctx.channel.send(embed=embed)
    
    @commands.command(name='error', help='Erro', description='sem argumentos')
    async def error(self, ctx):
        desc = f"**{ctx.author.name}** bugou"
        embed = self.create_embed('error', desc)

        await ctx.channel.send(embed=embed)


    @commands.command(name='scream', help='Gritar sozinho ou com o amiguinho', description='@user')
    async def scream(self, ctx, mention: discord.User=None):
        if mention is None:
            desc = f"**{ctx.author.name}** gritou D:"
            embed = self.create_embed('scream', desc)
        
        else:
            desc = f'**{ctx.author.name}** gritou com **{mention.name}**'
            embed = self.create_embed('scream', desc)

        await ctx.channel.send(embed=embed)
    
    @commands.command(name='dance', help='Dançar sozinho ou com o seu amiguinho', description='@user')
    async def dance(self, ctx, mention: discord.User=None):
        if mention is None:
            desc = f'**{ctx.author.name}** dançou ^^'
            embed = self.create_embed('dance', desc)
                 
        else:
            desc = f'**{ctx.author.name}** dançou com **{mention.name}** ^^'
            embed = self.create_embed('dance', desc)
        
        await ctx.channel.send(embed=embed)


    def create_embed(self, type, desc):   
        request = requests.get(f'https://kawaii.red/api/gif/{type}/token={KAWAII}/').json()

        embed = discord.Embed(description=desc, color=0x00B115)
        embed.set_image(url=request['response'])

        return embed
    

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.reply('Você precisa mencionar alguém', mention_author=False)


def setup(bot):
    bot.add_cog(Gifs(bot))