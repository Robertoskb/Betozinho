import requests
import discord
from discord.ext import commands
from decouple import config

KAWAII:str = config('kawaii')


class Gifs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        

    @commands.command(name='slap', help='Dar um tapa no seu amiguinho')
    async def slap(self, ctx, mention: discord.User=None):
        if mention is None:
            return await ctx.reply('Você precisa mencionar alguém', mention_author=False)      
            

        desc = f'**{ctx.author.name}** deu um tapa em **{mention.name}** D:'
        await self.create_embed(ctx, 'slap', desc)


    @commands.command(name='hug', help='Dar um abraço no seu amiguinho')
    async def hug(self, ctx, mention: discord.User=None):
        if mention is None:
            return await ctx.reply('Você precisa mencionar alguém', mention_author=False)
            
        
        desc = f'**{ctx.author.name}** deu um abraço em **{mention.name}**'
        await self.create_embed(ctx, 'hug', desc)
    
    
    @commands.command(name='pat', help='Dar um cafuné no seu amiguinho')
    async def pat(self, ctx, mention: discord.User=None):
        if mention is None:
            return await ctx.reply('Você precisa mencionar alguém', mention_author=False)        
            

        desc = f'**{ctx.author.name}** deu um cafuné em **{mention.name}** ^^'
        await self.create_embed(ctx, 'pat', desc)


    @commands.command(name='amazing', help='Incrível')
    async def amazing(self, ctx):
        desc = f'**{ctx.author.name}** ^^'
        await self.create_embed(ctx, 'Amazing', desc)

    
    @commands.command(name='cry', help='Vai chorar?')
    async def cry(self, ctx):
        desc = f'**{ctx.author.name}** está chorando :<'
        await self.create_embed(ctx, 'cry', desc)

    
    @commands.command(name='coffee', help='Cafézinho')
    async def coffe(self, ctx, mention: discord.User=None):
        if mention is None:
            desc = f"**{ctx.author.name}** está tomando café"
            await self.create_embed(ctx, 'coffee', desc)
        

        desc = f"**{ctx.author.name}** está tomando café com **{mention.name}**"
        await self.create_embed(ctx, 'coffee', desc)

    
    @commands.command(name='cute', help='Cute')
    async def cute(self, ctx):
        desc = f"**{ctx.author.name}** ^^"
        await self.create_embed(ctx, 'cute', desc)

    
    @commands.command(name='error', help='Erro')
    async def error(self, ctx):
        desc = f"**{ctx.author.name}** bugou"
        await self.create_embed(ctx, 'error', desc)


    @commands.command(name='scream', help='Gritar sozinho ou com o amiguinho')
    async def scream(self, ctx, mention: discord.User=None):
        if mention is None:
            desc = f"**{ctx.author.name}** gritou D:"
            return await self.create_embed(ctx, 'scream', desc)
        

        desc = f'**{ctx.author.name}** gritou com **{mention.name}**'
        await self.create_embed(ctx, 'scream', desc)

    
    @commands.command(name='dance', help='Dançar sozinho ou com o seu amiguinho')
    async def dance(self, ctx, mention: discord.User=None):
        if mention is None:
            desc = f'**{ctx.author.name}** dançou ^^'
            return await self.create_embed(ctx, 'dance', desc)
                 
        
        desc = f'**{ctx.author.name}** dançou com **{mention.name}** ^^'
        await self.create_embed(ctx, 'dance', desc)


    async def create_embed(self, ctx, type, desc):   
        request = requests.get(f'https://kawaii.red/api/gif/{type}/token={KAWAII}/').json()

        embed = discord.Embed(description=desc, color=0x00B115)
        embed.set_image(url=request['response'])
    
        await ctx.channel.send(embed=embed)
    

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.reply('Você precisa mencionar alguém', mention_author=False)


def setup(bot):
    bot.add_cog(Gifs(bot))