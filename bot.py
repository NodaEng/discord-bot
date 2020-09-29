# -*- coding: utf-8 -*-

import discord
import time
import random
import asyncio
import re

SERVER_ID = 750464085614919702
MAIN_TEXT_CHANNEL_ID = 750464086197797010
SECRET_TEXT_CHANNEL_ID = 751798622793891890
MAIN_VOICE_CHANNEL_ID = 750464086197797011

MAX_DICE_FACES = 1000

main_text_channel = None
secret_text_channel = None
main_voice_channel = None
bot_voice = None
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
    'd': lambda m: roll_dice(m),
    'vida': lambda m: show_life(m),
    'mana': lambda m: show_mana(m),
    'items': lambda m: list_items(m),
    'ajuda': lambda m: print_commands(m),
    'nome': lambda m: define_name(m),
    'sussurrar': lambda m: whisper(m),
    'falar': lambda m: undeafen_all(m),
    'silenciar': lambda m: mute(m),
    'desmutar': lambda m: unmute_all(m),
    'limpar': lambda m: clean_chat(m),
    'obg': lambda m: send_message(f"""Não tem por onde {m.author.mention}"""),
    'obrigado': lambda m: send_message(f"""Não tem por onde {m.author.mention}"""),

    'puta': lambda m: taunt(m),
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

taunt_dict = {
    'puta': lambda player: send_message(f"""Sua mãe não está nessa aventura, {player.nick}."""),
    'quero fuder': lambda player: send_message(f"""Eu tenho o feitiço **!sussurrar [amante]**, ele faz só os dois (ou mais) se escutarem.
Mas só o Mestre tem esse poder... (͠≖ ͜ʖ͠≖)"""),
    'vai toma no cu': lambda player: send_message(f"""To indo aí tomar nesse teu cu de piscina. (っ⌒‿⌒)っ"""),

}


def read_token():
    with open('token.txt', 'r') as f:
        lines = f.readlines()
        return lines[0].strip()


token = read_token()

client = discord.Client()


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


@client.event
async def on_connect():
    await client.wait_until_ready()


@client.event
async def on_ready():
    await set_text_channels()
    await set_voice_channels()
    await set_all_nicknames()
    await main_text_channel.send(f"""Cheguei, to pronto pra te ajudar.""")


@client.event
async def on_member_join(member):
    global joined
    joined += 1
    for channel in member.server.channels:
        if str(channel) == 'geral':
            await main_text_channel.send(f"""Bem-vindo à nossa távola de aventuras, {member.mention}""")


@client.event
async def on_message(message):
    await update_log(f'[{time.strftime("%H:%M:%S. %d/%m/%Y", time.gmtime())}] {message.author.nick}: {message.content}\n')

    if not client.is_ready():
        return

    global messages
    messages += 1

    id = client.get_guild(SERVER_ID)

    if message.content[0] == '!':
        try:
            await function_dict[get_function(message)](message)

        except KeyError as e:
            print(e)

            command = message.content.split(' ')[0]
            regex = re.compile('!(\d*)d(\d+)')

            # Check if function is a dice roll
            if message.content[1] == 'd':
                try:
                    await roll_dice(message, faces=int(message.content.split(' ')[0][2:]))
                    return

                except ValueError as e:
                    print(e)

            elif regex.search(command):
                try:
                    rolls = int(regex.findall(command)[0][0])
                    sides = int(regex.findall(command)[0][1])
                    total = 0

                    for _ in range(rolls):
                        result = await roll_dice(message, faces=sides)
                        total += result

                    await message.channel.send(f"""Total: **{total}**""")
                    return

                except ValueError as e:
                    print(e)

            await message.channel.send(f"""Não entendi o que quis dizer.""")


@client.event
async def on_member_update(before, after):
    global bot_update
    if bot_update:
        return

    if after.nick:
        if before.top_role == 'Mestre':
            bot_update = True
            await after.edit(nick='Mestre')
            await main_text_channel.send(f"""Me recuso a chamá-lo de outra coisa senão de Mestre.""")
            bot_update = False


        elif before.name not in defined_names.keys():
            bot_update = True
            await after.edit(nick=before.nick)
            await main_text_channel.send(f"""Digite **!nome Nome** para definir o seu nome nessa aventura.""")
            bot_update = False

        elif before.name in defined_names.keys() and after.nick not in defined_names.values():
            bot_update = True
            await after.edit(nick=defined_names[after.name])
            await main_text_channel.send(f"""Você já escolheu teu nome {after.mention}.""")
            bot_update = False

        else:
            return


