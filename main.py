import os
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

    if client.user in message.mentions:
        char_channel = client.get_channel(CHAR_ID)
        situation_channel = client.get_channel(SITUATION_ID)
        distination_channel = client.get_channel(THEME_ID)

        print('mention detected')
        print(message.content)
        if 'situation:' in message.content:
            print('situation received')
            await situation_channel.send(message.content.split(':')[1])

        if 'character:' in message.content:
            print('character received')
            print(message.embeds)
            await char_channel.send(message.content.split(':')[1], message.embeds)

        else:
            situations = await situation_channel.history(limit=HISTORY_LIMIT).flatten()
            situations_sorted = sorted(situations, key=lambda x: sum([emoji.count if str(emoji) == '👍' else -emoji.count if str(emoji) == '👎' else 0 for emoji in x.reactions]))
            print([s.content for s in situations_sorted])

            chars = await char_channel.history(limit=HISTORY_LIMIT).flatten()
            chars_sorted = sorted(chars, key=lambda x: sum([emoji.count if str(emoji) == '👍' else -emoji.count if str(emoji) == '👎' else 0 for emoji in x.reactions]))
            print([s.content for s in chars_sorted])

            char = random.choice(list(set(chars_sorted)))
            situation = random.choice(list(set(situations_sorted)))

            await distination_channel.send('キャラクター：' + char.content + '\nシチュエーション：' + situation.content)

client.run(TOKEN)
