# -*- coding: utf-8 -*-

import os
import json
import time
import random
import asyncio
import re
import discord
from discord.ext import commands
from discord.utils import get

SERVERS_JSON_PATH = 'servers.json'

messages = joined = 0

defined_names = {
    'Danoninho': 'Mestre',
    'siGGGil': 'Mardar',
    'Karolzinha': 'Lucy',
    'yoko': 'Shinra Okono',
    'Cbola': 'Myma Taru',
}

bot_update = False

function_dict = {
    'ajuda': lambda m: print_commands(m),

    'sussurrar': lambda m: whisper(m),
    'falar': lambda m: undeafen_all(m),
    'silenciar': lambda m: mute(m),
    'desmutar': lambda m: unmute_all(m),

    'nome': lambda m: set_player_name(m),
    'for': lambda m: set_player_strength(m),
    'des': lambda m: set_player_dexterity(m),
    'con': lambda m: set_player_constitution(m),
    'int': lambda m: set_player_intelligence(m),
    'sab': lambda m: set_player_wisdom(m),
    'car': lambda m: set_player_charisma(m),

    'limpar': lambda m: clean_chat(m),

    'obg': lambda m: m.channel.send_message(f"""Não tem por onde {m.author.mention}"""),
    'obrigado': lambda m: m.channel.send_message(m, f"""Não tem por onde {m.author.mention}"""),
}

attribute_bonus_dict = {
    0: -5,
    1: -5,
    2: -4,
    3: -4,
    4: -3,
    5: -3,
    6: -2,
    7: -2,
    8: -1,
    9: -1,
    10: 0,
    11: 0,
    12: 1,
    13: 1,
    14: 2,
    15: 2,
    16: 3,
    17: 3,
    18: 4,
    19: 4,
    20: 5,
    21: 5,
    22: 6,
    23: 6,
    24: 7,
    25: 7,
    26: 8,
    27: 8,
    28: 9,
    29: 9,
    30: 10,
    31: 10,
    32: 11,
    33: 11,
    34: 12,
    35: 12,
    36: 13,
    37: 13,
    38: 14,
    39: 14,
    40: 15,
}

number_emoji_dict = {
    '0': ':zero:',
    '1': ':one:',
    '2': ':two:',
    '3': ':three:',
    '4': ':four:',
    '5': ':five:',
    '6': ':six:',
    '7': ':seven:',
    '8': ':eight:',
    '9': ':nine:',
}

regex_dict = {
    'dice_throw': re.compile(r'!(\d*)[dD](\d+)\+?(\w*)'),

}

servers_json = {}

MAX_DICE_FACES = 1000


def read_token():
    with open('token.txt', 'r') as f:
        lines = f.readlines()
        return lines[0].strip()


token = read_token()


async def update_stats():
    await client.wait_until_ready()
    global messages, joined
    while not client.is_closed():
        try:
            with open('stats.txt', 'a') as f:
                f.write(f'[{time.strftime("%H:%M:%S %d/%m/%Y", time.gmtime())}] ({joined}) {messages}\n')

            messages = 0
            joined = 0

            await asyncio.sleep(30)
        except Exception as e:
            print(e)
            await asyncio.sleep(5)


async def update_log(text):
    try:
        with open('log.txt', 'a') as f:
            f.write(text)

    except Exception as e:
        print(e)


async def set_player_strength(message):
    if str(message.guild.id) not in servers_json.keys():
        servers_json[str(message.guild.id)] = {}

    if message.author.name not in servers_json[str(message.guild.id)].keys():
        servers_json[str(message.guild.id)][message.author.name] = {
            'nome': '',
            'for': 0,
            'des': 0,
            'con': 0,
            'int': 0,
            'sab': 0,
            'car': 0
        }

    servers_json[str(message.guild.id)][message.author.name]['for'] = int(get_args(message)[0])

    save_servers_json()


