### Professor Turo bot
### Created by evad3r

import re, os, asyncio, random, string
from discord.ext import commands, tasks
from pathlib import Path
import json
from json import loads

version = 'v1.0'

## Defining the server and bot token
config = loads(Path("config.json").read_text())

user_token = config["user_token"]
spam_id = config["spam_id"]
spawns_1 = config["spawns_1"]
spawns_2 = config["spawns_2"]
spawns_3 = config["spawns_3"]
spawns_4 = config["spawns_4"]
spawns_5 = config["spawns_5"]
incense = config["incense"]
test_p2 = config["test_p2"]


pokename = 874910942490677270
client = commands.Bot(command_prefix= '&' )

## Spammer
intervals = [3.0, 2.2, 2.4, 2.6, 2.8]

@tasks.loop(seconds=random.choice(intervals))
async def spam():
    channel = client.get_channel(int(spam_id))
    await channel.send(''.join(random.sample(['1','2','3','4','5','6','7','8','9','0'],7)*5))

@spam.before_loop
async def before_spam():
    await client.wait_until_ready()

@client.event
async def on_ready():
    global spam
    print(f'Logged into account: {client.user.name}')
    spam.start()

## Look for Pokename shiny hunt
### Spawns 1
@client.event
async def on_message(message):
    if message.channel.id == int(spawns_1):
        channel = client.get_channel(int(spawns_1))
        if message.author.id == pokename:
            if 'Rare Ping' in message.content:
                print('Rare ping in spawns-1!')
                channel = client.get_channel(int(spawns_1))
                await channel.send('?lock '(int(spawns_1)))
            elif 'Shiny Hunt Pings' in message.content:
                print('Shiny Hunt detected in spawns-1!')
                channel = client.get_channel(int(spawns_1))
                await channel.send('?shlock')
            
    if message.channel.id == int(spawns_2):
        channel = client.get_channel(int(spawns_2))
        if 'Rare Ping' in message.content:
                print('Rare ping in spawns-2!')
                channel = client.get_channel(int(spawns_2))
                await channel.send('?lock '(int(spawns_2)))
        elif message.author.id == pokename:
            if 'Shiny Hunt Pings' in message.content:
                print('Shiny Hunt detected in spawns 2!')
                channel = client.get_channel(int(spawns_2))
                await channel.send('?shlock')
        
    if message.channel.id == int(spawns_3):
        channel = client.get_channel(int(spawns_3))
        if message.author.id == pokename:
            if 'Rare Ping' in message.content:
                print('Rare ping in spawns-3!')
                channel = client.get_channel(int(spawns_3))
                await channel.send('?lock '(int(spawns_3)))
            elif 'Shiny Hunt Pings' in message.content:
                print('Shiny Hunt detected in spawns 3!')
                channel = client.get_channel(int(spawns_3))
                await channel.send('?shlock')
            
    if message.channel.id == int(spawns_4):
        channel = client.get_channel(int(spawns_4))
        if message.author.id == pokename:
            if 'Rare Ping' in message.content:
                print('Rare ping in spawns-4!')
                channel = client.get_channel(int(spawns_4))
                await channel.send('?lock '(int(spawns_4)))
            elif 'Shiny Hunt Pings' in message.content:
                print('Shiny Hunt detected in spawns 4!')
                channel = client.get_channel(int(spawns_4))
                await channel.send('?shlock')
            
    if message.channel.id == int(spawns_5):
        if message.author.id == pokename:
            if 'Rare Ping' in message.content:
                print('Rare ping in spawns-5!')
                channel = client.get_channel(int(spawns_5))
                await channel.send('?lock '(int(spawns_5)))
            elif 'Shiny Hunt Pings' in message.content:
                print('Shiny Hunt detected in spawns 5!')
                channel = client.get_channel(int(spawns_5))
                await channel.send('?shlock')
            
    if message.channel.id == int(incense):
        if message.author.id == pokename:
            if 'Rare Ping' in message.content:
                print('Rare ping in incense!')
            elif 'Shiny Hunt Pings' in message.content:
                print('Shiny Hunt detected in incense!')

    if message.channel.id == int(test_p2):
        if message.author.id == pokename:
            if 'Rare Ping' in message.content:
                print('Rare ping in test-p2!')
                channel = client.get_channel(int(test_p2))
                await channel.send(f'?lock <#{test_p2}>')
            elif 'Shiny Hunt Pings' in message.content:
                print('Shiny Hunt detected in spawns 5!')
                channel = client.get_channel(int(test_p2))
                await channel.send('?shlock')

print(f'Pokétwo Autocatcher {version}\nA free and open-source Pokétwo autocatcher Modified by Viwes Bot\nEvent Log:')
asyncio.run(client.run(f"{user_token}"))