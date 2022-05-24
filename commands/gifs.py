import discord
from discord.ext import commands
from decouple import config
from aiohttp import ClientSession
from commands.utils.onhold import OnHold

KAWAII = config('kawaii')


class Gifs(commands.Cog):
    """Gifs"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='slap', help='Dar um tapa no seu amiguinho', description='@user')
    async def slap(self, ctx, mention: discord.User):
        desc = '**{}** deu um tapa em **{}**'
        embed = await self.create_embed('slap', desc.format(ctx.author.display_name,
                                                            mention.display_name))

        gif = await ctx.channel.send(embed=embed)

        await self.gif_back(gif, ctx, mention, desc, 'slap')

    @commands.command(name='hug', help='Dar um abraço no seu amiguinho', description='@user')
    async def hug(self, ctx, mention: discord.User):
        desc = '**{}** deu um abraço em **{}**'
        embed = await self.create_embed('hug', desc.format(ctx.author.display_name,
                                                           mention.display_name))

        gif = await ctx.channel.send(embed=embed)

        await self.gif_back(gif, ctx, mention, desc, 'hug')

    @commands.command(name='pat', help='Dar um cafuné no seu amiguinho', description='@user')
    async def pat(self, ctx, mention: discord.User):
        desc = '**{}** deu um cafuné em **{}**'
        embed = await self.create_embed('pat', desc.format(ctx.author.display_name,
                                                           mention.display_name))

        gif = await ctx.channel.send(embed=embed)

        await self.gif_back(gif, ctx, mention, desc, 'pat')

    @commands.command(name='amazing', help='Incrível', description='sem argumentos')
    async def amazing(self, ctx):
        desc = f'**{ctx.author.display_name}** ^^'
        embed = await self.create_embed('Amazing', desc)

        await ctx.channel.send(embed=embed)

    @commands.command(name='cry', help='Vai chorar?', description='sem argumentos')
    async def cry(self, ctx):
        desc = f'**{ctx.author.display_name}** está chorando :<'
        embed = await self.create_embed('cry', desc)

        await ctx.channel.send(embed=embed)

    @commands.command(name='coffee', help='Cafézinho', description='@user')
    async def coffee(self, ctx, mention: discord.User = None):
        if mention is None:
            desc = f"**{ctx.author.display_name}** está tomando café"
            embed = await self.create_embed('coffee', desc)

        else:
            desc = f"**{ctx.author.display_name}** está tomando café com **{mention.display_name}**"
            embed = await self.create_embed('coffee', desc)

        await ctx.channel.send(embed=embed)

    @commands.command(name='cute', help='Cute', description='sem argumentos')
    async def cute(self, ctx):
        desc = f"**{ctx.author.display_name}** ^^"
        embed = await self.create_embed('cute', desc)

        await ctx.channel.send(embed=embed)

    @commands.command(name='error', help='Erro', description='sem argumentos')
    async def error(self, ctx):
        desc = f"**{ctx.author.display_name}** bugou"
        embed = await self.create_embed('error', desc)

        await ctx.channel.send(embed=embed)

    @commands.command(name='scream', help='Gritar sozinho ou com o amiguinho', description='@user')
    async def scream(self, ctx, mention: discord.User = None):
        if mention is None:
            desc = f"**{ctx.author.display_name}** gritou D:"
            embed = await self.create_embed('scream', desc)

        else:
            desc = f'**{ctx.author.display_name}** gritou com **{mention.display_name}**'
            embed = await self.create_embed('scream', desc)

        await ctx.channel.send(embed=embed)

    @commands.command(name='dance', help='Dançar sozinho ou com o seu amiguinho', description='@user')
    async def dance(self, ctx, mention: discord.User = None):
        if mention is None:
            desc = f'**{ctx.author.display_name}** dançou ^^'
            embed = await self.create_embed('dance', desc)

        else:
            desc = f'**{ctx.author.display_name}** dançou com **{mention.display_name}** ^^'
            embed = await self.create_embed('dance', desc)

        await ctx.channel.send(embed=embed)

    async def gif_back(self, gif, ctx, mention, desc, _type):
        hold = OnHold(self.bot, gif, mention)
        desc = desc.format(mention.display_name, ctx.author.display_name) + " de volta"

        if await hold.create_hold():
            await ctx.channel.send(embed=await self.create_embed(_type, desc))

    async def create_embed(self, _type, desc):
        request = await self.get_request(_type)

        embed = discord.Embed(description=desc, color=0x00B115)
        embed.set_image(url=request['response'])

        return embed

    @staticmethod
    async def get_request(_type):
        url = f'https://kawaii.red/api/gif/{_type}/token={KAWAII}/'

        async with ClientSession(trust_env=True) as Session:
            async with Session.get(url) as request:
                return await request.json()

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.BadArgument) or isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply('Você precisa mencionar alguém', mention_author=False)


def setup(bot):
    bot.add_cog(Gifs(bot))