def get_function(message):
    return message.content.split(' ')[0][1:]


def get_args(message):
    return message.content.split(' ')[1:]


def get_taunt(message):
    pass


async def set_text_channels():
    global main_text_channel, secret_text_channel
    main_text_channel = client.get_channel(MAIN_TEXT_CHANNEL_ID)


async def set_voice_channels():
    global main_voice_channel, bot_voice
    main_voice_channel = client.get_channel(MAIN_VOICE_CHANNEL_ID)
    bot_voice = await main_voice_channel.connect()


async def set_all_nicknames():
    for member in main_voice_channel.members:
        if member.name in defined_names.keys():
            try:
                await member.edit(nick=defined_names[member.name])

            except discord.errors.Forbidden as e:
                print(e)
                print(f'Não tenho permissão suficiente para mudar o nome de {member.name}')


async def roll_dice(message, faces=None):
    try:
        faces = faces if faces != None else message.int(get_args(message)[0])

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


async def define_name(message):
    if message.author.top_role == 'Mestre':
        await main_text_channel.send(f"""Seu nome sempre será Mestre.""")
        return

    defined_name = ' '.join(get_args(message)).capitalize()
    defined_names[message.author.name] = defined_name
    print(f"""'{message.author.name}': '{defined_name}'""")
    await message.author.edit(nick=defined_name)


async def whisper(message):
    if not message.author.top_role == 'Mestre':
        await main_text_channel.send(f"""Somente o Mestre tem permissão para usar um feitiço tão poderoso.""")

    deaf_players = [member for member in main_voice_channel.members
                    if (member.nick not in get_args(message)
                        or member.name not in get_args(message))
                    and member != message.author]

    for member in deaf_players:
        await member.edit(deafen=True)


async def mute(message):
    if not message.author.top_role == 'Mestre':
        await main_text_channel.send(f"""Somente o Mestre tem permissão para usar um feitiço tão poderoso.""")

    players = [member for member in main_voice_channel.members if str(member.top_role) == 'Aventureiro'
               and member.nick in get_args(message)]

    for player in players:
        await player.edit(mute=True)


async def undeafen_all(message):
    if not message.author.top_role == 'Mestre':
        await main_text_channel.send(f"""Somente o Mestre tem permissão para usar um feitiço tão poderoso.""")

    players = [member for member in main_voice_channel.members if str(member.top_role) == 'Aventureiro']

    for player in players:
        await player.edit(deafen=False)


async def unmute_all(message):
    if not message.author.top_role == 'Mestre':
        await main_text_channel.send(f"""Somente o Mestre tem permissão para usar um feitiço tão poderoso.""")

    players = [member for member in main_voice_channel.members if str(member.top_role) == 'Aventureiro']

    for player in players:
        await player.edit(mute=False)


async def send_message(text):
    main_text_channel.send(text)


async def taunt(message):
    await taunt_dict[get_taunt(message)](message.author)


async def clean_chat(message):
    if not message.author.top_role == 'Mestre':
        await main_text_channel.send(f"""Somente o Mestre tem permissão para usar um feitiço tão poderoso.""")

    while True:
        messages_to_delete = [sent_message async for sent_message in main_text_channel.history(limit=100)
                              if not sent_message.pinned]
        if len(messages_to_delete) == 0:
            await main_text_channel.send(f"""Apaguei todas as mensagens Mestre, agora está tudo no passado.""")
            return
        await main_text_channel.delete_messages(messages_to_delete)
        # for message_to_delete in messages_to_delete:
        #     await message_to_delete.delete()


async def print_commands(message):
    if str(message.author.top_role) == 'Mestre':
        await main_text_channel.send(f"""Tem algumas coisas que eu sei fazer:

!d[número de lados] - Rolo um dado para você.

!sussurrar[membro(s)] - Eu uso um feitiço para que ninguém escute o que você irá falar com a(s) pessoa(s).
!falar - Eu desfaço o feitiço de sussurrar.

!silenciar[membro(s)] - Eu uso um feitiço que silencia um aventureiro (Exclusivo de Mestre)
!desmutar - Eu desfaço o feitiço de silenciar.
""")

    else:
        await main_text_channel.send(f"""Tem algumas coisas que eu sei fazer:

!d[número de lados] - Rolo um dado para você.
!nome - Use com sabedoria para definir seu nome nessa aventura.]


""")


client.loop.create_task(update_stats())
client.run(token)
