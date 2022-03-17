import requests
import discord
from discord.ext import commands
from googletrans import Translator

class Bible(commands.Cog):
    '''Mostra Versículos da Bíblia atravez de um comando'''

    __slots__ = ('bot')

    def __init__(self, bot):
        self.bot = bot

    
    @commands.command(name='bible', help='Mostra versículos da Bíblia', aliases=['b'], description="-b Livro Capítulo:Versículo")
    async def bible(self, ctx, book = None, chapter_verse = None):
        none = book == None or chapter_verse == None
        
        if none:
            await ctx.channel.send('Por favor, tente digitar ``-b Livro Capítulo:Versículo``', 
            reference = ctx.message, mention_author = False)
        
        else:
            book = self.translator(book)
            request = self.request(book, chapter_verse)
            await self.CheckRequest(ctx, request)

    
    def translator(self, book):
        book = book.lower()

        erro = self.transerro()
        tr = Translator()

        if book in erro: book = erro[book]  
        else: book = tr.translate(book).text
        
        return book


    def request(self, book, chapter_verse):
        request = requests.get(f'https://bible-api.com/{book}+{chapter_verse}?translation=almeida&verse_numbers=true')
        request = request.json()
        
        return request


    def transerro(self):
        '''Mesmo usando uma bibliteca do Google Tradutor, 
        alguns dos livros não tinham seus nome traduzidos corretamente,
        Esse método faz a tradução correta dos nomes para a API'''

        dict = {   
            "rute": "RUT", "1reis": "1KI", "2reis": "2KI;", "1crônicas": "1CH",
            "2crônicas": "2CH", "jó": "JOB", "salmos": "PSA","eclesiastes": "ECC",
            "cânticos": "SNG", "oseias": "HOS", "naum": "NAM","ageu": "HAG",
            "1coríntios": "1CO", "2coríntios": "2CO", "efésios": "EPH",
            "filipenses": "PHP", "1tessalonicenses": "1TH", "2tessalonicenses": "2TH",
            "1timóteo": "1TI", "2timóteo": "2TI",
            "1joão": "1JN", "2joão": "2JN","3joão": "3JN"}

        return dict


    def CheckRequest(self, ctx, request):
        '''Checa se o request foi bem sucedido'''

        if 'text' in request:
            textlist = request['text'].split('\xa0 \xa0')
            return self.CreateEmbeds(ctx, textlist, request)
                       
        else:
            return self.embederro(ctx)
            

    async def embederro(self, ctx):
        file = discord.File('images/betozinho_bah.jpeg', filename='betozinho_bah.jpeg')

        embed = discord.Embed(
                title="Não Encontrado", 
                description="Verifique se você digitou ``-b Livro Capítulo:Versículo`` corretamente", 
                color=discord.Color.green())

        
        embed.set_thumbnail(url='attachment://betozinho_bah.jpeg')

        await ctx.reply(embed=embed, file=file, mention_author=False)


    async def CreateEmbeds(self, ctx, textlist, request):
        '''Envia versículos como mensagem no discord, a cada 25 versículos é 
           criada uma nova mensagem por conta da limitção de caracteres'''

        limit = 25
        newtextlist = [textlist[i:i + limit] for i in range(0, len(textlist), limit)]

        for list in newtextlist:
            response = '\n\n'.join(list)
            
            embed = discord.Embed(description=response, color = 0x00B115)
            embed.set_author(name=request['reference'], icon_url=ctx.author.avatar_url)

            await ctx.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Bible(bot)) 