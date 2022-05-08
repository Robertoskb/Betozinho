import math
from fractions import Fraction
from commands.utils.calculator import Calculator
from discord.ext import commands
from num2words import num2words


class Math(commands.Cog):
    """Matemática"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='calc', help='calculadora', description='sem argumentos')
    async def calculator(self, ctx):
        calculator = Calculator(self.bot, ctx)

        await calculator.create_calculator()

    @commands.command(name='ord', help='número ordinal', description='número inteiro de 1 a 10^15')
    async def ord(self, ctx, number: int):
        number = int(number)
        response = f"{number}º = {num2words(number, lang='pt', to='ordinal')}"

        await ctx.reply(response, mention_author=False)

    @commands.command(name='full', help='número por extenso', description='número inteiro de -10^15 a 10^15')
    async def full(self, ctx, number: int):
        response = f"{number} = {num2words(number, lang='pt')}"

        await ctx.reply(response, mention_author=False)

    @commands.command(name='mdc', help='Máximo Divisor Comum', description='números inteiros')
    async def gcd(self, ctx, *args: int):
        await ctx.reply(math.gcd(*args), mention_author=False)

    @commands.command(name='mmc', help='Mínimo Múltiplo Comum', description='números inteiros')
    async def lcm(self, ctx, *args: int):
        await ctx.reply(math.lcm(*args), mention_author=False)

    @commands.command(name='cos', help='cosseno', description='número real')
    async def cos(self, ctx, number: float):
        cos = math.cos(number)
        rest = f'ou {Fraction(cos).limit_denominator()}' if int(cos) != cos else ''
        response = f'{cos:.6f} {rest}'

        await ctx.reply(response, mention_author=False)

    @commands.command(name='sin', help='seno', description='número real')
    async def sin(self, ctx, number: float):
        sin = math.sin(number)
        rest = f'ou {Fraction(sin).limit_denominator()}' if int(sin) != sin else ''
        response = f'{sin:.6f} {rest}'

        await ctx.reply(response, mention_author=False)

    @commands.command(name='tan', help='tangente', description='número real')
    async def tan(self, ctx, number: float):
        tan = math.tan(number)
        rest = f'ou {Fraction(tan).limit_denominator()}' if int(tan) != tan else ''
        response = f'{tan:.6f} {rest}'

        await ctx.reply(response, mention_author=False)

    @commands.command(name='log', help='logaritmo', description='base > 0 != 1 e x > 0')
    async def log(self, ctx, b: float, x: float):
        log = math.log(x, b)
        rest = f'ou {Fraction(log).limit_denominator()}' if int(log) != log else ''
        response = f'{log:.6f} {rest}'

        await ctx.reply(response, mention_author=False)

    @commands.command(name='degr', help="radianos para graus", description='número real')
    async def degrees(self, ctx, number: float):
        degrees = math.degrees(number)
        rest = f'ou {Fraction(degrees).limit_denominator()}' if int(degrees) != degrees else ''
        response = f'{degrees:.6f}º {rest}º'

        await ctx.reply(response, mention_author=False)

    @commands.command(name='rad', help="graus para radianos", description='número real')
    async def radians(self, ctx, number: float):
        radians = math.radians(number)
        rest = ''
        if int(radians) != radians:
            rest = f'ou {str(Fraction(number/180).limit_denominator()).replace("/", "π/")}'

        response = f'{radians:.6f}rad {rest}rad'

        await ctx.reply(response, mention_author=False)

    async def cog_command_error(self, ctx, error):
        response = "Esse comando precisa de valores específicos! Use **-help [comando]**"

        await ctx.reply(response, mention_author=False)


def setup(bot):
    bot.add_cog(Math(bot))
