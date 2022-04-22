import asyncio


class Pages:

    def __init__(self, bot, ctx, reply, embeds):
        self.bot = bot
        self.ctx = ctx
        self.reply = reply
        self.embeds = embeds

    async def create_pages(self):
        await self.reply.add_reaction("◀️")
        await self.reply.add_reaction("▶️")

        def check(react, usr):
            return (
                usr == self.ctx.author 
                and str(react.emoji) in ["◀️", "▶️"]
                and react.message.id == self.reply.id
            )

        await self.timeout_pages(check)

    async def timeout_pages(self, check):
        cur_page = 0
        while True:
            try:
                reaction, user = await self.bot.wait_for("reaction_add", timeout=600, check=check)
                cur_page = await self.switch_pages(reaction, user, cur_page)

            except asyncio.TimeoutError:
                await self.reply.remove_reaction("◀️", self.bot.user)
                await self.reply.remove_reaction("▶️", self.bot.user)

                break

    async def switch_pages(self, reaction, user, cur_page: int) -> int:
        if str(reaction.emoji) == "▶️" and cur_page != len(self.embeds) - 1:
            cur_page += 1
            await self.reply.edit(embed=self.embeds[cur_page])
            await self.reply.remove_reaction(reaction, user)

        elif str(reaction.emoji) == "◀️" and cur_page > 0:
            cur_page -= 1
            await self.reply.edit(embed=self.embeds[cur_page])
            await self.reply.remove_reaction(reaction, user)
			
        else:
            await self.reply.remove_reaction(reaction, user)

        return cur_page
