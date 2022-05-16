import json
import os
import sys
import random


def get_msg_type(message) -> str:
    types_dict = bot_dict('input')
    msg = message.content.lower()

    msg_type = check_msg_type(types_dict, msg)

    return msg_type


def check_msg_type(types_dict, msg):
    msg_type = ''
    for Type, lst in types_dict.items():
        for item in lst:
            case1 = f'"{item}"' in msg
            case2 = f"'{item}'" in msg

            if case1 or case2:
                continue
            if item in msg:
                msg_type = Type

    return msg_type


def responses(message) -> dict:
    d = bot_dict('responses')

    author = message.author.display_name
    for k, v in d.items():
        d[k] = random.choice(v).format(author)

    return d


def bot_dict(mode: str) -> dict:
    arq = os.path.join(sys.path[0], 'dicts/dictfortalks.json')
    with open(arq, encoding='utf-8') as j:
        d = json.load(j)

    return d[mode]
