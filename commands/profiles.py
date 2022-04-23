import discord
from discord.ext import commands
from commands.utils.users import User
from commands.utils.confirm import Confirm
from awaits.awaitable import awaitable
from easy_pil import Editor, Font, load_image_async

COLOR = 0x00B115


class Profiles(commands.Cog):
    '''Perfis'''

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='create', help='Criar um perfil', description='sem argumentos')
    async def create(self, ctx):
        rest_response = 'Veja o seu perfil com **-profile**'
        if await self.create_user(ctx.author.id):
            response = 'Perfil criado! ' + rest_response

        else:
            response = 'Você já tem um perfil! ' + rest_response

        await ctx.reply(response, mention_author=False)

    @awaitable
    def create_user(self, id):
        user = User(id)
        created_user = user.create_user()
        user.cursor.close()

        return created_user

    @commands.command(name='delete', help='Excluir o seu perfil dos meus dados', description='sem argumentos')
    async def delete(self, ctx):
        if not await self.get_user(ctx.author.id):
            return await ctx.reply('Você não tem perfil', mention_author=False)

        additional = f'Eu vou sentir muita falta de você, {ctx.author.display_name}'
        confirm = Confirm(self.bot, ctx, additional)
        if await confirm.confirmation():
            await self.delete_user(ctx.author.id)
            response = "Perfil excluido do meu banco de dados 😔"

        else:
            response = 'Cancelado 😰'

        await ctx.reply(response, mention_author=False)

    @awaitable
    def delete_user(self, id):
        user = User(id)
        user.delete_user()
        user.cursor.close()

    @commands.command(name='profile', aliases=['perfil'], help='Ver o seu perfil ou de alguém', description='opcionalmente @user')
    async def profile(self, ctx, mention: discord.User = None):
        def response(response): return ctx.reply(
            response, mention_author=False)

        if mention is None:
            profile = await self.get_user(ctx.author.id)
            if profile:
                file = await self.get_profile_img(ctx.author, profile)
                await ctx.reply(file=file, mention_author=False)

            else:
                await response('Você não tem perfil! Crie um com **-create**')

        else:
            profile = await self.get_user(mention.id)
            if profile:
                file = await self.get_profile_img(mention, profile)
                await ctx.reply(file=file, mention_author=False)

            else:
                await response('Esse usuário não tem perfil')

    async def get_profile_img(self, user, profile):
        level, xp, description = self.get_profile_infos(profile)

        bg = Editor('bg.png')
        avatar = await load_image_async(str(user.avatar_url))
        avatar = Editor(avatar).resize((127, 127)).circle_image()
        bg.paste(avatar.image, (67, 114))

        font1 = Font(
            '/usr/share/fonts/truetype/msttcorefonts/arial.ttf').poppins(size=30)
        font2 = Font(
            '/usr/share/fonts/truetype/msttcorefonts/arial.ttf').poppins(size=23)

        bg.text((10, 10), str(user), font=font1, color='white')
        bg.text((270, 150), description, font=font2, color='white')
        bg.text(
            (280, 190), f'Nível: {level}            XP: {xp}', font=font2, color='white')

        file = discord.File(fp=bg.image_bytes, filename='card.png')

        return file

    def get_profile_infos(self, profile):
        level = profile.get('level')
        xp = profile.get('xp')
        description = profile.get('description')

        if type(level) == int and level < 7:
            xp = str(xp)
            xp += f'/{level*20000}'

        return level, xp, description

    @awaitable
    def get_user(self, id):
        user = User(id)
        profile = user.infos
        user.cursor.close()

        return profile

    @create.error
    async def create_handler(self, ctx, error):
        response = 'Erro ao criar o seu perfil'
        await ctx.reply(response, mention_author=False)

        print(error)

    @delete.error
    async def create_handler(self, ctx, error):
        response = 'Erro ao excluir o seu perfil'
        await ctx.reply(response, mention_author=False)

        print(error)

    @profile.error
    async def profile_handler(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await self.profile(ctx)

        else:
            await ctx.reply('Erro ao carregar perfil', mention_author=False)

            print(error)


def setup(bot):
    bot.add_cog(Profiles(bot))