async def set_player_dexterity(message):
    if str(message.guild.id) not in servers_json.keys():
        servers_json[str(message.guild.id)] = {}

    if message.author.name not in servers_json[str(message.guild.id)].keys():
        servers_json[str(message.guild.id)][message.author.name] = {
            'nome': '',
            'for': 0,
            'des': 0,
            'con': 0,
            'int': 0,
            'sab': 0,
            'car': 0
        }

    servers_json[str(message.guild.id)][message.author.name]['des'] = int(get_args(message)[0])

    save_servers_json()


async def set_player_constitution(message):
    if str(message.guild.id) not in servers_json.keys():
        servers_json[str(message.guild.id)] = {}

    if message.author.name not in servers_json[str(message.guild.id)].keys():
        servers_json[str(message.guild.id)][message.author.name] = {
            'nome': '',
            'for': 0,
            'des': 0,
            'con': 0,
            'int': 0,
            'sab': 0,
            'car': 0
        }

    servers_json[str(message.guild.id)][message.author.name]['con'] = int(get_args(message)[0])

    save_servers_json()


async def set_player_intelligence(message):
    if str(message.guild.id) not in servers_json.keys():
        servers_json[str(message.guild.id)] = {}

    if message.author.name not in servers_json[str(message.guild.id)].keys():
        servers_json[str(message.guild.id)][message.author.name] = {
            'nome': '',
            'for': 0,
            'des': 0,
            'con': 0,
            'int': 0,
            'sab': 0,
            'car': 0
        }

    servers_json[str(message.guild.id)][message.author.name]['int'] = int(get_args(message)[0])

    save_servers_json()


async def set_player_wisdom(message):
    if str(message.guild.id) not in servers_json.keys():
        servers_json[str(message.guild.id)] = {}

    if message.author.name not in servers_json[str(message.guild.id)].keys():
        servers_json[str(message.guild.id)][message.author.name] = {
            'nome': '',
            'for': 0,
            'des': 0,
            'con': 0,
            'int': 0,
            'sab': 0,
            'car': 0
        }

    servers_json[str(message.guild.id)][message.author.name]['sab'] = int(get_args(message)[0])

    save_servers_json()


async def set_player_charisma(message):
    if str(message.guild.id) not in servers_json.keys():
        servers_json[str(message.guild.id)] = {}

    if message.author.name not in servers_json[str(message.guild.id)].keys():
        servers_json[str(message.guild.id)][message.author.name] = {
            'nome': '',
            'for': 0,
            'des': 0,
            'con': 0,
            'int': 0,
            'sab': 0,
            'car': 0
        }

    servers_json[str(message.guild.id)][message.author.name]['car'] = int(get_args(message)[0])

    save_servers_json()


async def set_player_name(message):
    if str(message.guild.id) not in servers_json.keys():
        servers_json[str(message.guild.id)] = {}

    if message.author.name not in servers_json[str(message.guild.id)].keys():
        servers_json[str(message.guild.id)][message.author.name] = {
            'nome': '',
            'for': 0,
            'des': 0,
            'con': 0,
            'int': 0,
            'sab': 0,
            'car': 0
        }

    servers_json[str(message.guild.id)][message.author.name]['nome'] = ' '.join(get_args(message))

    save_servers_json()


async def print_commands(message):
    if str(message.author.top_role) == 'Mestre':
        await message.channel.send(f"""Tem algumas coisas que eu sei fazer:

!d[número de lados] - Rolo um dado para você.

!sussurrar[membro(s)] - Eu uso um feitiço para que ninguém escute o que você irá falar com a(s) pessoa(s).
!falar - Eu desfaço o feitiço de sussurrar.

!silenciar[membro(s)] - Eu uso um feitiço que silencia um aventureiro (Exclusivo de Mestre)
!desmutar - Eu desfaço o feitiço de silenciar.
""")

    else:
        await message.channel.send(f"""Tem algumas coisas que eu sei fazer:

!d[número de lados] - Rolo um dado para você.
!nome - Use com sabedoria para definir seu nome nessa aventura.]


""")


def get_function(message):
    return message.content.split(' ')[0][1:]


def get_args(message):
    return message.content.split(' ')[1:]


