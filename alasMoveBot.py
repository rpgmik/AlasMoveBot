## Runs in Linux via: python kultTarotBot.py
## Requires Python > 3.4
## Bot needs to be given message read and send permissions on the Discord server.
## Need to install the discord.py API wrapper (e.g., via: pip install discord.py)

import random
import discord

## Ascertain mode: dev or production
m = open('modeFile.txt', "r")
MODE = m.readline().rstrip()
m.close()

## Read in Discord bot token from file
if MODE=="prod":
    tokenFile = 'prodToken.txt'
elif MODE=="dev":
    tokenFile = 'devToken.txt'

f = open(tokenFile, "r")
TOKEN = f.readline().rstrip()
f.close()

## Define variables here...

sep = ' '
gap = ''

aup = ['# Acting Under Pressure', 'SUCCESS!', 'You falter, buckle or break. The GM can offer you a worse outcome, a hard bargain, or an ugly choice.', 'MISS: The GM makes things worse.']

ia = ['# Intimidate Another', 'SUCCESS! They choose: cave in and do what you want, or endure the consequences of your threat', 'They choose one of the following that is within their ability:\n - Get out of your way, for now\n - Give you something they think you want\n - Tell you what you want to know, or what you want to hear','MISS! The GM makes things worse']

awf = ['# Act With Force', 'SUCCESS! Choose 3:\n - You take a definite hold of it, or of the situation\n - You suffer little harm (GM note: -1 to harm suffered)\n - You inflict terrible harm (GM note: +2 to harm inflicted)\n - You impress, dismay, or frighten your enemy', 'Choose 2:\n - You take a definite hold of it, or of the situation\n - You suffer little harm (GM note: -1 to harm suffered)\n - You inflict terrible harm (GM note: +2 to harm inflicted)\n - You impress, dismay, or frighten your enemy','MISS! The GM makes things worse']

map = ['# Manipulate Another (PC)', 'Success! Both of the following:\n - If they do it, they get +1 to their next roll\n - If they refuse, they are ACTING UNDER PRESSURE.', 'Choose 1:\n - If they do it, they get +1 to their next roll\n - If they refuse, they are ACTING UNDER PRESSURE.', 'MISS! The GM makes things worse']

man = ['# Manipulate Another (NPC) - they make you promise something first:', 'Success! It works. Whether you keep the promise later is up to you', 'They change the terms to suit themselves, or demand concrete assurance first', 'MISS! The GM makes things worse']

ras = ['# Read A Situation', 'Success! Ask 3:\n - Who or what is most vulnerable to me?\n - Who or what is the biggest threat?\n - What should I be on the lookout for?\n - Who is in control here?\n - What here is not what it seems?\n - What is my best way in, way out, or way past?', 'Ask 2:\n - Who or what is most vulnerable to me?\n - Who or what is the biggest threat?\n - What should I be on the lookout for?\n - Who is in control here?\n - What here is not what it seems?\n - What is my best way in, way out, or way past?', 'MISS! The GM makes things worse']

rat = ["# Read Another's Thoughts", 'Success! Ask 3:\n - Is this character telling the truth?\n - What does this character need most?\n - What does this character intend to do?\n - What does this character wish I’d do?\n - How can I get your character to _________?', 'Ask 1:\n - Is this character telling the truth?\n - What does this character need most?\n - What does this character intend to do?\n - What does this character wish I’d do?\n - How can I get your character to _________?', 'MISS! The GM makes things worse']

swb = ["# Sense What's Beyond", 'Success! You receive visions and truths', 'You receive fragments and mysteries', 'MISS! The GM makes things worse']

hoh = ['# Help Or Hinder', 'Success! They take +2 or -2', 'They take +1 or -1', 'MISS! The GM makes things worse']

moves = ["aup", "ia", "awf", "man", "map", "ras", "rat", "swb", "hoh"]

## Get discord connection
client = discord.Client()

## Define an event so that Bot can read messages
@client.event
async def on_message(message):

    ## Respond if user sends "!move"
    if message.content.startswith('!move'):

        ## Split into into "!move", the type of Move to undertake, the modifier (if any), and a comment (if any).
        bits = message.content.split(" ")

        dice = '```md\n'
        if len(bits)==1:
            dice += "Please specify a Move"

        if len(bits)>1:
            if bits[1] == "?":
                dice += "# Usage:\n"
                dice += "!move ? - displays this message\n"
                dice += "!move xxx - roll to perform Move xxx\n"
                dice += "!move xxx -1 - roll to perform Move xxx with negative modifier -1\n"
                dice += "!move xxx +2 - roll to perform Move xxx with positive modifier +2\n"
                dice += "# Moves:\n"
                dice += "- Acting Under Pressure (aup): Roll + Balance\n"
                dice += "- Intimidate Another (ia): Roll + Brawn\n"
                dice += "- Act With Force (awf): Roll + Brawn\n"
                dice += "- Manipulate Another - PC (map): Roll + Beauty\n"
                dice += "- Manipulate Another - NPC (man): Roll + Beauty\n"
                dice += "- Read A Situation (ras): Roll + Brains\n"
                dice += "- Read Another's Thoughts (rat): Roll + Brains\n"
                dice += "- Sense What's Beyond (swb): Roll + Beyond\n"
                dice += "- Help Or Hinder (hoh): Roll + Bonds\n"

            elif bits[1] not in moves:
                dice += 'Please specify a Move (or "!move ?" for help)'

            elif bits[1] in moves:
                roll = [random.randint(1,6), random.randint(1,6)]
                if bits[1] == "aup":
                    options = aup
                if bits[1] == "ia":
                    options = ia
                if bits[1] == "awf":
                    options = awf
                if bits[1] == "map":
                    options = map
                if bits[1] == "man":
                    options = man
                if bits[1] == "ras":
                    options = ras
                if bits[1] == "rat":
                    options = rat
                if bits[1] == "swb":
                    options = swb
                if bits[1] == "hoh":
                    options = hoh

                result = roll[0] + roll[1]
                mod = ''

                if len(bits) > 2:
                    mod = [' ',list(bits[2])[0],' ',list(bits[2])[1],' ']
                    mod = gap.join(mod)
                    if list(bits[2])[0]=="+":
                        result = result + int(list(bits[2])[1])
                    elif list(bits[2])[0]=="-":
                        result = result - int(list(bits[2])[1])

                if result < 7:
                    outcome = options[3]
                elif result > 9:
                    outcome = options[1]
                else:
                    outcome = options[2]

                dice += options[0]
                dice += "\nResult: "
                dice += str(roll[0])
                dice += " + "
                dice += str(roll[1])
                dice += mod
                dice += " = "
                dice += str(result)
                dice += "\nOutcome: "
                dice += outcome

        dice += '```'

        ## Send message to channel
        await message.channel.send(dice)

## Write login details locally (i.e., on linux box where bot code is running)
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="Alas: !move ? for help"))
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

## Run Bot on Discord server
client.run(TOKEN)
