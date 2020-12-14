

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

regex_dict = {
    'dice_throw': re.compile(r'!(\d*)[dD](\d+)\+?(\w*)'),

}

MAX_DICE_FACES = 1000

class Commands:
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

            await message.channel.send(f""">>> {message.author.mention}
Total: **{total}**""")
            return

        except ValueError as e:
            print(e)