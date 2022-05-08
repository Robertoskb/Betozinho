import discord
import random
import asyncio

expressions = ['1+1', '3*4', '10/2', '5-2']

buttons = {'0️⃣': '0', '1️⃣': '1', '2️⃣': '2', '3️⃣': '3',
           '4️⃣': '4', '5️⃣': '5', '6️⃣': '6', '7️⃣': '7',
           '8️⃣': '8', '9️⃣': '9',
           '↪️': '(', '↩️': ')', '⏺️': '.',
           '➕': '+', '➖': '-', '➗': '/', '✖': '*',
           '🔙': 'b'}


class Calculator:

    def __init__(self, bot, ctx):
        self.bot = bot
        self.ctx = ctx
        self._expression = random.choice(expressions)

    async def create_calculator(self):
        reply = await self.ctx.reply(embed=self.get_embed(), mention_author=False)

        for button in buttons.keys():
            await reply.add_reaction(button)

        def check(react, usr):
            return (
                usr == self.ctx.author
                and str(react.emoji) in buttons
                and react.message.id == reply.id
            )

        await self.timeout_calculator(reply, check)

    async def timeout_calculator(self, reply, check):
        while True:
            try:
                reaction, user = await self.bot.wait_for("reaction_add", timeout=600, check=check)
                await self.edit_reply(reply, reaction, user)

            except asyncio.TimeoutError:
                for button in buttons.keys():
                    await reply.remove_reaction(button, self.bot.user)

                return

    async def edit_reply(self, reply, reaction, user):
        self.edit_expression(str(reaction))
        await reply.edit(embed=self.get_embed())
        await reply.remove_reaction(reaction, user)

    def edit_expression(self, reaction):
        if reaction != '🔙':
            self._expression = self._expression.replace('. . .', '').replace("**", "*")
            self._expression += buttons[reaction]

        else:
            self._expression = self._expression[:-1] or '. . .'

    def get_embed(self):
        embed = discord.Embed(title='Calculadora', color=0x00B115)
        embed.add_field(name='Expressão:', value=self._expression.replace('*', 'x'), inline=False)
        embed.add_field(name='Resultado:', value=self.get_result(), inline=False)

        return embed

    def get_result(self):
        try:
            result = eval(self._expression)

        except:
            result = '-'

        return result
