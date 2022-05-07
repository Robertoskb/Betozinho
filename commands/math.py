from commands.utils.calculator import Calculator
from discord.ext import commands


class Math(commands.Cog):
    """Matemática"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='calc', help='calculadora', description='sem argumentos')
    async def calculator(self, ctx):
        calculator = Calculator(self.bot, ctx)

        await calculator.create_calculator()

    # @commands.command(name='ord', help='número ordinal', description='número inteiro e positivo')
    # async def ord(self, ctx: commands.context, number):
    #     number = int(number)
    #     response = num2words(number, lang='pt', to='ordinal')
    #
    #     await ctx.reply(response, mention_author=False)
    #
    # @ord.error
    # async def ord_handler(self, ctx, error):
    #     errors = {
    #         KeyError: "Número muito grande '-'",
    #         TypeError: "Digite um número possitivo!",
    #         ValueError: "Digite um número inteiro!",
    #         commands.MissingRequiredArgument: "Digite um número!"
    #     }
    #
    #     for name, response in errors.items():
    #         if isinstance(error, name):
    #             return await ctx.reply(response, mention_author=False)
    #
    #     print(error)


def setup(bot):
    bot.add_cog(Math(bot))
