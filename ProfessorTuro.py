import asyncio
import json
import random
import string
import time
from pathlib import Path

from discord.ext import commands, tasks

version = 'v1.2'

config = json.loads(Path("config.json").read_text())

user_token = config["user_token"]
spam_id = config["spam_id"]
spawns_1 = config["spawns_1"]
spawns_2 = config["spawns_2"]
spawns_3 = config["spawns_3"]
spawns_4 = config["spawns_4"]
spawns_5 = config["spawns_5"]
test_p2 = config["test_p2"]
timeout_secs = 12.0

pokename = 874910942490677270
client = commands.Bot(command_prefix='&')

# List to store opted-in user IDs
opted_in_users = config.get("opted_in_users", [])

# Spammer
intervals = [3.0, 2.2, 2.4, 2.6, 2.8]


@tasks.loop(seconds=random.choice(intervals))
async def spam():
    channel = client.get_channel(int(spam_id))
    message = ''.join(random.sample(['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'], 7) * 5)
    try:
        await channel.send(message)
        print(f'Sent message ' + message)
    except Exception as e:
        print("Something went wrong while sending the message:", str(e))


@spam.before_loop
async def before_spam():
    print(f'Awaiting until client is ready before spamming...')
    await client.wait_until_ready()


@client.event
async def on_ready():
    global spam
    print(f'Logged into account: {client.user.name}')
    spam.start()


# Look for Pokename shiny hunt
async def handle_spawn_message(channel_id, message):
    channel = client.get_channel(channel_id)
    if 'Rare Ping' in message.content:
        print(f'Rare ping in {channel.name}!')
        await channel.send(f'?lock <#{channel_id}>')
    elif 'Shiny Hunt Pings' in message.content and "@" in message.content:
        print(f'Shiny Hunt detected in {channel.name}!')

        # Check if any opted-in user is mentioned
        opted_in_mentioned = any(user.id in opted_in_users for user in message.mentions)
        if opted_in_mentioned:
            try:
                await client.wait_for('message', timeout=timeout_secs,
                                      check=lambda m: m.channel == channel and m.author != client.user)
                print("Interrupted, not shiny locking!")
            except asyncio.TimeoutError:
                future_timestamp = int(time.time()) + 3600
                await channel.send('?shlock', delete_after=timeout_secs)
                await channel.send(
                    f"ShLocked! Will be unlocked automatically <t:{future_timestamp}:R> (unless someone unlocks manually, of course!)")
        else:
            print("All mentioned users are opted-out, skipping locking.")
            await channel.send("All mentioned users are opted-out, skipping locking!")



@client.event
async def on_message(message):
    if client.user.mentioned_in(message):
        if "optout" in message.content:
            await optout(message)
        elif "optin" in message.content:
            await optin(message)
    elif message.author.id == pokename:
        if message.channel.id == int(spawns_1):
            await handle_spawn_message(int(spawns_1), message)
        elif message.channel.id == int(spawns_2):
            await handle_spawn_message(int(spawns_2), message)
        elif message.channel.id == int(spawns_3):
            await handle_spawn_message(int(spawns_3), message)
        elif message.channel.id == int(spawns_4):
            await handle_spawn_message(int(spawns_4), message)
        elif message.channel.id == int(spawns_5):
            await handle_spawn_message(int(spawns_5), message)
        elif message.channel.id == int(test_p2):
            await handle_spawn_message(int(test_p2), message)


@client.command()
async def optin(ctx):
    if ctx.author.id not in opted_in_users:
        opted_in_users.append(ctx.author.id)
        await ctx.channel.send("You have opted in to have your shiny hunts locked for you.")
        # Save the updated opted_in_users list to config.json
        config["opted_in_users"] = opted_in_users
        with open("config.json", "w") as config_file:
            config_file.write(json.dumps(config, indent=4))
    else:
        await ctx.channel.send("You are already opted in.")


@client.command()
async def optout(ctx):
    if ctx.author.id in opted_in_users:
        opted_in_users.remove(ctx.author.id)
        await ctx.channel.send("You have been removed from the opt-in list.")
        # Save the updated opted_in_users list to config.json
        config["opted_in_users"] = opted_in_users
        with open("config.json", "w") as config_file:
            config_file.write(json.dumps(config, indent=4))
    else:
        await ctx.channel.send("You are not currently opted in.")


asyncio.run(client.run(f"{user_token}"))