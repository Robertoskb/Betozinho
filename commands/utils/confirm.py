import discord
import asyncio


class Confirm:

    def __init__(self, bot, ctx):
        self.bot = bot
        self.ctx = ctx

    async def confirmation(self, additional=''):
        embed = self.confirmation_embed(additional)
        reply = await self.ctx.reply(embed=embed, mention_author=False)

        return await self.create_confirmation(reply)

    async def create_confirmation(self, reply):
        await reply.add_reaction("✅")
        await reply.add_reaction("❌")

        def check(react, user):
            return (
                user == self.ctx.author
                and str(react.emoji) in ["✅", "❌"]
                and react.message.id == reply.id
            )

        return await self.timeout_confirmation(check, reply)

    async def timeout_confirmation(self, check, reply):
        options = {'✅': True, '❌': False}
        try:
            reaction, _ = await self.bot.wait_for('reaction_add', timeout=60, check=check)

        except asyncio.TimeoutError:
            await reply.delete()

        else:
            await reply.delete()
            return options[str(reaction.emoji)]

    @staticmethod
    def confirmation_embed(additional):
        title = "Você tem certeza?"
        description = f"\n✅ **SIM**\n❌ **NÃO**\n\n{additional}"
        color = 0x00B115
        embed = discord.Embed(title=title, description=description, color=color)

        return embed
