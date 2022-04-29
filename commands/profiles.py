import discord
import sys
import os
from discord.ext import commands
from commands.utils.users import User
from commands.utils.confirm import Confirm
from easy_pil import Editor, Font, load_image_async


class Profiles(commands.Cog):
    '''Perfis'''

    def __init__(self, bot):
        self.bot = bot

    @commands.guild_only()
    @commands.command(name='create', help='Criar um perfil', description='sem argumentos')
    async def create(self, ctx):
        rest_response = 'Veja o seu perfil com **-profile**'

        if User(ctx.author.id).create_user():
            response = 'Perfil criado! ' + rest_response

        else:
            response = 'Você já tem um perfil! ' + rest_response

        await ctx.reply(response, mention_author=False)

    @commands.guild_only()
    @commands.command(name='delete', help='Excluir o seu perfil dos meus dados', description='sem argumentos')
    async def delete(self, ctx):
        if not User(ctx.author.id).infos:
            return await ctx.reply('Você não tem perfil', mention_author=False)

        additional = f'Eu vou sentir muita falta de você, {ctx.author.display_name}'
        if await Confirm(self.bot, ctx).confirmation(additional):
            User(ctx.author.id).delete_user()
            response = "Perfil excluido do meu banco de dados 😔"

        else:
            response = 'Cancelado 😰'

        await ctx.reply(response, mention_author=False)

    @commands.guild_only()
    @commands.command(name='profile', aliases=['perfil'], help='Ver o seu perfil ou de alguém', description='opcionalmente @user')
    async def profile(self, ctx, mention: discord.User = None):
        user = mention or ctx.author
        profile = User(user.id)
        msg = 'Você não tem perfil! Crie um com **-create**' if not mention else 'Usuario não tem perfil'
        
        if profile.infos:
            file = await self.get_profile_img(ctx, user, profile)

            await ctx.reply(file=file, mention_author=False)

        else:

            await ctx.reply(msg, mention_author=False)

    async def get_profile_img(self, ctx, user, profile):
        bg = await self.get_bg(user, profile)
        bg = self.write_bg(ctx, bg, user, profile)

        file = discord.File(fp=bg.image_bytes, filename='card.png')

        return file

    async def get_bg(self, user, profile):
        bg = Editor(os.path.join(sys.path[0], f'images/bgs/bglv{profile.infos["bg"]}.png'))
        avatar = await load_image_async(str(user.avatar_url))
        avatar = Editor(avatar).resize((182, 182)).circle_image()
        bg.paste(avatar.image, (30, 88))

        return bg

    def write_bg(self, ctx, bg, user, profile):
        fonts = self.get_fonts()
        rank = profile.get_rank(ctx.guild.members)

        bg.text((10, 7), user.display_name, font=fonts['main'], color='white')
        bg.text((10, 45), f'#{rank} {ctx.guild.name}',font=fonts['rank'], color='white')
        bg.text((245, 136), f'Nível {profile.infos["level"]}', font=fonts['status'], color='white')
        bg.text((245, 165), f'XP {profile.get_needed_xp()}', font=fonts['status'], color='white')
        bg.text((10, 300), profile.infos['description'], font=fonts['descr'], color='white')

        return bg

    def get_fonts(self):
        fonts = {
        'main' : Font(os.path.join(sys.path[0], 'fonts/FreeMono.ttf')).poppins(size=30),
        'status': Font(os.path.join(sys.path[0], 'fonts/FreeMonoBoldOblique.ttf')).poppins(size=32),
        'rank' : Font(os.path.join(sys.path[0], 'fonts/FreeMonoBoldOblique.ttf')).poppins(size=18),
        'descr': Font(os.path.join(sys.path[0], 'fonts/FreeMonoBoldOblique.ttf')).poppins(size=30)
        }
        
        return fonts

    @create.error
    async def create_handler(self, ctx, error):
        if not isinstance(error, commands.NoPrivateMessage):
            response = 'Erro ao criar o seu perfil'
            await ctx.reply(response, mention_author=False)
            print(error)

    @delete.error
    async def create_handler(self, ctx, error):
        if not isinstance(error, commands.NoPrivateMessage):
            response = 'Erro ao excluir o seu perfil'
            await ctx.reply(response, mention_author=False)

            print(error)

    @profile.error
    async def profile_handler(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            return
        if isinstance(error, commands.BadArgument):
            await self.profile(ctx)

        else:
            response = 'Erro ao carregar perfil'
            await ctx.reply(response, mention_author=False)

            print(error)


def setup(bot):
    bot.add_cog(Profiles(bot))
