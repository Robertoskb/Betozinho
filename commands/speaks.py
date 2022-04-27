import discord 
import textwrap
import os
import sys
from easy_pil import Editor, Font
from discord.ext import commands


class Speak(commands.Cog):
    """Falas"""
    
    def __init__(self, bot):
        self.bot = bot
    
    
    @commands.command(name='enderman', help='Enderman fala', description="[Fala]")
    async def enderman(self, ctx, *, speech='olleh'):
        speech =  "".join(speech)
        file = self.get_file('enderman', speech)
        
        await ctx.reply(file=file, mention_author=False)
    
    @commands.command(name='creeper', help='Creeper fala', description="[Fala]")
    async def creeper(self, ctx, *, speech='Shhhhhhhhhh'):
        speech =  "".join(speech)
        file = self.get_file('creeper', speech)
        
        await ctx.reply(file=file, mention_author=False)
    
    @commands.command(name='steve', help='Steve fala', description="[Fala]")
    async def steve(self, ctx, *, speech='Eu quero diamantes'):
        speech =  "".join(speech)
        file = self.get_file('steve', speech)
        
        await ctx.reply(file=file, mention_author=False)
    
    @commands.command(name='villager', help='Villager fala', description="[Fala]")
    async def villager(self, ctx, *, speech='hm'):
        speech =  "".join(speech)
        file = self.get_file('villager', speech)
        
        await ctx.reply(file=file, mention_author=False)
    
    @commands.command(name='zombie', help='Zombie fala', description="[Fala]")
    async def zombie(self, ctx, *, speech='bruuh'):
        speech =  "".join(speech)
        file = self.get_file('zombie', speech)
        
        await ctx.reply(file=file, mention_author=False)
    
    def get_file(self, file, speech):
        font = Font(os.path.join(sys.path[0], 'fonts/FreeMono.ttf')).poppins(size=50)
        img = Editor(os.path.join(sys.path[0], f'images/speaks/{file}.png'))
        cx, cy = (925, 350)
        
        lines = textwrap.wrap(speech, 25)
        w, h = font.getsize(speech)
        y_text = cy-(h/2) - (len(lines)*h)/2
        
        for line in lines:
            w, h = font.getsize(line)
            img.text((cx-(w/2), y_text), line, color='white', font=font)
            y_text += h
                   
        return discord.File(fp=img.image_bytes, filename='card.png')


def setup(bot):
    bot.add_cog(Speak(bot))