async def define_name(message):
    if message.author.top_role == 'Mestre':
        await message.channel.send(f"""Seu nome sempre será Mestre.""")
        return

    defined_name = ' '.join(get_args(message)).capitalize()
    defined_names[message.author.name] = defined_name
    print(f"""'{message.author.name}': '{defined_name}'""")
    await message.author.edit(nick=defined_name)


async def whisper(message):
    if not message.author.top_role == 'Mestre':
        await message.channel.send(f"""Somente o Mestre tem permissão para usar um feitiço tão poderoso.""")

    deaf_players = [member for member in message.author.voice.channel.members
                    if (member.nick not in get_args(message)
                        or member.name not in get_args(message))
                    and member != message.author]

    for member in deaf_players:
        await member.edit(deafen=True)


async def mute(message):
    if not message.author.top_role == 'Mestre':
        await message.channel.send(f"""Somente o Mestre tem permissão para usar um feitiço tão poderoso.""")

    players = [member for member in message.author.voice.channel.members if str(member.top_role) == 'Aventureiro'
               and member.nick in get_args(message)]

    for player in players:
        await player.edit(mute=True)


async def undeafen_all(message):
    if not message.author.top_role == 'Mestre':
        await message.channel.send(f"""Somente o Mestre tem permissão para usar um feitiço tão poderoso.""")

    players = [member for member in message.author.voice.channel.members if str(member.top_role) == 'Aventureiro']

    for player in players:
        await player.edit(deafen=False)


async def unmute_all(message):
    if not message.author.top_role == 'Mestre':
        await message.channel.send(f"""Somente o Mestre tem permissão para usar um feitiço tão poderoso.""")

    players = [member for member in message.author.voice.channel.members if str(member.top_role) == 'Aventureiro']

    for player in players:
        await player.edit(mute=False)


def load_servers_json(path=SERVERS_JSON_PATH):
    global servers_json

    with open(path) as json_file:
        servers_json = json.load(json_file)


def save_servers_json(path=SERVERS_JSON_PATH):
    global servers_json

    with open(path, 'w') as outfile:
        json.dump(servers_json, outfile)


