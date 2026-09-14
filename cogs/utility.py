import discord
from discord.ext import commands
import discord.utils as utils
import urllib.parse
import time
import io
import os
import json
import string
from discord.ext import tasks
import datetime
import aiohttp
import asyncio
import re
import random


class Utility(commands.Cog, name="⚙ Utility", description="""
These commands will help you with some things. Some will help you moderate,
some help set up your server, some give you valuable information.
However, if you're looking for moderation, you definitely have better options
instead of Serpynth.
"""):
    def __init__(self, client):
        self.client = client
        #self.weather.start()
        self.deleted_messages = {}
        self.edited_messages = {}
        f = open("timezones.json", "r")
        self.tzones = json.load(f)
        f.close()


    # background tasks - weather clear
    @tasks.loop(seconds=300)
    async def weather(self):
        return
        guild = self.client.get_guild(692393060692263002)
        channel = guild.get_channel(780465799625965609)
        places = ["Ottawa", "London"]
        flags = {"Ottawa": "🇨🇦", "London": "🇬🇧"}
        msgs = [await channel.fetch_message(857327084313772033),
                await channel.fetch_message(857327358432247809),
                await channel.fetch_message(857327441601495040),
                await channel.fetch_message(857327442066145311)]
        async with aiohttp.ClientSession() as session:
            for i in range(len(places)):
                async with session.get(f"http://api.openweathermap.org/data/2.5/weather?appid={os.environ['OWMKEY']}&q={places[i]}") as info:
                    info = await info.json()
                    main = info["main"]
                    weather = info["weather"][0]
                    sym = ""
                    if weather["main"] == "Thunderstorm":
                        sym = "⛈"
                    elif weather["main"] in ("Drizzle", "Rain"):
                        sym = "🌧"
                    elif weather["main"] == "Clear":
                        sym = "☀"
                    elif weather["main"] == "Snow":
                        sym = "🌨"
                    elif weather["main"] == "Clouds":
                        if weather["description"] == "few clouds":
                            sym = "🌤"
                        elif weather["description"] == "scattered clouds":
                            sym = "⛅"
                        elif weather["description"] == "broken clouds":
                            sym = "🌥"
                        else:
                            sym = "☁"
                    elif weather["main"] in ("Mist", "Haze", "Fog"):
                        sym = "🌁"
                    elif weather["main"] == "Ash":
                        sym = "🌋"
                    elif weather["main"] == "Squall":
                        sym = "💨"
                    elif weather["main"] == "Tornado":
                        sym = "🌪"
                    elif weather["main"] in ("Sand", "Dust"):
                        sym = "<:sand:780472713801760799>"
                    elif weather["main"] == "Smoke":
                        sym = "🚬"
                    else:
                        sym = "❔"
                    await msgs[i * 2].edit(content=f"""**CURRENT WEATHER IN {places[i].upper()} {flags[places[i]]}**
`{weather["description"]}`, `{round(main["temp"] - 273.15)}°C`""")
                    await msgs[i * 2 + 1].edit(content=sym)


    @weather.before_loop
    async def before_weather(self):
        await self.client.wait_until_ready()


    def cog_unload(self):
        self.weather.cancel()


    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.channel.id in self.deleted_messages:
            self.deleted_messages[message.channel.id].append([message, time.time(), len(message.embeds), len(message.attachments)])
            if len(self.deleted_messages[message.channel.id]) > 6:
                self.deleted_messages[message.channel.id].pop(0)
        else:
            self.deleted_messages[message.channel.id] = [[message, time.time(), len(message.embeds), len(message.attachments)]]


    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.channel.id in self.edited_messages:
            self.edited_messages[before.channel.id].append([before, after, time.time(), len(before.embeds), len(before.attachments)])
            if len(self.edited_messages[before.channel.id]) > 6:
                self.edited_messages[before.channel.id].pop(0)
        else:
            self.edited_messages[before.channel.id] = [[before, after, time.time(), len(before.embeds), len(before.attachments)]]


    @commands.command(aliases=["timemachine", "deletetimemachine" "tm", "dtm"], help="snipes the last deleted message in your server")
    async def snipe(self, ctx):

        if ctx.channel.id in self.deleted_messages:
            messages = self.deleted_messages[ctx.channel.id]
        else:
            embed = discord.Embed(color=random.randint(0, 16777215), title="SNIPE")
            embed.description = f"No deleted messages have been found in {ctx.channel.mention} yet."
            await ctx.send(embed=embed)
            return

        embed = discord.Embed(color=random.randint(0, 16777215), title="SNIPE")
        embed.description = f"In {ctx.channel.mention}, `{len(messages)}` deleted message{'s' if len(messages) != 1 else ''} " + \
                            f"ha{'ve' if len(messages) != 1 else 's'} been found:\n_ _"

        for message in messages:
            if message[0].content != "":
                content = ">>> " + message[0].content[:980]
                if len(message[0].content) > 980:
                    content += "..."
            else:
                content = "`no content`"
                if message[2] > 0:
                    content += f"\n`(+ {message[2]} embed{'s' if message[2] != 1 else ''})`"
                if message[3] > 0:
                    content += f"\n`(+ {message[3]} file{'s' if message[3] != 1 else ''})`"

            embed.add_field(name=f"_ _\nSent by {message[0].author} <t:{round(message[0].created_at.timestamp())}:R>:",
                            value=content, inline=False) # [Here]({message[0].jump_url})\n

        await ctx.send(embed=embed)


    @commands.command(aliases=["edittimemachine", "etm"], help="snipes the last deleted message in your server")
    async def editsnipe(self, ctx):

        if ctx.channel.id in self.edited_messages:
            messages = self.edited_messages[ctx.channel.id]
        else:
            embed = discord.Embed(color=random.randint(0, 16777215), title="EDIT SNIPE")
            embed.description = f"No edited messages have been found in {ctx.channel.mention} yet."
            await ctx.send(embed=embed)
            return

        embed = discord.Embed(color=random.randint(0, 16777215), title="EDIT SNIPE")
        embed.description = f"In {ctx.channel.mention}, `{len(messages)}` edited message{'s' if len(messages) != 1 else ''} " + \
                            f"ha{'ve' if len(messages) != 1 else 's'} been found:\n_ _"

        for message in messages:
            if message[0].content != "":
                content = ">>> " + message[0].content[:970]
                if len(message[0].content) > 970:
                    content += "..."
            else:
                content = "`no content`"
                if message[3] > 0:
                    content += f"\n`(+ {message[3]} embed{'s' if message[3] != 1 else ''})`"
                if message[4] > 0:
                    content += f"\n`(+ {message[4]} file{'s' if message[4] != 1 else ''})`"

            embed.add_field(name=f"_ _\nEdited by {message[0].author} <t:{round(message[2])}:R>:",
                            value=f"[Current message]({message[1].jump_url})", inline=False)
            embed.add_field(name="Original:",
                            value=content, inline=False)

        await ctx.send(embed=embed)


    @commands.command(aliases=["die", "rolldice", "rolldie"], help="gives you a random number from 1 to 6")
    async def dice(self, ctx, amount=6):
        await ctx.send(f"You rolled a `{random.randint(1, amount)}`!")


    @commands.command(aliases=["coin", "cf", "cointoss"], help="flips a coin")
    async def coinflip(self, ctx):
        coin = random.randint(1, 600001)
        if coin == 600001:
            await ctx.send("You won't believe this, but it landed on the side. 🪙")
        elif coin <= 300000:
            await ctx.send("You got heads! 🪙")
        else:
            await ctx.send("You got tails! 🪙")


    @commands.command(help="bans a member from your server")
    @commands.has_permissions(ban_members=True)
    @commands.is_owner()
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        if (ctx.author.id == 597852310764519434) or (ctx.author.top_role > member.top_role):
            await member.ban(reason=reason)
            await ctx.send(f"Sucessfully banned `{member}`.")
        else:
            await ctx.send(f"You can't ban `{member}`; they have a higher rank than you!")
    

    @commands.command(aliases=["banhammer"])
    @commands.is_owner()
    async def ban(self, ctx, *, member: discord.Member):
        await ctx.guild.ban(member)
        await ctx.send(f"Successfully banned `{member}`.")


    @commands.command(aliases=["pardon"], help="unbans a member from your server")
    @commands.has_permissions(ban_members=True)
    @commands.is_owner()
    async def unban(self, ctx, *, id):
        user = await self.client.fetch_user(int(id))
        await ctx.guild.unban(user)
        await ctx.send(f"Successfully unbanned `{user}`.")


    @commands.command(aliases=["purge", "delete"], help="deletes a specified number of messages")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=1):
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"Deleted `{'{:,}'.format(amount)}` messages.", delete_after=2.0)


    @commands.command(aliases=["gstart", "gw", "gaw"], help="starts a giveaway (note: Serpynth is not the best option for giveaways)")
    async def giveaway(self, ctx, minutes, * , prize):
        embed = discord.Embed(title="GIVEAWAY", description=f'Prize: {prize}', color = random.randint(0, 16777215))
        end = datetime.datetime.utcnow() + datetime.timedelta(seconds=float(minutes) * 60.0)
        embed.add_field(name="Ends At", value=f"{end.year}-{end.month}-{end.day} at {end.hour-4}:{end.minute} EST")
        embed.set_footer(text=f"Ends {minutes} minutes from now!")
        msg = await ctx.send(embed=embed)
        await msg.add_reaction('🎉')
        await asyncio.sleep(float(minutes) * 60.0)

        getmsg = await ctx.channel.fetch_message(msg.id)
        users = await getmsg.reactions[0].users().flatten()
        users.pop(users.index(self.client.user))
        if len(users) != 0:
            winner = random.choice(users)
            await ctx.send(f"**GIVEAWAY END**\n{winner.mention} won **{prize}**!\n{msg.jump_url}")
        else:
            await ctx.send(f"**GIVEAWAY END**\nNobody entered the giveaway.")


    @commands.command(aliases=["bye", "goodbye"], help="makes Serpynth leave your server")
    @commands.has_permissions(manage_guild=True)
    async def leaveserver(self, ctx):
        await ctx.send("Are you sure you want to remove me from your server? (yes/no)")
        def check(m):
            return m.content.lower() in ("yes", "no") and m.channel == ctx.message.channel and m.author == ctx.message.author
        try:
            msg = await self.client.wait_for("message", timeout=15.0, check=check)
        except asyncio.TimeoutError:
            pass
        else:
            if msg.content.lower() == "yes":
                await ctx.send("Okay then. Goodbye!")
                await ctx.guild.leave()
            else:
                await ctx.send("Okay then, I'll stay.")


    @commands.command(aliases=["boot", "roundhouse"], help="kicks a member from the server")
    @commands.is_owner()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, victim: discord.Member, *, reason=None):
        if ctx.guild.id != 849352438812377128:
            if (ctx.author.id == 597852310764519434) or (ctx.author.top_role > victim.top_role):
                await victim.kick(reason=reason)
                await ctx.send(f"Sucessfully kicked `{victim}`.")
            else:
                await ctx.send(f"You can't kick `{victim}`; they have a higher role than you!")

        else:
            await victim.kick(reason=reason)

            f = json.load(open("kicks.json", "r"))
            if str(ctx.author.id) not in f:
                f[str(ctx.author.id)] = [0, 0, 0]
            if ctx.author.id != victim.id:
                f[str(ctx.author.id)][0] += 1
                f[str(ctx.author.id)][2] += 1
            if f[str(ctx.author.id)][0] > f[str(ctx.author.id)][1]:
                f[str(ctx.author.id)][1] = f[str(ctx.author.id)][0]

            json.dump(f, open("kicks.json", "w"))

            await ctx.send(f"You've kicked {victim}. You now have a score of `{f[str(ctx.author.id)][0]}`")


    @commands.command(aliases=["points"], help="how many points in King of the Hill do you have?")
    async def score(self, ctx, member: discord.Member = None):
        if member == None:
            member = str(ctx.author.id)
        else:
            member = str(member.id)

        f = json.load(open("kicks.json", "r"))
        if member == str(ctx.author.id):
            if member not in f:
                await ctx.send("You haven't kicked anyone in King of the Hill yet!\nJoin the server https://discord.gg/hTDCvP28hZ")
            else:
                await ctx.send(f"Your current score: `{f[member][0]}`\nYour best score: `{f[member][1]}`") #\nTotal score: `{f[member][2]}
        else:
            if member not in f:
                await ctx.send(f"They haven't kicked anyone in King of the Hill yet!\nJoin the server https://discord.gg/hTDCvP28hZ")
            else:
                await ctx.send(f"Their current score: `{f[member][0]}`\nTheir best score: `{f[member][1]}`") #\nTotal score: `{f[member][2]}


    @commands.command(aliases=["nickname"], help="nicknames someone in the server")
    @commands.has_permissions(manage_nicknames=True)
    async def nick(self, ctx, member: discord.Member, *, nick):
        await member.edit(nick=nick)
        await ctx.send(f"Changed {member}'s nickname to {nick}")


    @commands.command(aliases=["ui"], help="gives information about a member")
    async def userinfo(self, ctx, *, user: discord.Member = None):
        if user == None:
            user = ctx.message.author
        if user.activity != None:
            activity = []
            activity += str(user.activity.type)
            for foobar in range(13):
                activity.pop(0)
            if "".join(activity) == "custom":
                for foobar in range(6):
                    activity.pop(0)
            activity = "".join(activity)
        embed = discord.Embed(title=f"{user}'s Profile", color=user.color)
        embed.add_field(name="Server Nickname", value=user.display_name)
        embed.add_field(name="Mention", value=user.mention)
        embed.add_field(name="Is bot?", value=str(user.bot))
        embed.add_field(name="Status", value=str(user.status))
        embed.add_field(name="Connected to Voice?", value=str(user.voice != None))
        try:
            embed.add_field(name="Activity", value=f"{activity} {user.activity.name}")
        except:
            embed.add_field(name="Activity", value="None")
        embed.add_field(name="Top role", value=user.top_role.mention)
        embed.set_image(url=user.avatar_url)
        await ctx.send(embed=embed)


    @commands.command(aliases=["giverole", "gr"], help="gives someone a role")
    @commands.has_permissions(manage_roles=True)
    async def role(self, ctx, member: discord.Member, role: discord.Role):
        if 597852310764519434 in (ctx.author.id, member.id):
            await member.add_roles(role)
            await ctx.send(f"Gave {member.name} role: {role.name}")
        elif (ctx.author.top_role > role):
            await member.add_roles(role)
            await ctx.send(f"Gave {member.name} role: {role.name}")
        else:
            await ctx.send(f"You can't add this role to `{member}`; the role is higher than yours!")


    @commands.command(aliases=["remindme", "alarm"], help="starts a timer")
    async def timer(self, ctx, time, *, reason="None"):
        tl = []
        tl += time
        if tl[len(tl) - 1].lower() in ("s", "m", "h"):
            inc = tl[len(tl) - 1].lower()
            tl.pop(len(tl) - 1)
            tl = "".join(tl)
            if inc == "s":
                val = float(tl)
            elif inc == "m":
                val = float(tl) * 60
            elif inc == "h":
                val = float(tl) * 3600
            msg = await ctx.send(f"Starting timer for `{float(tl)}{inc}`")
            await asyncio.sleep(val)

            await msg.reply(content=f"{ctx.message.author.mention}, your timer is up!\n{ctx.message.jump_url}\n{reason if reason != 'None' else ''}")

        else:
            await ctx.send("Serpynth only supports time in seconds (s), minutes (m) or hours (h).")


    @commands.command(aliases=["weather", "temperature", "temp"], help="gets weather info on a city/place")
    @commands.cooldown(60, 60, commands.BucketType.user)
    async def weatherinfo(self, ctx, *, location):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"http://api.openweathermap.org/data/2.5/weather?appid={os.environ['OWMKEY']}&q={location}") as info:
                info = await info.json()
                if info["cod"] == 200:
                    main = info["main"]
                    weather = info["weather"][0]
                    await ctx.send(f"""```apache
City: {location}
Country: {info["sys"]["country"]}
Temperature: {round(main["temp"] - 273.15)}°C
Feels: {round(main["feels_like"] - 273.15)}°C
Humidity: {main["humidity"]}%
Weather: {weather["main"]}
Description: {weather["description"]}```
                """)
                else:
                    await ctx.send(f"""There was an error retrieving the weather information from `{location}`.
Make sure that `{location}` actually exists.""")


    @commands.command(aliases=["wolf", "wolframalpha", "calc", "calculate", "calculator"], help="ask wolfram")
    async def wolfram(self, ctx, *, question="wolfram"):
        if not question.lower() in ("wolfram", "site", "website"):
            async with ctx.message.channel.typing():
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"http://api.wolframalpha.com/v2/query?appid=" + \
                    f"{os.environ['WOLF-ID']}&input={urllib.parse.quote_plus(question)}&format=plaintext&output=json") as info:
                        info = await info.read()
                        info = json.loads(info)
                try:
                    answer = info["queryresult"]["pods"][1]["subpods"][0]["plaintext"]
                    query = info["queryresult"]["pods"][0]["subpods"][0]["plaintext"]
                except:
                    answer = "Results could not be retrieved from Wolfram"
                    query = question.lower()

            if answer == "":
                answer = "Results could not be retrieved from Wolfram"

            embed = discord.Embed(colour=0xff7e00)
            embed.set_author(name="WolframAlpha", url="https://www.wolframalpha.com/")
            embed.add_field(name=question, value=f"https://www.wolframalpha.com/input/?i={urllib.parse.quote_plus(question)}", inline=False)
            embed.add_field(name="Input", value=f"```mathematica\n{query}```", inline=False)
            embed.add_field(name="Output", value=f"```mathematica\n{answer}```", inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send("**Wolfram|Alpha's website:**\nhttps://www.wolframalpha.com/")


    @commands.command(aliases=["ivi", "iinfo"], help="gets info on an invite link")
    async def inviteinfo(self, ctx, invite_url):
        url = invite_url
        if url.startswith("discord.gg/") or url.startswith("https://discord.gg/") or url.startswith("http://discord.gg/"):
            url = await self.client.fetch_invite(url, with_counts=True)
            await ctx.send(f"""```prolog
MEMBERS: {"{:,}".format(url.approximate_member_count)}
ONLINE MEMBERS: {"{:,}".format(url.approximate_presence_count)}
INVITE CREATED BY: {url.inviter if url.inviter != None else "?"}
ID: {url.code}
```""")
        else:
            await ctx.send("This is not a valid invite link.")


    @commands.command(aliases=["tz", "timezone", "tzc", "tzconvert", "timezones"], help="converts timezones")
    async def timezoneconvert(self, ctx, tz1, tz2="UTC"):
        tz1 = tz1.upper()
        tz2 = tz2.upper()
        numicons = {0: "1️⃣", 1: "2️⃣", 2: "3️⃣"}
        revicons = {"1️⃣": 0, "2️⃣": 1, "3️⃣": 2}
        br = "\n"

        if tz1 == tz2:
            await ctx.send(f"Those are the exact same timezones, there is no need to convert between them.")
            return

        if tz1 not in self.tzones["times"]:
            await ctx.send(f"`{tz1}` is not a valid time zone!")
            return
        if tz2 not in self.tzones["times"]:
            await ctx.send(f"`{tz2}` is not a valid time zone!")
            return

        async def checkmulti(tz):
            if type(self.tzones["times"][tz]) == list:
                ask = await ctx.send(f"""`{tz}` can mean {len(self.tzones["times"][tz])} different timezones.
Which one do you want?

{br.join([numicons[i] + ": `" + j + "`" for i, j in enumerate(self.tzones["names"][tz])])}""")
                for i, j in enumerate(self.tzones["names"][tz]):
                    await ask.add_reaction(numicons[i])

                specify = []

                def check(reaction, user):
                    if reaction.emoji in [numicons[i] for i, j in enumerate(self.tzones["names"][tz])]:
                        if user == ctx.author and reaction.message == ask:
                            return True
                        else:
                            return False
                    else:
                        return False

                try:
                    reaction, user = await self.client.wait_for("reaction_add", check=check, timeout=120.0)
                except asyncio.TimeoutError:
                    await ask.clear_reactions()
                    return
                else:
                    global tz1time
                    global tz1name
                    global tz2time
                    global tz2name
                    if tz == tz1:
                        tz1time = self.tzones["times"][tz1][revicons[reaction.emoji]]
                        tz1name = self.tzones["names"][tz1][revicons[reaction.emoji]]
                    else:
                        tz2time = self.tzones["times"][tz2][revicons[reaction.emoji]]
                        tz2name = self.tzones["names"][tz2][revicons[reaction.emoji]]
            else:
                if tz == tz1:
                    tz1time = self.tzones["times"][tz1]
                    tz1name = self.tzones["names"][tz1]
                else:
                    tz2time = self.tzones["times"][tz2]
                    tz2name = self.tzones["names"][tz2]

        await checkmulti(tz1)
        await checkmulti(tz2)

        utctime = ("0" if len(str(datetime.datetime.utcnow().hour)) < 2 else "") + str(datetime.datetime.utcnow().hour) + ":" + \
                    ("0" if len(str(datetime.datetime.utcnow().minute)) < 2 else "") + str(datetime.datetime.utcnow().minute)

        embed = discord.Embed(colour=0xf1c40f)
        embed.set_author(name=f"{tz1} ⬄ {tz2}", icon_url="https://images.emojiterra.com/twitter/v13.0/512px/2600.png")
        embed.add_field(name=tz1, value=f"{tz1name}\n`{abs(tz1time)}h` {'behind' if tz1time < 0 else 'ahead of'} UTC")
        embed.add_field(name=tz2, value=f"{tz2name}\n`{abs(tz2time)}h` {'behind' if tz2time < 0 else 'ahead of'} UTC")
        embed.set_footer(text=f"Current time in UTC: {utctime}")
        await ctx.send(embed=embed)


    @commands.command(aliases=["rule"], help="tries to find the rules channel")
    async def rules(self, ctx):
        channel = ctx.guild.rules_channel
        if not channel:
            for c in ctx.guild.text_channels:
                if "rule" in c.name:
                    channel = c
                    break

        if channel:
            await ctx.send(f"Rules channel: {channel.mention}")
        else:
            await ctx.send("No rules channel found.")


    @commands.command(aliases=["nothing", "invisible", "blank", "whitespace", "invis"], help="ways to send an empty message in Discord")
    async def empty(self, ctx):
        embed = discord.Embed(colour=0x2f3136)
        embed.set_author(name="A GUIDE TO NOTHING", url="http://www.e-try.com/black.htm")
        embed.description = """You may copy-paste the characters and character sequences by double-clicking or
triple-clicking, or just type them if your keyboard has them.
Keep in mind that you may be able to see the characters, depending on your OS."""
        embed.add_field(name="Space", value="""` `
The space won't actually allow you to send an empty message. It's still a classic though.""")
        embed.add_field(name="Empty Italics", value="""`_ _`
Normally, two underscores can be used to create indented text, but here they can be used to send just a space.""")
        embed.add_field(name="Empty Bold", value="""`** **`
Works similarly to the empty italics.""")
        embed.add_field(name="0-Width Space (U+200B)", value="""`​`
Truly empty. Doesn't even have any width.""")
        embed.add_field(name="Right-To-Left Mark (U+200F)", value="""`‏`
Like the 0-Width Space, it almost has no width.""")
        embed.add_field(name="Braille Pattern Blank (U+2800)", value="""`⠀`
The blank braille pattern.""")
        embed.add_field(name="Soft Hyphen (U+00AD)", value="""`­`
Can be used to tell a computer to break a work across lines.""")
        embed.add_field(name="Arabic Letter Mark (U+061C)", value="""`؜`
Works in strange ways.""")
        embed.add_field(name="Hangul Jungseong Filler (U+1160)", value="""`ᅠ`
The widest invisible character here.""")
        embed.add_field(name="Combining Grapheme Joiner (U+034F)", value="""`͏`
Also 0-width.""")
        embed.add_field(name="<reserved> (U+1CBC)", value="""`᲼`
Can be used to get yourself an invisible nickname/server name.""")
        embed.add_field(name="Khmer Vowel Inherent AA (U+17B5)", value="""`឵`
Can be used to get yourself a zero-width nickname/server name.""")
        embed.add_field(name="Transparent Images", value="""`https://upload.wikimedia.org/wikipedia/commons/c/ca/1x1.png`
Is actually a 1x1 transparent image.""")
        embed.add_field(name="Transparent Emojis", value="""<:__:1028468329456865310>
You can upload empty transparent emojis to your servers. You won\'t be able to copy-paste this one.""")
        embed.add_field(name="Bots", value="""With the Manage
Messages permissions, you
can make a bot send
an embed and by clicking the X
near the top right corner of
the embed, you can
actually remove it.""")
        embed.set_footer(text="More at https://invisible-characters.com/")
        await ctx.send(embed=embed)


    @commands.command(aliases=["text", "txt", "file", "ttf"], help="inserts text into a file")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def texttofile(self, ctx, filename, *, text: str):
        if "." not in filename:
            filename += ".txt"
        await ctx.send(file=discord.File(io.StringIO(text), filename=filename))


    @commands.command(aliases=["tr", "react", "reaction"], help="adds/removes a reaction to a message")
    @commands.has_permissions(add_reactions=True)
    async def togglereaction(self, ctx, message, emoji):
        if message.startswith("https://discord.com/channels/"):
            message = message.split("/")[6]
        try:
            msg = await ctx.channel.fetch_message(message)
        except:
            msg = None

        if msg == None:
            if ctx.message.reference != None:
                msg = await ctx.channel.fetch_message(ctx.message.reference.message_id)
            else:
                await ctx.send("Message ID not found.")
                return

        for r in msg.reactions:
            if r.me and r.emoji == emoji:
                await msg.remove_reaction(emoji, self.client.user)
                await ctx.message.add_reaction("✅")
                return
        await msg.add_reaction(emoji)
        await ctx.message.add_reaction("✅")



    @commands.command(aliases=["createmoji", "emoji", "emj"], help="creates an emoji to your server")
    @commands.has_permissions(manage_emojis=True)
    async def createemoji(self, ctx, name=None, allowed_roles: discord.ext.commands.Greedy[discord.Member] = None):
        if len(ctx.message.attachments) < 1:
            await ctx.send("Make sure to attach an image on the command, so I can upload it.")
            return
        elif not ctx.message.attachments[0].content_type.startswith("image"):
            await ctx.send("Make sure to attach an image on the command with the correct file type.")
            return
        elif ctx.message.attachments[0].size > 255999:
            await ctx.send("This image is too large! Make sure the file size is less than 256kb.")
            return
        elif type(name) == str:
            if len(name) < 2:
                await ctx.send("The name must be at least 2 characters long.")
                return

        img = ctx.message.attachments[0]
        if name == None:
            name = img.filename
            name = "".join(name.split(".")[:-1])

        try:
            emj = await ctx.guild.create_custom_emoji(name=name, image=await img.read(), roles=allowed_roles)
        except discord.HTTPException:
            await ctx.send(f"The emoji's name `{name}` is not valid.")
            return

        await ctx.send("Created emoji:")
        if emj.animated:
            await ctx.send(f"<a:{emj.name}:{emj.id}>")
        else:
            await ctx.send(f"<:{emj.name}:{emj.id}>")


    @commands.command(aliases=["rmd", "emd", "remove markdown"], help="removes markdown, for example **hello** becomes \*\*hello**")
    async def escapemarkdown(self, ctx, message=""):
        if message.startswith("https://discord.com/channels/"):
            message = message.split('/')[6]
        try:
            msg = await ctx.channel.fetch_message(message)
        except:
            msg = None

        if msg == None:
            if ctx.message.reference != None:
                msg = await ctx.channel.fetch_message(ctx.message.reference.message_id)
            else:
                await ctx.send("Message ID not found.")
                return

        await ctx.send(f"{discord.utils.escape_markdown(msg.content)}")


    @commands.command(name="embed", aliases=["summonembed", "mbed"], help="create a Discord embed")
    @commands.cooldown(1, 10, type=commands.BucketType.channel)
    @commands.has_permissions(manage_webhooks=True)
    async def createembed(self, ctx):
        embed = discord.Embed()
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        await ctx.send("""**Let's create an embed!**
At any point you can type "cancel" to cancel creation or "none" to leave a section blank.

1: What will your embed's colour be? (e.g., #7289DA, #E74C3C, #2ECC71)""")

        try:
            m = await self.client.wait_for("message", check=check, timeout=300.0)
        except asyncio.TimeoutError:
            await ctx.send("Embed creation cancelled due to 5 minute timeout")
            return
        else:
            if m.content.lower() == "cancel":
                await ctx.send("Embed creation cancelled manually")
                return
            elif m.content.lower() == "none":
                embed.colour = 0x2F3136
            else:
                c = m.content.lower().replace("#", "")
                if len(c) != 6:
                    await ctx.send("Embed creation cancelled due to invalid input - not a hex code")
                    return
                for i in c:
                    if i not in "0123456789abcdef":
                        await ctx.send("Embed creation cancelled due to invalid input - not a hex code")
                        return
                embed.colour = int(c, 16)

        await ctx.send("What will your embed's title be? (Max. 256 characters)")
        try:
            m = await self.client.wait_for("message", check=check, timeout=300.0)
        except asyncio.TimeoutError:
            await ctx.send("Embed creation cancelled due to 5 minute timeout")
            return
        else:
            if m.content.lower() == "cancel":
                await ctx.send("Embed creation cancelled manually")
                return
            elif m.content.lower() != "none":
                if len(m.content) > 256:
                    await ctx.send("Embed creation cancelled due to invalid input - title too long")
                    return
                else:
                    embed.title = m.content

        try:
            await ctx.send("What will your embed's author be? (Max. 256 characters)", embed=embed)
        except:
            await ctx.send("What will your embed's author be? (Max. 256 characters)")
        try:
            m = await self.client.wait_for("message", check=check, timeout=300.0)
        except asyncio.TimeoutError:
            await ctx.send("Embed creation cancelled due to 5 minute timeout")
            return
        else:
            if m.content.lower() == "cancel":
                await ctx.send("Embed creation cancelled manually")
                return
            elif m.content.lower() != "none":
                if len(m.content) > 256:
                    await ctx.send("Embed creation cancelled due to invalid input - author too long")
                    return
                else:
                    embed.set_author(name=m.content)



async def setup(client):
    await client.add_cog(Utility(client))
