import os
dirname = os.path.dirname(__file__)
data_file = os.path.join(dirname, '1434_data.db')

import random
import discord
from discord.ext import commands
from dotenv import load_dotenv
import sqlite3
from datetime import datetime


# load sensitive info
load_dotenv()

TOKEN_1434 = os.getenv("TOKEN_1434")
if TOKEN_1434 is None:
    raise ValueError("Discord bot TOKEN_1434 environment variable not set.")

OWNERID_STR = os.getenv("OWNERID")
if OWNERID_STR is None:
    raise ValueError("Discord bot OWNERID environment variable not set.")
OWNERID = int(OWNERID_STR)


# variables
emoji_1434 = '<:1434:1289227580209106977>'
emoji_33 = '<:33:1420238524313108661>'
m = ['MIT', 'Math']
t = ['Tilted', 'Thoroughly', 'Turtle']
s = ['Students', 'Splash']


# functions
async def reaction(name, numbers, emojis, message, words):
    i = 0
    while i+len(numbers)-1 < len(words):
        for j in range(len(numbers)):
            if len(words[j]) != numbers[j]:
                break
        else:
            for e in emojis:
                await message.add_reaction(e)

            conn = sqlite3.connect(data_file)
            cursor = conn.cursor()
            cursor.execute('INSERT INTO messages (text, reaction_type, timestamp) VALUES (?, ?, ?)',
                (' '.join(words[i:(i+len(numbers))]), 
                    name, 
                    int(datetime.fromisoformat(str(message.created_at)).timestamp())
                )
            )

            cursor.execute('SELECT count_'+name+' FROM users WHERE user_id=?', (message.author.id,))
            row = cursor.fetchone()

            if row is None:
                cursor.execute('INSERT INTO users (user_id) VALUES (?)', (message.author.id,))

            cursor.execute('UPDATE users SET count_'+name+' = count_'+name+'+1 WHERE user_id=?', (message.author.id,))

            conn.commit()
            conn.close()
        i += 1


# setup sqlite
conn = sqlite3.connect(data_file)
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT,
        reaction_type TEXT,
        timestamp INTEGER
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        count_1434 INTEGER DEFAULT 0,
        count_3315 INTEGER DEFAULT 0,
        count_3345 INTEGER DEFAULT 0
    )
''')
conn.commit()
conn.close()


# bot setup
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready() -> None:
    await bot.tree.sync()
    print(f"Logged in as {bot.user}")


# message events
@bot.event
async def on_message(message) -> None:
    if message.author.bot:
        return
    words = message.content.split()


    # Check guilds and members (just for me)
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


    # reactions
    await reaction('1434', [1,4,3,4], [emoji_1434], message, words)
    await reaction('3345', [3,3,4,5], [emoji_33], message, words)
    await reaction('3315', [3,3,1,5], ['🫵', '👩', '❓'], message, words)


    # acronym recognition
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


# dumb echo command
@bot.tree.command(name="echo", description="If the bot says strange things, this is why.")
async def echo(interaction: discord.Interaction, message: str) -> None:
    if interaction.user.id == OWNERID:
        await interaction.channel.send(message) # type: ignore
        await interaction.response.send_message(f"Sent!", ephemeral=True)
    else:
        await interaction.response.send_message(f"This does not do anything except make you lose the game.", ephemeral=True)



bot.run(TOKEN_1434)