## PROFESSOR TURO BOT

import re, os, asyncio, random, string, time
from discord.ext import commands, tasks
from pathlib import Path
import json
from json import loads

version = 'v1.2'

## Defining the server and bot token
config = loads(Path("config.json").read_text())

user_token = config["user_token"]
spam_id = config["spam_id"]
spawns_1 = config["spawns_1"]
spawns_2 = config["spawns_2"]
spawns_3 = config["spawns_3"]
spawns_4 = config["spawns_4"]
spawns_5 = config["spawns_5"]
test_p2 = config["test_p2"]
timeout_secs = 6.0


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

async def handle_spawn_message(channel_id, content):
    channel = client.get_channel(channel_id)
    if 'Rare Ping' in content:
        print(f'Rare ping in {channel.name}!')
        await channel.send(f'?lock <#{channel_id}>')
    elif 'Shiny Hunt Pings' in content and "@" in content:
        print(f'Shiny Hunt detected in {channel.name}!')

        # wait for 5 seconds for someone else to send a message
        try:
            await client.wait_for('message', timeout=timeout_secs, check=lambda m: m.channel == channel and m.author != client.user)
            print("Interrupted, not shiny locking!")
        except asyncio.TimeoutError:
            future_timestamp = int(time.time()) + 3600
            await channel.send('?shlock',delete_after=timeout_secs)
            await channel.send("ShLocked! Will be unlocked automatically <t:" + (f"{future_timestamp}") + ":R> (unless someone unlocks manually, of course!)")


@client.event
async def on_message(message):
    if message.author.id == pokename:
        if message.channel.id == int(spawns_1):
            await handle_spawn_message(int(spawns_1), message.content)
        elif message.channel.id == int(spawns_2):
            await handle_spawn_message(int(spawns_2), message.content)
        elif message.channel.id == int(spawns_3):
            await handle_spawn_message(int(spawns_3), message.content)
        elif message.channel.id == int(spawns_4):
            await handle_spawn_message(int(spawns_4), message.content)
        elif message.channel.id == int(spawns_5):
            await handle_spawn_message(int(spawns_5), message.content)
        elif message.channel.id == int(test_p2):
            await handle_spawn_message(int(test_p2), message.content)

asyncio.run(client.run(f"{user_token}"))
