import discord
import asyncio
from discord.ext import tasks
from discord.ext import commands
from itertools import cycle
import datetime
import colored
import aiohttp
import random
import dotenv
import time
import json
import sys
import os
dotenv.load_dotenv(".env.txt")
intents = discord.Intents.default()
intents.bans = True
intents.presences = True
intents.members = True
intents.message_content = True


class Client(commands.Bot):
    max_messages = 1000
    was_typing = {}

    async def greet(self, person):
        return f"Hello, {person}!"
    
    async def setup_hook(self):
        pass

    async def current_time(self):
        now = datetime.datetime.now()
        if now.hour < 12:
            period = "AM"
        else:
            period = "PM"
        hour = now.hour % 12
        if hour == 0:
            hour = 12

        minute = now.minute
        if minute < 10:
            minute = f"0{minute}"

        second = now.second
        if second < 10:
            second = f"0{second}"
        
        return f"{hour}:{minute}:{second} {period}"

client = Client(command_prefix=commands.when_mentioned_or("sy", "SY", "Sy", "Hey Serpynth, "),
                        max_messages=Client.max_messages,
                        status=discord.Status.invisible,
                        activity=discord.Activity(type=discord.ActivityType.watching,
                                                name="you 👀 | syhelp"),
                        strip_after_prefix=True,
                        intents=intents,
                        owner_id=597852310764519434)

client.remove_command("help")
status = cycle([discord.Status.online, discord.Status.dnd, discord.Status.idle])


@client.check
def in_dms(ctx):
    return ctx.channel.type != discord.ChannelType.private


@tasks.loop(seconds=0.3)
async def rainbowstatus():
    await client.change_presence(status=next(status),
                                activity=discord.Activity(type=discord.ActivityType.watching,
                                                        name="you 👀 | syhelp"))


@client.event
async def on_connect():
    now = datetime.datetime.now()
    if now.hour < 12:
        period = "AM"
    else:
        period = "PM"
    hour = now.hour % 12
    if hour == 0:
        hour = 12

    minute = now.minute
    if minute < 10:
        minute = f"0{minute}"

    second = now.second
    if second < 10:
        second = f"0{second}"

    print(f"[{hour}:{minute}:{second} {period}]  \x1b[33;1mConnected to Discord\x1b[0m")


@client.event
async def on_ready():
    now = datetime.datetime.now()
    if now.hour < 12:
        period = "AM"
    else:
        period = "PM"
    hour = now.hour % 12
    if hour == 0:
        hour = 12

    minute = now.minute
    if minute < 10:
        minute = f"0{minute}"

    second = now.second
    if second < 10:
        second = f"0{second}"

    print(f"[{hour}:{minute}:{second} {period}]  \x1b[32;1m{client.user} is ready\x1b[0m")

    #await client.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.watching, name="you 👀 | syhelp"))
    #rainbowstatus.start()


@client.event
async def on_disconnect():
    now = datetime.datetime.now()
    if now.hour < 12:
        period = "AM"
    else:
        period = "PM"
    hour = now.hour % 12
    if hour == 0:
        hour = 12

    minute = now.minute
    if minute < 10:
        minute = f"0{minute}"

    second = now.second
    if second < 10:
        second = f"0{second}"

    print(f"[{hour}:{minute}:{second} {period}]  \x1b[31;1mDisconnected from Discord\x1b[0m")


@client.event
async def on_resumed():
    now = datetime.datetime.now()
    if now.hour < 12:
        period = "AM"
    else:
        period = "PM"
    hour = now.hour % 12
    if hour == 0:
        hour = 12

    minute = now.minute
    if minute < 10:
        minute = f"0{minute}"

    second = now.second
    if second < 10:
        second = f"0{second}"

    print(f"[{hour}:{minute}:{second} {period}]  \x1b[33;1mReconnected to Discord\x1b[0m")


@client.event
async def on_message(message):

    if message.channel.type == discord.ChannelType.private:
        content = message.content.lower().replace("very", "").replace("so", "").replace("much", "")
        content = content.replace("serpynth", "").replace("s", "").replace("u", "")
        content = content.replace(" ", "").replace(",", "").replace("!", "")
        if content in ("ty", "thx", "thank", "thankyo"):
            await message.channel.send(random.choice(["No problem!", "You're welcome!", "My pleasure!"]))

    elif message.content.lower() == "hey serpynth, what are your pronouns?":
        await message.channel.send("They/them. Or he/him. Or she/her. Or it/its. I literally do not care")
    
    elif True: #message.guild.id != 887052880782176266:
        await client.process_commands(message)


