import os

import discord
#from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

emoji = '<:1434:1179160439167406091>'
m = ['MIT', 'Math']

@client.event
async def on_ready() -> None:
    print(f"Logged in as {client.user}")

@client.event
async def on_message(message) -> None:
    if message.author == client.user:
        return
    words = message.content.split()

    i = 0
    while i+3 < len(words):
        if len(words[i]) == 1 and len(words[i+1]) == 4 and len(words[i+2]) == 3 and len(words[i+3]) == 4:
            await message.add_reaction(emoji)
            break
        i += 1
    
    i = 0
    while i+3 < len(words):
        if len(words[i]) == 3 and len(words[i+1]) == 3 and len(words[i+2]) == 1 and len(words[i+3]) == 5:
            await message.add_reaction('🫵')
            await message.add_reaction('👩')
            await message.add_reaction('❓')
            break
        i += 1
    
    if len(words) == 1:
        m_count = 0
        msg = []
        for letter in words[0]:
            if letter.lower() == 'h':
                msg.append('Harvard')
            elif letter.lower() == 'm':
                msg.append(m[m_count])
                m_count = 1 - m_count
            elif letter.lower() == 't':
                msg.append('Tournament')
            else:
                break
        else:
            await message.reply(' '.join(msg))

client.run(TOKEN)
