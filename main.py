import os
import random
import discord
#from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)

emoji = '<:1434:1289227580209106977>' # YOUR EMOJI ID HERE
m = ['MIT', 'Math']
t = ['Tilted', 'Thoroughly', 'Turtle']
s = ['Students', 'Splash']

@client.event
async def on_ready() -> None:
    print(f"Logged in as {client.user}")

@client.event
async def on_message(message) -> None:
    if message.author == client.user:
        return
    words = message.content.split()

    # Check guilds and members
    if message.author.id == int(os.getenv("OWNERID")) and words[0] == 'LISTGUILDS':
        x = ''
        if len(words) == 2 or len(words) == 3:
            if len(words) == 2:
                n = 1
            else:
                n = int(words[2])
            x = 'Members in ' + client.guilds[int(words[1])].name + ' (' + str(20*(n-1)+1) + '-' + str(min(20*n, len(client.guilds[int(words[1])].members))) + '):\n'
            for member in client.guilds[int(words[1])].members[20*(n-1):20*n]:
                x += str(member) + '\n'
        else:
            x = '*Guilds: ' + str(len(client.guilds)) + '*\n'
            i=0
            for guild in client.guilds:
                x += str(i) + ': ' + guild.name + ' *(' + str(len([x for x in guild.members if not x.bot])) + ' bots, ' + str(len([x for x in guild.members if x.bot])) + ' humans)*\n'
                i += 1
        await message.channel.send(x)
        return
    #

    # 1434 reaction
    i = 0
    while i+3 < len(words):
        if len(words[i]) == 1 and len(words[i+1]) == 4 and len(words[i+2]) == 3 and len(words[i+3]) == 4:
            await message.add_reaction(emoji)
            break
        i += 1
    
    # are you a woman reaction
    i = 0
    while i+3 < len(words):
        if len(words[i]) == 3 and len(words[i+1]) == 3 and len(words[i+2]) == 1 and len(words[i+3]) == 5:
            await message.add_reaction('🫵')
            await message.add_reaction('👩')
            await message.add_reaction('❓')
            break
        i += 1
    
    if len(words) == 1:
        # hmmt
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
            await message.reply(' '.join(msg)[0:2000])
        # tstst
        msg = []
        r = random.random()
        if r<0.9:
            first = True
            for letter in words[0]:
                if letter.lower() == 't':
                    if first:
                        msg.append('Team')
                        first = False
                    else:
                        msg.append('Test')
                elif letter.lower() == 's':
                    msg.append('Selection')
                else:
                    break
            else:
                await message.reply(' '.join(msg)[0:2000])
        else:
            t_count = 0
            s_count = 0
            for letter in words[0]:
                if letter.lower() == 't':
                    msg.append(t[t_count])
                    t_count = (t_count + 1) % 3
                elif letter.lower() == 's':
                    msg.append(s[s_count])
                    s_count = 1-s_count
                else:
                    break
            else:
                await message.reply(' '.join(msg)[0:2000])

client.run(os.getenv("TOKEN"))