@client.event
async def on_presence_update(before, after):
    if after.guild.id == 0:
        if before.status != after.status:
            statuses = ["online", "offline", "idle", "dnd"]
            emjstat = ["<:online:1028413805039976478>",
                "<:offline:1028413801487409203>",
                "<:idle:1028413800124252180>",
                "<:dnd:1028413796236136591>"]

            log = client.get_channel(0)
            embed = discord.Embed(colour=after.colour)
            embed.description = f"""{after.mention} has changed status
From {emjstat[statuses.index(before.raw_status)]} to {emjstat[statuses.index(after.raw_status)]}"""
            await log.send(embed=embed)


@client.event
async def on_typing(channel, user, when):
    if channel.guild.id == 0:
        if user.id not in client.was_typing:
            log = client.get_channel(0)
            embed = discord.Embed(colour=user.colour)
            embed.description = f"{user.mention} is typing in {channel.mention}"
            await log.send(embed=embed)
            client.was_typing[user.id] = [time.time(), channel.id]

        if (time.time() - client.was_typing[user.id][0] > 60.0):
            log = client.get_channel(0)
            embed = discord.Embed(colour=user.colour)
            embed.description = f"{user.mention} is typing in {channel.mention}"
            await log.send(embed=embed)
            client.was_typing[user.id] = [time.time(), channel.id]


@client.event
async def on_raw_reaction_add(payload):
    if payload.guild_id == 0:
        log = client.get_channel(0)
        embed = discord.Embed(colour=payload.member.colour)
        embed.description = (f"{payload.member.mention} added a reaction to a message in <#{payload.channel_id}>\n" +
                             f"Added {payload.emoji} to [this message]" +
                             f"(https://discord.com/channels/{payload.guild_id}/{payload.channel_id}/{payload.message_id} '{payload.emoji}')")
        await log.send(embed=embed)


@client.event
async def on_member_join(member):
    if member.guild.id == 849352438812377128:
        f = json.load(open("kicks.json", "r"))
        if str(member.id) in f:
            f[str(member.id)][0] = 0

        json.dump(f, open("kicks.json", "w"))


@client.event
async def on_member_remove(member):
    if member.guild.id == 849352438812377128:
        f = json.load(open("kicks.json", "r"))
        if str(member.id) in f:
            f[str(member.id)][0] = 0

        json.dump(f, open("kicks.json", "w"))
    

# Start bot
EXTENSIONS = ("help", "fun", "utility", "images", "chill", "music", "arena", "other", "debug")


@client.command(aliases=[])
@commands.is_owner()
async def load(ctx, *, extension):
    """ Loads an extension. """

    if extension.lower() == "all":
        send = ""
        for i in EXTENSIONS:
            try:
                await client.load_extension("cogs." + i)
            except Exception as e:
                send += f"\n`{e}`"
            else:
                send += f"\nSuccessfully loaded `{i}` extension."
        await ctx.send(send)

    else:
        send = f"Successfully loaded `{extension}` extension."
        try:
            await client.load_extension("cogs." + extension.lower())
        except Exception as e:
            send = f"`{e}`"
        await ctx.send(send)


@client.command(aliases=["rl"])
@commands.is_owner()
async def reload(ctx, *, extension):
    """ Unloads an extension, then loads it again. """

    if extension.lower() == "all":
        send = ""
        for i in EXTENSIONS:
            try:
                try:
                    await client.unload_extension("cogs." + i)
                except:
                    pass
                await client.load_extension("cogs." + i)
            except Exception as e:
                send += f"\n`{e}`"
            else:
                send += f"\nSuccessfully reloaded `{i}` extension."
        await ctx.send(send)

    else:
        send = f"Successfully reloaded `{extension}` extension."
        try:
            try:
                await client.unload_extension("cogs." + extension.lower())
            except:
                pass
            await client.load_extension("cogs." + extension.lower())
        except Exception as e:
            send = f"`{e}`"
        await ctx.send(send)


@client.command(aliases=["ul"])
@commands.is_owner()
async def unload(ctx, *, extension):
    """ Unloads an extension. """

    if extension.lower() == "all":
        send = ""
        for i in EXTENSIONS:
            try:
                await client.unload_extension("cogs." + i)
            except Exception as e:
                send += f"\n`{e}`"
            else:
                send += f"\nSuccessfully unloaded `{i}` extension."
        await ctx.send(send)

    else:
        send = f"Successfully unloaded `{extension}` extension."
        try:
            await client.unload_extension("cogs." + extension.lower())
        except Exception as e:
            send = f"`{e}`"
        await ctx.send(send)


async def main():
    async with client:
        for i in EXTENSIONS:
            await client.load_extension("cogs." + i)

        await client.load_extension("jishaku")
        await client.start(os.environ["TOKEN"], reconnect=True)

asyncio.run(main())
