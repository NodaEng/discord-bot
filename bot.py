# -*- coding: utf-8 -*-

import time

import discord
from discord.ext import commands

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
        with open('log.txt', 'a') as f:
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
            'regex': '!(?P<number_of_dice>\d*)(?P<function>d)(?P<number_of_sides>\d+)(?P<modifier>(?<=\+)\s*)',
            'function': lambda self, *args, **kwargs:
            self.roll_dice(args, kwargs)
        }

    ]

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

    async def save_info(self, ctx, info_key, info_value):
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

    @commands.command(name='for')
    async def set_strength(ctx, value):
        await RpgClient.save_info(ctx, ctx, 'for', value)

    @commands.command(name='des')
    async def set_dexterity(ctx, value):
        await RpgClient.save_info(ctx, ctx, 'des', value)

    @commands.command(name='con')
    async def set_constitution(ctx, value):
        await RpgClient.save_info(ctx, ctx, 'con', value)

    @commands.command(name='int')
    async def set_intelligence(ctx, value):
        await RpgClient.save_info(ctx, ctx, 'int', value)

    @commands.command(name='sab')
    async def set_wisdom(ctx, value):
        await RpgClient.save_info(ctx, ctx, 'sab', value)

    @commands.command(name='car')
    async def set_charisma(ctx, value):
        await RpgClient.save_info(ctx, ctx, 'car', value)

    @commands.command(name='san')
    async def set_sanity(ctx, value):
        await RpgClient.save_info(ctx, ctx, 'san', value)


if __name__ == '__main__':
    client = RpgClient('!')
    # client.loop.create_task(update_stats())
    client.run(token)
