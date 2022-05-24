import asyncio


class OnHold:

    def __init__(self, bot, gif, mention):
        self.bot = bot
        self.gif = gif
        self.mention = mention

    async def create_hold(self):
        await self.gif.add_reaction("🔁")

        def check(react, user):
            return (user == self.mention
                    and str(react.emoji) == '🔁'
                    and react.message.id == self.gif.id
                    )

        return await self._timeout_hold(check)

    async def _timeout_hold(self, check):
        try:
            reaction, _ = await self.bot.wait_for('reaction_add', timeout=600, check=check)

        except asyncio.TimeoutError:
            await self.gif.remove_reaction('🔁')

            confirm = False

        else:
            confirm = True

        return confirm
