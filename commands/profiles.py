import re
import discord
from discord.ext import commands
from commands.utils.users import User
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
        if await self.create_user(ctx):
            response = 'Perfil criado! ' + rest_response

        else:
            response = 'Você já tem um perfil! ' + rest_response

        await ctx.reply(response, mention_author=False)

    @awaitable
    def create_user(self, ctx):
        user = User(ctx.author.id)
        created_user = user.create_user()
        user.cursor.close()

        return created_user

    @commands.command(name='profile', help='Ver o seu perfil ou de alguém', description='opcionalmente @user')
    async def profile(self, ctx, mention: discord.User = None):
        def response(response): return ctx.reply(response, mention_author=False)
        
        if mention is None:
            profile = await self.get_user_profile(ctx.author.id)
            if profile:
                file = await self.get_profile_img(ctx.author, profile)
                await ctx.reply(file=file, mention_author=False)

            else:
                await response('Você não tem perfil! Crie um com **-create**')

        else:
            profile = await self.get_user_profile(mention.id)
            if profile:
                file = await self.get_profile_img(mention, profile)
                await ctx.reply(file=file, mention_author=False)

            else:
                await response('Esse usuário não tem perfil')
    
    async def get_profile_img(self, user, profile):
        level = profile['level']
        xp = profile['xp']
        rest = f'/{profile["level"]*20000}' if profile["level"] < 7 else ''
        description = profile['description']
        
        bg = Editor('bg.png')
        avatar = await load_image_async(str(user.avatar_url))
        avatar = Editor(avatar).resize((127, 127)).circle_image()
        bg.paste(avatar.image, (67, 114))

        font1, font2 = self._get_fonts()

        bg.text((10,10), str(user), font=font1, color='white')
        bg.text((270, 150), description,font=font2, color='white')
        bg.text((280, 190), f'Nível: {level}            XP: {str(xp)+rest}',font=font2, color='white')
        
        file = discord.File(fp=bg.image_bytes, filename='card.png')
        
        return file
    
    def _get_fonts(self):
        font1 = Font('/usr/share/fonts/truetype/msttcorefonts/arial.ttf').poppins(size=30)
        font2 =  Font('/usr/share/fonts/truetype/msttcorefonts/arial.ttf').poppins(size=23)
        
        
        return font1, font2
        

    @awaitable
    def get_user_profile(self, id):
        user = User(id)
        profile = user.infos
        user.cursor.close()

        return profile

    @create.error
    async def create_handler(self, ctx, error):
        response = 'Erro ao criar o seu perfil'
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
