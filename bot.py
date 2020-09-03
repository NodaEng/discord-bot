import discord
import time
import random
import asyncio

SERVER_ID = 750464086197797011
MAIN_VOICE_CHANNEL = None
BOT_VOICE = None
messages = joined = 0
function_dict = {
    'd': lambda m: roll_dice(m),
    'vida': lambda m: show_life(m),
    'mana': lambda m: show_mana(m),
    'items': lambda m: list_items(m),
    'help': lambda m: f(),
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


@client.event
async def on_connect():
    pass


@client.event
async def on_ready():
    MAIN_VOICE_CHANNEL = client.get_channel(SERVER_ID)
    BOT_VOICE = await MAIN_VOICE_CHANNEL.connect()


@client.event
async def on_member_join(member):
    global joined
    joined += 1
    for channel in member.server.channels:
        if str(channel) == 'geral':
            await client.send_message(f"""Welcome to the server {member.mention}""")


@client.event
async def on_message(message):
    global messages
    messages += 1

    id = client.get_guild(750464085614919702)

    await message.author.edit(mute=True)

    if message.content[0] == '!':
        await function_dict[get_function(message)](message)



@client.event
async def on_member_update(before, after):
    n = after.nick


def get_function(message):
    return message.content.split(' ')[0][1:]


def get_args(message):
    return message.content.split(' ')[1:]


async def roll_dice(message):
    await message.channel.send(f'{random.randint(1, int(get_args(message)[0]))}')


client.loop.create_task(update_stats())
client.run(token)
