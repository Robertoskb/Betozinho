import discord
import sys
import os
from discord.ext import commands
from commands.utils.users import User
from commands.utils.confirm import Confirm
from easy_pil import Editor, Font, load_image_async

COLOR = 0x00B115


class Profiles(commands.Cog):
    '''Perfis'''

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='create', help='Criar um perfil', description='sem argumentos')
    async def create(self, ctx):
        if ctx.channel.type == discord.ChannelType.private:
            return
        
        rest_response = 'Veja o seu perfil com **-profile**'
        
        if User(ctx.author.id).create_user():
            response = 'Perfil criado! ' + rest_response

        else:
            response = 'Você já tem um perfil! ' + rest_response

        await ctx.reply(response, mention_author=False)

    @commands.command(name='delete', help='Excluir o seu perfil dos meus dados', description='sem argumentos')
    async def delete(self, ctx):
        if ctx.channel.type == discord.ChannelType.private:
            return
        
        if not User(ctx.author.id).infos:
            return await ctx.reply('Você não tem perfil', mention_author=False)

        confirm = Confirm(
            self.bot, ctx, f'Eu vou sentir muita falta de você, {ctx.author.display_name}')

        if await confirm.confirmation():
            User(ctx.author.id).delete_user()
            response = "Perfil excluido do meu banco de dados 😔"

        else:
            response = 'Cancelado 😰'

        await ctx.reply(response, mention_author=False)

    @commands.command(name='profile', aliases=['perfil'], help='Ver o seu perfil ou de alguém', description='opcionalmente @user')
    async def profile(self, ctx, mention: discord.User = None):
        if ctx.channel.type == discord.ChannelType.private:
            return
        
        def response(response): return ctx.reply(
            response, mention_author=False)

        def img(user): return self.get_profile_img(ctx, user, profile)

        if mention is None:
            profile = User(ctx.author.id).infos
            if profile:
                file = await img(ctx.author)
                await ctx.reply(file=file, mention_author=False)

            else:
                await response('Você não tem perfil! Crie um com **-create**')

        else:
            profile = User(mention.id).infos
            if profile:
                file = await img(mention)
                await ctx.reply(file=file, mention_author=False)

            else:
                await response('Esse usuário não tem perfil')

    async def get_profile_img(self, ctx, user, profile):
        bg = await self.get_bg(user)
        bg = self.write_bg(ctx, bg, user, profile)
        
        file = discord.File(fp=bg.image_bytes, filename='card.png')

        return file

    async def get_bg(self, user):
        bg = Editor(os.path.join(sys.path[0], 'images/bgs/bg.png'))
        avatar = await load_image_async(str(user.avatar_url))
        avatar = Editor(avatar).resize((127, 127)).circle_image()
        bg.paste(avatar.image, (67, 114))

        return bg

    def write_bg(self, ctx, bg, user, profile):
        fonts = self.get_fonts()
        rank = User(user.id).get_rank(ctx.guild.members)
        level, xp, description = self.get_profile_infos(profile)

        bg.text((10, 7), user.display_name, font=fonts[0], color='white')
        bg.text( (10, 35), f'#{rank} {ctx.guild.name}', font=fonts[2], color='white')
        bg.text((263, 146), description, font=fonts[1], color='white')
        bg.text((265, 190), f'Nível: {level}    XP: {xp}', font=fonts[1], color='white')

        return bg

    def get_fonts(self):
        font1 = Font(os.path.join(sys.path[0], 'fonts/FreeMono.ttf')).poppins(size=25)
        font2 = Font(os.path.join(sys.path[0], 'fonts/FreeMono.ttf')).poppins(size=23)
        font3 = Font(os.path.join(sys.path[0], 'fonts/FreeMonoBoldOblique.ttf')).poppins(size=18)

        return [font1, font2, font3]

    def get_profile_infos(self, profile):
        level = profile.get('level')
        xp = profile.get('xp')
        description = profile.get('description')

        if type(level) == int and level < 7:
            xp = f'{xp}/{level*20000}'

        return level, xp, description

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