class RpgClient(discord.Client):
    BOT_PREFIX = '!'

    async def on_guild_join(self):
        await client.get_all_channels().send(f"""Olá, muito obrigado por me adicionar nas suas sessões. ≧ ͡• ‿‿ ͡•≦ """)

    async def on_connect(self):
        await update_log('Connected to Discord.')

        load_servers_json()

        await client.wait_until_ready()

    async def on_disconnect(self):
        await update_log('Disconnect from Discord')

    async def on_message(self, message):
        await update_log(f'[{time.strftime("%H:%M:%S. %d/%m/%Y", time.gmtime())}] {message.author.nick}: {message.content}\n')

        if message.author == self.user or not message.content:
            return

        await client.wait_until_ready()

        global messages
        messages += 1

        if message.content[0] == '!':
            print(message.content)

            command = message.content.split(' ')[0]

            if regex_dict['dice_throw'].search(command):
                return await self.roll_dice(message)

            else:
                try:
                    await function_dict[get_function(message)](message)

                except Exception as e:
                    print(e)
                    await message.channel.send(f"""Não entendi o que quis dizer.""")

    async def on_message_delete(self, message):
        await message.channel.send(f"""Não adianta apagar não. ( ͡≖( ͡≖ ͜ʖ ͡≖( ͡≖ ͜ʖ ͡≖) ͡≖ ͜ʖ ͡≖) ͡≖)""")

    async def on_ready(self):
        await update_log("Bot ready.")

    async def on_member_join(self, member):
        global joined
        joined += 1
        await member.guild.text_channels[0].send(f"""Bem-vindo à nossa távola de aventuras, {member.mention}""")

    async def on_member_update(self, before, after):
        global bot_update
        if bot_update:
            return

        if after.nick:
            if before.top_role == 'Mestre':
                bot_update = True
                await after.edit(nick='Mestre')
                await after.guild.text_channels[0].send(f"""Me recuso a chamá-lo de outra coisa senão de Mestre.""")
                bot_update = False

            elif before.name not in defined_names.keys():
                bot_update = True
                await after.edit(nick=before.nick)
                await after.guild.text_channels[0].send(f"""Digite **!nome Nome** para definir o seu nome nessa aventura.""")
                bot_update = False

            elif before.name in defined_names.keys() and after.nick not in defined_names.values():
                bot_update = True
                await after.edit(nick=defined_names[after.name])
                await after.guild.text_channels[0].send(f"""Você já escolheu teu nome {after.mention}.""")
                bot_update = False

            else:
                return

        # elif after.roles:

    async def roll_die(self, message, faces=None):
        try:
            faces = faces if faces else message.int(get_args(message)[0])

            if faces <= MAX_DICE_FACES:
                roll_result = str(random.randint(1, faces))
                digits = [number_emoji_dict[digit] for digit in roll_result]
                await message.channel.send(f"""{''.join(digits)}""")
                return int(roll_result)

            elif faces > MAX_DICE_FACES:
                await message.channel.send(f"""Um dado com {faces} lados é muito poderoso para simplesmente usá-lo.""")
                return

            else:
                await message.channel.send(f"""Como é um dado com nenhum lado?""")
                return

        except IndexError as ie:
            print(ie)
            await message.channel.send(f"""Para rolar um dado, insira o número de lados dele.
ex: **!d20**""")

        except AttributeError as ae:
            print(ae)
            await message.channel.send(f"""Para rolar um dado, insira o número de lados dele.
ex: **!d20**""")

    async def roll_dice(self, message):
        await update_log('Add game_die emoji as reaction.')
        await message.add_reaction('🎲')

        command = message.content.split(' ')[0]

        try:
            args = regex_dict['dice_throw'].findall(command)[0]
            rolls = int(args[0]) if args[0] else 1
            sides = int(args[1])
            attribute = str(args[2]) if len(args) == 3 else None
            total = 0

            for _ in range(rolls):
                total += await self.roll_die(message, faces=sides)

            if attribute:
                if attribute not in ['for', 'des', 'con', 'int', 'sab', 'car']:
                    await message.channel.send(f"""```diff
- Não entendi qual atributo você quis adicionar, conheço apenas esses 6:
+ for
+ des
+ con
+ int
+ sab
+ car
```""")
                    return

                global servers_json

                if str(message.guild.id) not in servers_json:
                    servers_json[str(message.guild.id)] = {}
                    await message.channel.send(f"""```diff
- Para eu adicionar o seu bônus de atributo, defina eles usando os comandos:
+ !for 
+ !des 
+ !con
+ !int
+ !sab
+ !car
```""")
                    return

                if message.author.name in servers_json[str(message.guild.id)]:
                    attribute_value = servers_json[str(message.guild.id)][message.author.name][attribute]
                    total += attribute_bonus_dict[attribute_value]

                else:
                    await message.channel.send(f"""```diff
- Para eu adicionar o seu bônus de atributo, defina eles usando os comandos:
+ !for 
+ !des 
+ !con
+ !int
+ !sab
+ !car
```""")

            await message.channel.send(f""">>> {message.author.mention    }
Total: **{total}**""")
            return

        except ValueError as e:
            print(e)

    async def play_song(self, message):
        song_name = get_args(message)[0]
        song_url = get_args(message)[1] if len(get_args(message)) > 1 else None
        song_there = os.path.isfile(f'{song_name}.mp3')

        if song_url:
            if song_there:
                await message.channel.send(f"""Já existe uma música com esse nome, deseja sobrescrever?
:one: Sim.
:two: Não.""")
                reply = await self.wait_for('message', check=lambda m: message.author == m.author)
                if reply == 2:
                    await update_log(f'Não sobrescreveu a música {song_name}')
                    return

            # Download

        await message.author.voice.channel.connect().play(discord.FFmpegPCMAudio(f'{song_name}.mp3'), )


client = RpgClient()
client.loop.create_task(update_stats())
client.run(token)