# -*- coding: utf-8 -*-

import time
import re

import discord
from discord.ext import commands
from rpg.rpg_commands import roll_die

bot_update = False

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


def read_token():
    with open('token.txt', 'r') as f:
        lines = f.readlines()
        return lines[0].strip()


token = read_token()


async def update_log(text):
    try:
        with open('../log.txt', 'a') as f:
            f.write(text)

    except Exception as e:
        print(e)


class RpgClient(commands.Bot):
    functions = [
        {
            'name': 'play',
            'regex': '!(?P<function>play) (?P<song>.*)',
            'function': lambda self, *args, **kwargs: self.play(args, kwargs)
        },
        {
            'name': 'roll_dice',
            'regex': '!(?P<number_of_rolls>\d*)(?P<function>d)(?P<number_of_faces>\d+)(?P<modifier>(?<=\+)\w*)',
            'function': lambda self, *args, **kwargs:
            self.process_dice_roll(args, kwargs)
        }

    ]

    DICE_ROLL_PATTERN = re.compile('!(?P<number_of_rolls>\d*)(?P<function>d)(?P<number_of_faces>\d+)(?P<have_modifier>\+)?(?P<modifier>(?(have_modifier)\w*|))')

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

    async def on_guild_join(self):
        await client.get_all_channels().send(f"""Olá, muito obrigado por me adicionar nas suas sessões. ≧ ͡• ‿‿ ͡•≦ """)

    async def on_connect(self):
        await update_log('Connected to Discord.')

        await client.wait_until_ready()

    async def on_disconnect(self):
        await update_log('Disconnected from Discord')

    async def on_message(self, message):
        await update_log(
            f'[{time.strftime("%H:%M:%S. %d/%m/%Y", time.gmtime())}] {message.author.nick}: {message.content}\n')

        if message.author == self.user or not message.content:
            return

        await client.wait_until_ready()

        if await self.is_dice_roll(message):
            await self.process_dice_roll(message)

        else:
            await self.process_commands(message)

    async def on_ready(self):
        self.add_command(self.play_song)
        self.add_command(self.set_strength)
        self.add_command(self.set_dexterity)
        self.add_command(self.set_constitution)
        self.add_command(self.set_intelligence)
        self.add_command(self.set_wisdom)
        self.add_command(self.set_charisma)
        self.add_command(self.set_sanity)

        await update_log("Bot ready.")

    async def on_member_join(self, member):
        global joined
        joined += 1
        await member.guild.text_channels[0].send(f"""Bem-vindo à nossa távola de aventuras, {member.mention}""")

    async def on_member_update(self, before, after):
        global bot_update

    @commands.command(name='play')
    async def play_song(self, ctx):
        #         song_name = get_args(message)[0]
        #         song_url = get_args(message)[1] if len(get_args(message)) > 1 else None
        #         song_there = os.path.isfile(f'songs/{song_name}.mp3')
        #
        #         if song_url:
        #             if song_there:
        #                 await message.channel.send(f"""Já existe uma música com esse nome, deseja sobrescrever?
        # :one: Sim.
        # :two: Não.""")
        #                 reply = await self.wait_for('message', check=lambda m: message.author == m.author)
        #                 if reply == 2:
        #                     await update_log(f'Não sobrescreveu a música {song_name}')
        #                     return
        #
        #             # Download
        #
        #         await message.author.voice.channel.connect().play(discord.FFmpegPCMAudio(f'songs/{song_name}.mp3'), )
        pass

    async def set_info(self, ctx, info_key, info_value):
        text_channel_names = [guild.name for guild in ctx.guild.text_channels]

        bot_info = None

        if 'bot-info' not in text_channel_names:
            overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                ctx.guild.me: discord.PermissionOverwrite(read_messages=True)
            }

            bot_info = await ctx.guild.create_text_channel(name='bot-info', overwrites=overwrites)

        else:
            bot_info = ctx.guild.text_channels[text_channel_names.index('bot-info')]

        member_info = None

        async for message in bot_info.history():
            if ctx.author.name == message.content.split('\n')[0]:
                member_info = message

        if not member_info:
            member_info = await bot_info.send(ctx.author.name)

        if '\n' in member_info.content:
            info_list = member_info.content.split('\n')[1:]

            for i, info in enumerate(info_list):
                if info.split(': ')[0] == info_key:
                    info_list[i] = f'{info_key}: {info_value}'
                    break

            else:
                info_list.append(f'{info_key}: {info_value}')

            new_info = ctx.author.name + '\n' + '\n'.join(info_list)

        else:
            new_info = ctx.author.name + f'\n{info_key}: {info_value}'

        await member_info.edit(content=new_info)

    async def get_info(self, ctx, info_key):
        text_channel_names = [guild.name for guild in ctx.guild.text_channels]

        if 'bot-info' not in text_channel_names:
            raise Exception('This server does not have a bot-info text channel.')

        else:
            bot_info = ctx.guild.text_channels[text_channel_names.index('bot-info')]

        member_info = None

        async for message in bot_info.history():
            if ctx.author.name == message.content.split('\n')[0]:
                member_info = message

        if not member_info or '\n' not in member_info.content:
            raise Exception('This member does not have any set info to get.')

        else:
            info_list = member_info.content.split('\n')[1:]

            for i, info in enumerate(info_list):
                if info.split(': ')[0] == info_key:
                    return info.split(': ')[1]

            return None

    @commands.command(name='for')
    async def set_strength(ctx, value):
        await RpgClient.set_info(ctx, ctx, 'for', value)

    @commands.command(name='des')
    async def set_dexterity(ctx, value):
        await RpgClient.set_info(ctx, ctx, 'des', value)

    @commands.command(name='con')
    async def set_constitution(ctx, value):
        await RpgClient.set_info(ctx, ctx, 'con', value)

    @commands.command(name='int')
    async def set_intelligence(ctx, value):
        await RpgClient.set_info(ctx, ctx, 'int', value)

    @commands.command(name='sab')
    async def set_wisdom(ctx, value):
        await RpgClient.set_info(ctx, ctx, 'sab', value)

    @commands.command(name='car')
    async def set_charisma(ctx, value):
        await RpgClient.set_info(ctx, ctx, 'car', value)

    @commands.command(name='san')
    async def set_sanity(ctx, value):
        await RpgClient.set_info(ctx, ctx, 'san', value)

    async def is_dice_roll(self, message):
        print(RpgClient.DICE_ROLL_PATTERN.match(message.content))
        return RpgClient.DICE_ROLL_PATTERN.match(message.content)

    async def process_dice_roll(self, message):
        await message.add_reaction('🎲')

        text_channel = message.channel
        match = RpgClient.DICE_ROLL_PATTERN.match(message.content)

        print(match.groupdict())

        number_of_rolls = match.groupdict()['number_of_rolls']
        number_of_faces = int(match.groupdict()['number_of_faces'])
        modifier = match.groupdict()['modifier']

        print(number_of_rolls, number_of_faces, modifier)

        if number_of_faces > 1000:
            await text_channel.send(f'Um dado com {number_of_faces} lados é muito poderoso para simplesmente usá-lo.')
            return

        if modifier and modifier not in ['for', 'des', 'con', 'int', 'sab', 'car']:
            await text_channel.send(f"""Não entendi qual atributo você quis adicionar, conheço apenas esses 6: `for`, `des`, `con`, `int`, `sab`, `car`.""")

        number_of_rolls = int(number_of_rolls) if number_of_rolls else 1

        total = 0

        for _ in range(number_of_rolls):
            result = roll_die(number_of_faces)
            total += result
            await self.print_emoji_number(text_channel, result)

        author_attribute = int(await self.get_info(message, modifier)) if modifier else 10

        if not author_attribute:
            await text_channel.send(f"Para eu adicionar o seu bônus de atributo, defina eles usando os comandos: `!for`, `!des`, `!con`, `!int`, `!sab`, `!car`")

        total += RpgClient.attribute_bonus_dict[author_attribute]

        await message.channel.send(f""">>> {message.author.mention}
Total: **{total}**""")

    async def print_emoji_number(self, text_channel, number):
        digits = [number_emoji_dict[digit] for digit in str(number)]
        await text_channel.send(f"""{''.join(digits)}""")


if __name__ == '__main__':
    client = RpgClient('!')
    # client.loop.create_task(update_stats())
    client.run(token)
