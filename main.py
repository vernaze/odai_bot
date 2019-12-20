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
#THEME_ID = 654326252353617933

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
        # reactions in DM
        print('DM received from {}'.format(message.author))

        if 'situation:' in message.content:
            print('situation received')
            await situation_channel.send(message.content.split(':')[1])
            if message.attachments:
                files = [discord.File(io.BytesIO(await f.read()), f.filename) for f in message.attachments]
                await situation_channel.send(files=files)
            return

        elif 'character' in message.content:
            print('new character arrived')
            await char_channel.send(message.content.split(':')[1])
            if message.attachments:
                files = [discord.File(io.BytesIO(await f.read()), f.filename) for f in message.attachments]
                await char_channel.send(files=files)
            return
        else:
            pass
        '''
        else:
            await message.channel.send('お題を追加してみましょう！')
            await message.channel.send('character:◯◯\nでキャラクターを、')
            await message.channel.send('situation:◯◯\nでシチュエーションを投稿することができます。')
            await message.channel.send('画像を添付すると同様の画像が対象のチャンネルに投稿されます。参考画像を追加すると便利です。')
            return
        '''

    if 'https://discordapp.com/channels' in message.content:

        # detect citation like:
        #   https://discordapp.com/channels/serverID/channelID/messageID
        print(f'citation detected: {message.content}')

        message_id = message.content.split('/')[-1]
        cited_channel = client.get_channel(message.content.split('/')[-2])
        written_odai = await cited_channel.fetch_message(message_id)
        print(f'applicable message: {written_odai}')

        if not message.attachments:
            print('no attached images')
            return

        print(f'attached files: {message.attachments}')
        attachment_url = message.attachments[0].url
        embed = discord.Embed().set_image(url=attachment_url)

        attached_file = message.attachments
        await written_odai.edit(
          embed=embed
        )
        return


    # check mentioned to generate ODAI
    if client.user not in message.mentions:
        return

    print('generating new ODAI')

    sum_thumbs = lambda message: sum([emoji.count if str(emoji) == '👍' else -emoji.count if str(emoji) == '👎' else 0 for emoji in message.reactions])

    situations = await situation_channel.history(limit=HISTORY_LIMIT).flatten()
    situations_sorted = sorted(situations, key=sum_thumbs, reverse=True)

    if 'sukebe' not in message.content:
        print('no-echi')
        situations_sorted = [s for s in situations_sorted if '🔞' not in [str(e) for e in s.reactions]]

    if 'dosukebe' in message.content:
        print('echi detected!')
        situations_sorted = [s for s in situations_sorted if '🔞' in [str(e) for e in s.reactions]]

    print([s.content for s in situations_sorted])

    chars = await char_channel.history(limit=HISTORY_LIMIT).flatten()
    chars_sorted = sorted(chars, key=sum_thumbs, reverse=True)
    print([s.content for s in chars_sorted])

    char = random.choice(list(set(chars_sorted)))
    situation = random.choice(list(set(situations_sorted)))

    await distination_channel.send(f'キャラクター： {char.content}\nシチュエーション：{situation.content}')
    if char.attachments:
        print(char.attachments)
        files = [discord.File(io.BytesIO(await f.read()), f.filename) for f in char.attachments]
        await distination_channel.send(files=files)
    if situation.attachments:
        print(situation.attachments)
        files = [discord.File(io.BytesIO(await f.read()), f.filename) for f in situation.attachments]
        await distination_channel.send(files=files)

    return


client.run(TOKEN)
