import discord
import sys
import os
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

        return created_user

    @commands.command(name='delete', help='Excluir o seu perfil dos meus dados', description='sem argumentos')
    async def delete(self, ctx):
        if not await self.get_user(ctx.author.id):
            return await ctx.reply('Você não tem perfil', mention_author=False)

        confirm = Confirm(
            self.bot, ctx, f'Eu vou sentir muita falta de você, {ctx.author.display_name}')

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
        bg = await self.get_bg(user)

        font1, font2 = self.get_fonts()

        bg = self.write_bg(bg, user, profile, font1, font2)

        file = discord.File(fp=bg.image_bytes, filename='card.png')

        return file

    async def get_bg(self, user):
        bg = Editor(os.path.join(sys.path[0], 'images/bg.png'))
        avatar = await load_image_async(str(user.avatar_url))
        avatar = Editor(avatar).resize((127, 127)).circle_image()
        bg.paste(avatar.image, (67, 114))

        return bg

    def write_bg(self, bg, user, profile, font1, font2):
        level, xp, description = self.get_profile_infos(profile)
        bg.text((10, 10), str(user), font=font1, color='white')
        bg.text((263, 146), description, font=font1, color='white')
        bg.text(
            (265, 190), f'Nível: {level}    XP: {xp}', font=font2, color='white')

        return bg

    def get_fonts(self):
        font1 = Font(os.path.join(
            sys.path[0], 'fonts/FreeMono.ttf')).poppins(size=25)
        font2 = Font(os.path.join(
            sys.path[0], 'fonts/FreeMono.ttf')).poppins(size=23)

        return font1, font2

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
            response = 'Erro ao carregar perfil'
            await ctx.reply(response, mention_author=False)

            print(error)


def setup(bot):
    bot.add_cog(Profiles(bot))
