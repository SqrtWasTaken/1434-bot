import os
dirname = os.path.dirname(__file__)
output_file = os.path.join(dirname, 'output.txt')

import random
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
if TOKEN is None:
    raise ValueError("Discord bot TOKEN environment variable not set.")

OWNERID_STR = os.getenv("OWNERID")
if OWNERID_STR is None:
    raise ValueError("Discord bot OWNERID environment variable not set.")
OWNERID = int(OWNERID_STR)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

emoji = '<:1434:1289227580209106977>' # YOUR EMOJI ID HERE
m = ['MIT', 'Math']
t = ['Tilted', 'Thoroughly', 'Turtle']
s = ['Students', 'Splash']

@bot.event
async def on_ready() -> None:
    await bot.tree.sync()
    print(f"Logged in as {bot.user}")

@bot.event
async def on_message(message) -> None:
    if message.author.bot:
        return
    words = message.content.split()

    # Check guilds and members
    if message.author.id == OWNERID and words[0] == 'LISTGUILDS':
        x = ''
        if len(words) == 2 or len(words) == 3:
            if len(words) == 2:
                n = 1
            else:
                n = int(words[2])
            x = 'Members in ' + bot.guilds[int(words[1])].name + ' (' + str(20*(n-1)+1) + '-' + str(min(20*n, len(bot.guilds[int(words[1])].members))) + '):\n'
            for member in bot.guilds[int(words[1])].members[20*(n-1):20*n]:
                x += str(member) + '\n'
        else:
            x = '*Guilds: ' + str(len(bot.guilds)) + '*\n'
            i=0
            for guild in bot.guilds:
                x += str(i) + ': ' + guild.name + ' *(' + str(len([x for x in guild.members if not x.bot])) + ' humans, ' + str(len([x for x in guild.members if x.bot])) + ' bots)*\n'
                i += 1
        await message.channel.send(x)
        return

    # 1434 reaction
    i = 0
    while i+3 < len(words):
        if len(words[i]) == 1 and len(words[i+1]) == 4 and len(words[i+2]) == 3 and len(words[i+3]) == 4:
            await message.add_reaction(emoji)
            with open(output_file, 'a') as f:
                f.write('\n'+' '.join(words[i:i+4]))
            break
        i += 1
    
    # are you a woman reaction
    i = 0
    while i+3 < len(words):
        if len(words[i]) == 3 and len(words[i+1]) == 3 and len(words[i+2]) == 1 and len(words[i+3]) == 5:
            await message.add_reaction('🫵')
            await message.add_reaction('👩')
            await message.add_reaction('❓')
            with open(output_file, 'a') as f:
                f.write('\n'+' '.join(words[i:i+4]))
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

@bot.tree.command(name="echo", description="If the bot says strange things, this is why.")
async def echo(interaction: discord.Interaction, message: str) -> None:
    if interaction.user.id == OWNERID:
        await interaction.channel.send(message) # type: ignore
        await interaction.response.send_message(f"Sent!", ephemeral=True)
    else:
        await interaction.response.send_message(f"This does not do anything except make you lose the game.", ephemeral=True)

bot.run(TOKEN)
