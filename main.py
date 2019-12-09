import os
import io
import random

import discord
from dotenv import load_dotenv

load_dotenv('./.env')
TOKEN = os.getenv('BOT_TOKEN')
HISTORY_LIMIT = int(os.getenv('HISTORY_LIMIT'))
client = discord.Client()

CHAR_ID = 653161082873184267
SITUATION_ID = 653161113558712320
THEME_ID = 653202794987388959

@client.event
async def on_ready():
    print('bot ready')


@client.event
async def on_message(message):
    if message.author.bot:
        return

    char_channel = client.get_channel(CHAR_ID)
    situation_channel = client.get_channel(SITUATION_ID)
    distination_channel = client.get_channel(THEME_ID)

    if 'me' in dir(message.channel):
        print('DM received from {}'.format(message.author))

        if 'situation:' in message.content:
            print('situation received')
            files = [discord.File(io.BytesIO(await f.read()), f.filename) for f in message.attachments]
            await situation_channel.send(message.content.split(':')[1])
            await situation_channel.send(files=files)
            return

        elif 'character' in message.content:
            print('new character arrived')
            files = [discord.File(io.BytesIO(await f.read()), f.filename) for f in message.attachments]
            await char_channel.send(message.content.split(':')[1])
            await char_channel.send(files=files)
            return

        else:
            await message.channel.send('お題を追加してみましょう！')
            await message.channel.send('character:◯◯\nでキャラクターを、')
            await message.channel.send('situation:◯◯\nでシチュエーションを投稿することができます。')
            await message.channel.send('画像を添付すると同様の画像が対象のチャンネルに投稿されます。参考画像を追加すると便利です。')
            return

    if client.user not in message.mentions:
        return

    print('generating new ODAI')
    situations = await situation_channel.history(limit=HISTORY_LIMIT).flatten()
    situations_sorted = sorted(situations, key=lambda x: sum([emoji.count if str(emoji) == '👍' else -emoji.count if str(emoji) == '👎' else 0 for emoji in x.reactions]))
    print([s.content for s in situations_sorted])

    chars = await char_channel.history(limit=HISTORY_LIMIT).flatten()
    chars_sorted = sorted(chars, key=lambda x: sum([emoji.count if str(emoji) == '👍' else -emoji.count if str(emoji) == '👎' else 0 for emoji in x.reactions]))
    print([s.content for s in chars_sorted])

    char = random.choice(list(set(chars_sorted)))
    situation = random.choice(list(set(situations_sorted)))

    await distination_channel.send('キャラクター：' + char.content + '\nシチュエーション：' + situation.content)
    if char.attachments:
        files = [discord.File(io.BytesIO(await f.read()), f.filename) for f in char.attachments]
        await distination_channel.send(files)

    return


client.run(TOKEN)
