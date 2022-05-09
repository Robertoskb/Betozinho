import discord
import requests
import sys
import os
import json
from decouple import config
from aiohttp import ClientSession
from unidecode import unidecode
from commands.utils.serversettings import ServerSettings

API = "https://www.abibliadigital.com.br/api"
COLOR = 0x00B115
HEADERS = {'Authorization': f'Beare {config("bible")}'}


class BibleUtils:

    def general_check(self, request: dict, key: str, method) -> discord.Embed:
        if request.get(key):
            embed = method(request)

        else:
            embed = self.request_msg(request.get('msg'))

        return embed

    @staticmethod
    def split_list(lst: list, limit: int) -> list:
        newlist = [lst[i:i + limit] for i in range(0, len(lst), limit)]

        return newlist

    @staticmethod
    def get_request(url: str) -> dict:
        request = requests.get(url, headers=HEADERS)
        return request.json()

    @staticmethod
    def request_msg(msg: str) -> discord.Embed:
        msgs = {
            'Book not found': 'Livro não econtrado',
            'Chapter not found': 'Capítulo não econtrado',
            'Verse not found': 'Versículo não econtrado',
        }

        response = msgs.get(msg, 'Erro desconhecido')
        embed = discord.Embed(title='Nada encontrado',
                              description=response, color=COLOR)

        return embed

    @staticmethod
    async def post_request(lang, search: str) -> dict:
        data = {"version": lang, "search": search}
        url = f'{API}/verses/search'

        async with ClientSession(trust_env=True) as Session:
            async with Session.post(url, headers=HEADERS, json=data) as request:
                return await request.json()

    @staticmethod
    def get_lang(ctx) -> str:
        if ctx.channel.type == discord.ChannelType.private:
            return 'nvi'

        server = ServerSettings(ctx.guild.id)
        settings = server.get_settings('biblelang')

        return settings

    @staticmethod
    def highlight_search(text: str, search: str) -> str:
        for w in search.split():
            case1 = f'**{w}' in text
            case2 = f'{w}**' in text

            if case1 or case2:
                continue
            else:
                text = text.replace(w, f'**{w}**')

        return text

    @staticmethod
    def get_abbrev(book: str) -> str:
        arq = os.path.join(sys.path[0], 'dicts/dictforbible.json')
        with open(arq, encoding='utf-8') as j:
            Dict = json.load(j)

        return Dict.get(unidecode(book).lower())
