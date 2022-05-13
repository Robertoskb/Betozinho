from discord.ext import commands
from pyMorseTranslator import translator
from unidecode import unidecode
from hashlib import sha256
from caesarcipher import CaesarCipher


class Encoder(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='morse', help='codificar um texto para morse', description='texto')
    async def morse(self, ctx, *, text: str):
        morse = translator.Encoder().encode(unidecode(text)).morse

        response = morse if len(morse) < 4000 else "Texto muito grande '-'"

        await ctx.reply(response, mention_author=False)

    @commands.command(name='dmorse', help='decodificar um código morse', description='código morse')
    async def dmorse(self, ctx, *, text: str):
        decode = translator.Decoder().decode(unidecode(text)).plaintext

        await ctx.reply(decode, mention_author=False)
  
    @commands.command(name='sha256', help='codificar um texto para sha256', description='texto')
    async def hash(self, ctx, *, text: str):
        await ctx.reply(sha256(text.encode("utf-8")).hexdigest(), mention_author=False)

    @commands.command(neme='cipher', help='Cifra de Cesar',  description='cifra e texto')
    async def cipher(self, ctx, offset: int, *, text: str):
        await ctx.reply(CaesarCipher(unidecode(text), offset=offset).decoded, mention_author=False)

    @morse.error
    async def morse_handler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply('Digite um texto para codificar', mention_author=False)

    @dmorse.error
    async def dmorse_handler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply('Digite um código morse para decodificar', mention_author=False)

        else:
            await ctx.reply("Isso não é um código morse '-'", mention_author=False)

    @hash.error
    async def hash_handler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply('Digite um texto para codificar', mention_author=False)

    @cipher.error
    async def cipher_handler(self, ctx, error):
        if isinstance(error, commands.BadArgument) or isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply("Digite um número inteiro para a cifra e um texto", mention_author=False)


def setup(bot):
    bot.add_cog(Encoder(bot))

