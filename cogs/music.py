import discord
from discord.ext import commands
from discord.utils import get
import time
import aiohttp
import random
# import youtube_dl
import yt_dlp as youtube_dl
import os
import asyncio
import re
# import pyaudio
import array
import pydub
from pydub import AudioSegment


class Music(commands.Cog, name="🎶 Music", description="""
Most of these commands play music in a voice channel! Make Serpynth join your
voice channel with `syjoin`, find a song using `syytsearch`
(which is in a different category), copy its url and put it into `syplay`,
and stop it using `systop`.
Includes a few audio manipulation commands!
"""):
    def __init__(self, client):
        # youtube_dl.utils.bug_reports_message = lambda: ""
        self.players = {}
        self.client = client
        self.discs = {"13": "<:13:1028416985563926598>",
                "cat": "<:cat_:1028416987573014539>",
                "blocks": "<:blocks:1028416986482487336>",
                "chirp": "<:chirp:1028416989397524540>",
                "far": "<:far:1028416991503061123>",
                "mall": "<:mall:1028416992568410223>",
                "mellohi": "<:mellohi:1028416994585886781>",
                "stal": "<:stal:1028416997853253702>",
                "strad": "<:strad:1028416999136698458>",
                "ward": "<:ward:1028417001661661234>",
                "11": "<:11:1028417003691716699>",
                "wait": "<:wait:1028417000105594941>",
                "pigstep": "<:pigstep:1028416996775305346>",
                "otherside": "<:otherside:1028416995777052732>",
                "5": "<:5_:1028417002630565938>",
                "medlegia": "<:medlegia:1028416993650540575>",
                "ducks": "<:ducks:1028416990563532870>",
                "relic": "<:relic:1101894589532610570>"}


    @commands.command(aliases=["pl"], help="plays music in a voice channel")
    async def play(self, ctx, *, url: str = ""):

        ydl_opts = {"format": "bestaudio/best", "quiet": "True",
            "postprocessors": [{"key": "FFmpegExtractAudio","preferredcodec": "mp3","preferredquality": "192"}]}
        voice = get(self.client.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            await voice.move_to(ctx.message.author.voice.channel)
        else:
            try:
                voice = await ctx.message.author.voice.channel.connect()
            except:
                voice = get(self.client.voice_clients, guild=ctx.guild)

        if ctx.message.author.voice != None:
            if not voice.is_paused():

                def checkvalid(link):
                    if link.startswith("https://youtu"):
                        return True
                    elif link.startswith("http://youtu"):
                        return True
                    elif link.startswith("http://www.youtu"):
                        return True
                    elif link.startswith("https://www.youtu"):
                        return True
                    elif link.startswith("https://open.spotify.com/track/"):
                        return True
                    elif len(link) < 1:
                        return False
                    else:
                        return False

                if not checkvalid(url):
                    searchquery = []
                    searchquery += url
                    item = 0
                    for char in searchquery:
                        if char == " ":
                            searchquery.pop(item)
                            searchquery.insert(item, "+")
                        item += 1
                    searchquery = "".join(searchquery)

                    async with aiohttp.ClientSession() as session:
                        htmcontent = await session.get(f"http://www.youtube.com/results?search_query={searchquery}")
                        htmcontent = await htmcontent.read()
                    results = re.findall(r"/watch\?v=(.{11})", str(htmcontent)) # List
                    if results != []:
                        url = results[0]
                    else:
                        await ctx.send(f"No results found. Try a different URL or a different search.")
                        return

                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    data = info["formats"]
                    title = info.get("title", None)
                    duration = info.get("duration", None)
                    views = info.get("view_count", None)
                
                for form in data[::-1]:
                    if form.get("audio_channels") == 2:
                        stream = form["url"]
                        break

                msg = await ctx.send("Preparing audio...")
                voice.play(discord.FFmpegPCMAudio(stream,
                        before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 0"))
                durstr = f"{duration // 60}:"
                if len(f"{duration - ((duration // 60) * 60)}") == 1:
                    durstr += "0"
                durstr += f"{duration - ((duration // 60) * 60)}"
                views = "{:,}".format(views)

                embed = discord.Embed(colour=0x9b59b6)
                embed.set_author(name="MUSIC TIME")
                embed.add_field(name=title, value=f"Length: `{durstr}`\nViews: `{views}`")
                embed.set_footer(text="From YouTube")

                await msg.edit(content=f"Ready! Now playing audio {random.choice(('💿', '🎶', '🎵', '🎧', '🎻', '🎺', '🎸'))}",
                                embed=embed)
            else:
                voice.resume()
                await ctx.send("Audio resumed\nIf you want to play something different, `systop` the current audio first")

        else:
            await ctx.send("You are not connected to a voice channel!")


    @commands.command(aliases=["connect"], help="makes Serpynth join your voice channel")
    async def join(self, ctx):
        if ctx.author.voice != None:
            try:
                ctx.voice_client.cleanup()
            except:
                pass
            channel = ctx.author.voice.channel
            msg = await ctx.send("Connecting...")
            start = time.time()
            voice = get(self.client.voice_clients, guild=ctx.guild)
            if voice and voice.is_connected():
                await voice.move_to(channel)
            else:
                voice = await channel.connect(self_deaf=False)
            try:
                voice.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source="Connect.mp3"))
            except discord.ClientException:
                pass
            await msg.edit(content=f"Successfully joined channel: `{ctx.author.voice.channel.name}`\n" + \
                                        f"Connection time: `{round((time.time() - start) * 1000)}ms`")
        else:
            await ctx.send("You are not connected to a voice channel!")


    @commands.command(aliases=["disconnect"], help="disconnects bot from voice channel")
    async def leave(self, ctx):
        voice = get(self.client.voice_clients, guild=ctx.guild)
        await ctx.voice_client.disconnect()
        try:
            ctx.voice_client.cleanup()
        except:
            pass
        await ctx.send(f"Successfully left channel: `{voice.channel.name}`")


    @commands.command(aliases=["end", "halt"], help="stops the currently playing audio")
    async def stop(self, ctx):
        voice = get(self.client.voice_clients, guild=ctx.guild)
        if voice and voice.is_playing():
            await ctx.send("Audio stopped")
            voice.stop()
        else:
            await ctx.send("No audio currently playing.")


    @commands.command(help="pauses the currently playing audio")
    async def pause(self, ctx):
        voice = get(self.client.voice_clients, guild=ctx.guild)
        if voice and voice.is_playing():
            await ctx.send("Audio paused")
            voice.pause()
        else:
            await ctx.send("No audio currently playing.")


    @commands.command(aliases=["res", "unpause"], help="resumes the paused audio")
    async def resume(self, ctx):
        voice = get(self.client.voice_clients, guild=ctx.guild)
        await ctx.send("Audio resumed")
        voice.resume()


    @commands.command(aliases=["downloadmp3", "dlmp3", "dl3"], help="downloads the .mp3 file from a youtube video")
    @commands.cooldown(1, 5, commands.BucketType.user)
    #@commands.is_owner()
    async def mp3(self, ctx, url: str):

        ydl_opts = {"format": "bestaudio/best",
            "postprocessors": [{"key": "FFmpegExtractAudio","preferredcodec": "mp3","preferredquality": "192"}] }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get("title", None)
            duration = info.get("duration", None)
            views = info.get("view_count", None)

        if False: # if duration >= 600:
            await ctx.send("Error: Video length must be less than 10 minutes in duration")
        else:
            try:
                if os.path.isfile("audio.mp3"):
                    os.remove("audio.mp3")
            except PermissionError:
                await ctx.send("Error: Audio is being used somewhere else")
                return
            msg = await ctx.send("Retrieving audio...")
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            for file in os.listdir("./"):
                if file.endswith(".mp3"):
                    os.rename(file, "audio.mp3")
            await msg.edit(content=f"Ready! Now uploading .mp3 file from `{title}`")

            durstr = f"{duration // 60}:"
            if len(f"{duration - ((duration // 60) * 60)}") == 1:
                durstr += "0"
            durstr += f"{duration - ((duration // 60) * 60)}"
            views = "{:,}".format(views)

            await ctx.send(file=discord.File("audio.mp3", filename=f"{title}.mp3"))


    @commands.command(aliases=["downloadmp4", "dlmp4", "dl4"], help="downloads the .mp4 file from a youtube video")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.is_owner()
    async def mp4(self, ctx, url: str):

        ydl_opts = {"format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best",
            "postprocessors": [{"preferedformat": "mp4", "key": "FFmpegVideoConvertor"}] }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get("title", None)
            duration = info.get("duration", None)
            views = info.get("view_count", None)

        if False: # if duration >= 300:
            await ctx.send("Error: Video length must be less than 5 minutes in duration")
        else:
            try:
                if os.path.isfile("video.mp4"):
                    os.remove("video.mp4")
            except PermissionError:
                await ctx.send("Error: Video is being used somewhere else")
                return
            msg = await ctx.send("Retrieving video...")
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            for file in os.listdir("./"):
                if file.endswith(".mp4"):
                    os.rename(file, "video.mp4")
            await msg.edit(content=f"Ready! Now uploading .mp4 file from `{title}`")

            durstr = f"{duration // 60}:"
            if len(f"{duration - ((duration // 60) * 60)}") == 1:
                durstr += "0"
            durstr += f"{duration - ((duration // 60) * 60)}"
            views = "{:,}".format(views)

            await ctx.send(file=discord.File("video.mp4", filename=f"{title}.mp4"))


    @commands.command(aliases=["maketune", "comp"], help="compose in a voice channel")
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def compose(self, ctx):
        try:
            channel = ctx.author.voice.channel
            voice = get(self.client.voice_clients, guild=ctx.guild)
            if voice and voice.is_connected():
                await voice.move_to(channel)
            else:
                voice = await channel.connect(self_deaf=True)
        except:
            await ctx.send("There was an error while connecting to your voice channel.")
            return

        malpha = ["A", "B", "C", "D", "E", "F", "G"]
        pat = []
        msg = await ctx.send(f"""
- Add notes by sending the note (`A`, `B`, `C`, `D`, `E`, `F`, `G`)
    followed by its accidentals (`o`, `#`, `b` where `o` is a natural) and then its octave (0-8). (For example: `Co4`, `D#2`, `Ab5`)
- Put in a rest (break) by saying `rest` or `r`
- Delete the last note by saying `delete` or `d` and clear everything by saying `clear` or `c` (Note: There is no confirmation when using `clear`)
- Play your composition by saying `play` or `p`
- End by saying `end` or `e`
```fix\n{" ".join(pat)} ```""")

        def check(m):
            if m.channel == ctx.message.channel and m.author == ctx.message.author:
                if len(m.content) == 3 and m.content.lower() != "end":
                    if m.content in ("Ab0", "C#8", "C♯8", "A♭0"):
                        return False
                    else:
                        f = lambda a: str(a)
                        if m.content[0] in malpha and m.content[1] in ("o", "♮", "#", "♯", "b", "♭"):
                            if m.content[2] in tuple(map(f, tuple(range(0, 9)))):
                                if m.content[2] == "0":
                                    if m.content[0] in ("A", "B"):
                                        return True
                                    else:
                                        return False
                                elif m.content[2] == "8":
                                    if m.content[0] == "C":
                                        return True
                                    else:
                                        return False
                                else:
                                    return True
                            else:
                                return False
                        else:
                            return False
                else:
                    if m.content.lower() in ("d", "delete"):
                        return True
                    elif m.content.lower() in ("c", "clear"):
                        return True
                    elif m.content.lower() in ("p", "play"):
                        return True
                    elif m.content.lower() in ("e", "end"):
                        return True
                    elif m.content.lower() in ("r", "𝄽", "rest"):
                        return True
                    else:
                        return False
            else:
                return False

        while True:
            try:
                m = await self.client.wait_for("message", check=check, timeout=120.0)
            except asyncio.TimeoutError:
                await ctx.send("Composition session ended automatically due to 2-minute timeout")
                break
            else:
                if m.content.lower() in ("d", "delete"):
                    try:
                        pat.pop(len(pat) - 1)
                    except IndexError:
                        pass
                elif m.content.lower() in ("c", "clear"):
                    pat.clear()
                elif m.content.lower() in ("p", "play"):
                    voice = get(self.client.voice_clients, guild=ctx.guild)
                    for n in pat:
                        note = n
                        if note != "𝄽":
                            if note[1] == "♭":
                                if note[0] in ("C", "F"):
                                    note = note.replace(note[0], malpha[malpha.index(note[0]) - 1])
                                    note = note.replace("♭", "♮")
                                    if note[0] == "B":
                                        note = note.replace(note[2], str(int(note[2]) - 1))
                                else:
                                    note = note.replace(note[0], malpha[malpha.index(note[0]) - 1])
                                    note = note.replace("♭", "♯")
                            elif note[1] == "♯":
                                if note[0] in ("B", "E"):
                                    note = note.replace(note[0], malpha[malpha.index(note[0]) + 1])
                                    note = note.replace("♯", "♮")
                                    if note[0] == "C":
                                        note = note.replace(note[2], str(int(note[2]) + 1))

                        voice.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source=f"88notes/{note}.mp3"))
                        await asyncio.sleep(1)
                        voice.stop()
                elif m.content.lower() in ("e", "end"):
                    await ctx.send("Composition session ended manually")
                    break
                elif m.content.lower() in ("r", "𝄽", "rest"):
                    pat.append("𝄽")
                else:
                    pat.append(m.content.replace("o", "♮").replace("#", "♯").replace("b", "♭"))

                await m.delete()
                await msg.edit(content=f"""
- Add notes by sending the note (`A`, `B`, `C`, `D`, `E`, `F`, `G`)
    followed by its accidentals (`o`, `#`, `b` where `o` is a natural) and then its octave (0-8). (For example: `Co4`, `D#2`, `Ab5`)
- Put in a rest (break) by saying `rest` or `r`
- Delete the last note by saying `delete` or `d` and clear everything by saying `clear` or `c` (Note: There is no confirmation when using `clear`)
- Play your composition by saying `play` or `p`
- End by saying `end` or `e`
```fix\n{" ".join(pat)} ```""")


    @commands.command(aliases=["disc", "juke", "discs"], help="plays a music disc\n**You may not have two copies of the same disc.**")
    async def jukebox(self, ctx, disc="inv", member: discord.Member = None):
        readdoc = open("discs.txt", "r")
        dict = eval(readdoc.read())
        readdoc.close()

        try:
            dict[ctx.message.author.id]
        except KeyError:
            dict[ctx.message.author.id] = []
        d = disc.lower()
        if d == "eleven":
            d = "11"
        elif d == "thirteen":
            d = "13"
        elif d == "five":
            d = "5"
        if d in dict[ctx.message.author.id]:
            if ctx.author.voice != None:
                channel = ctx.author.voice.channel
                voice = get(self.client.voice_clients, guild=ctx.guild)
                if voice and voice.is_connected():
                    await voice.move_to(channel)
                else:
                    voice = await channel.connect(self_deaf=True)
                voice.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=f"{d}.mp3"))
                await ctx.send(f"Now playing: `{d}`")
                await ctx.send(self.discs[d])
            else:
                await ctx.send("You are not connected to a voice channel!")
        elif d in ("inv", "inventory", "discs"):
            inv = ""
            if member == None:
                user = ctx.message.author
            else:
                user = member
            try:
                for item in dict[user.id]:
                    foo = []
                    foo += item
                    foo[0] = foo[0].upper()
                    foo = "".join(foo)
                    inv += f"\n{foo} {self.discs[item]}"
                if inv == "":
                    inv = f"\n{user.mention} does not have any discs yet!"
            except KeyError:
                inv = f"\n{user.mention} does not have any discs yet!"
            await ctx.send(f"**{user.mention}'s music disc inventory:** {inv}")
        else:
            await ctx.send("You do not own this disc!")


    @commands.command(aliases=["summondisc", "gd", "awarddisc"], help="gives someone a music disc (does not trade)")
    @commands.is_owner()
    async def grantdisc(self, ctx, member: discord.Member, disc):
        d = disc.lower()
        if d == "eleven":
            d = "11"
        elif d == "thirteen":
            d = "13"
        elif d == "five":
            d = "5"

        readdoc = open("discs.txt", "r")
        dict = eval(readdoc.read())
        readdoc.close()
        try:
            dict[member.id]
        except KeyError:
            dict[member.id] = []

        dict[member.id].append(d)
        writedoc = open("discs.txt", "w")
        writedoc.write(str(dict))
        writedoc.close()
        await ctx.send(f"Gave {member} the disc: `{disc}` {self.discs[d]}")


    @commands.command(aliases=["trade", "disctrade" "discexchange", "exchangedisc"], help="trades music discs with someone else")
    @commands.is_owner()
    async def tradedisc(self, ctx, member: discord.Member):
        readdoc = open("discs.txt", "r")
        dict = eval(readdoc.read())
        readdoc.close()
        p1 = ctx.author
        p2 = member
        try:
            dict[p2.id]
        except KeyError:
            dict[p2.id] = []

        try:
            dict[p1.id]
        except KeyError:
            dict[p1.id] = []

        p1offer = [0, "", "", "", "", "", "", ""]
        p2offer = [0, "", "", "", "", "", "", ""]

        trading = f"""
|{" " * (32 - len(p1.name))}{p1.name}|{p2.name}{" " * (32 - len(p2.name))}|
|{" " * (32 - len(p1offer[1]))}{p1offer[1]}|{p2offer[1]}{" " * (32 - len(p2offer[1]))}|
|{" " * (32 - len(p1offer[2]))}{p1offer[2]}|{p2offer[2]}{" " * (32 - len(p2offer[2]))}|
|{" " * (32 - len(p1offer[3]))}{p1offer[3]}|{p2offer[3]}{" " * (32 - len(p2offer[3]))}|
|{" " * (32 - len(p1offer[4]))}{p1offer[4]}|{p2offer[4]}{" " * (32 - len(p2offer[4]))}|
|{" " * (32 - len(p1offer[5]))}{p1offer[5]}|{p2offer[5]}{" " * (32 - len(p2offer[5]))}|
|{" " * (32 - len(p1offer[6]))}{p1offer[6]}|{p2offer[6]}{" " * (32 - len(p2offer[6]))}|
|{" " * (32 - len(p1offer[7]))}{p1offer[7]}|{p2offer[7]}{" " * (32 - len(p2offer[7]))}|
|---------------------|
|${p1offer[0]}{" " * (32 - len(str(p1offer[0])))}|${p2offer[0]}{" " * (32 - len(str(p2offer[0])))}|
"""


    @commands.command(aliases=["lys", "songlyric", "lyric"])
    @commands.is_owner()
    @commands.cooldown(2, 1, commands.BucketType.user)
    async def lyrics(self, ctx, *, song):
        """ Finds the lyrics to a song.\n(this command does not work at the moment) """

        async with ctx.channel.typing():
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"https://some-random-api.ml/lyrics?title={song}") as info:
                        info = await info.json()

                length = len(info["lyrics"])
                if length < 2048:
                    lys = info["lyrics"]
                else:
                    lys = info["lyrics"][:2047]

                embed = discord.Embed(colour=random.randint(0, 16777215))
                embed.set_author(name=f"{info['title']} by {info['author']}")
                embed.description = lys
                if len(lys) > 2046:
                    embed.add_field(name="_ _", value="...")
                embed.set_footer(text="https://some-random-api.ml/")
                await ctx.send(embed=embed)
            except:
                await ctx.send("An error occured; this API, after all, isn't very good.")


    @commands.command(aliases=["telephonegame", "chinesewhispers"], help="telephone game in a voice channel")
    @commands.is_owner()
    @commands.has_permissions(manage_channels=True)
    async def telephone(self, ctx):
        if ctx.author.voice != None:
            channel = ctx.author.voice.channel
            voice = get(self.client.voice_clients, guild=ctx.guild)
            if voice and voice.is_connected():
                await voice.move_to(channel)
            else:
                voice = await channel.connect(self_deaf=True)
        else:
            await ctx.send("You are not connected to a voice channel!")
            return

        embed = discord.Embed(color=random.randint(1, 16777215))
        embed.set_author(name="HOW TO PLAY")
        embed.description = """
        When the game starts, everyone will be deafened and muted.
        The first person in the voice channel will be unmuted, and the second
        will be undeafened. The first person shall say some phrase, and once
        the second person hears it, they should react to this message with 👍.
        The first person will be muted, the second will be unmuted and deafened,
        the third will be undeafened, and the second should say what they
        heard from the first person. Repeat until the last person hears from
        the second last person, and everyone will be undeafened. They will
        say what they heard. Then, the game ends.
        """

        m = await ctx.send(f"Join `{voice.channel.name}` if you want to play!\n"
                            f"The host ({ctx.author.mention}) can start the game by reacting with ✅.",
                            embed=embed)
        await m.add_reaction("✅")
        await m.add_reaction("👍")

        def checkr(reaction, user):
            return reaction.message == m and reaction.emoji == "✅" and user == ctx.author

        try:
            await self.client.wait_for("reaction_add", check=checkr, timeout=600.0)
        except asyncio.TimeoutError:
            await m.reply(content="You didn't start the game in time.", mention_author=False)
            return

        await ctx.send("Starting!")
        members = []
        for member in voice.channel.members:
            if member.id != 743131027786170509:
                members.append(member)
                await member.edit(mute=True, deafen=True)


    @commands.command(aliases=["searchyt", "youtube", "yt"], help="searches for something on YouTube")
    async def ytsearch(self, ctx, *, search="https://www.youtube.com/"):
        searchquery = []
        searchquery += search
        item = 0
        for char in searchquery:
            if char == " ":
                searchquery.pop(item)
                searchquery.insert(item, "+")
            item += 1
        searchquery = "".join(searchquery)

        async with aiohttp.ClientSession() as session:
            htmcontent = await session.get(f"http://www.youtube.com/results?search_query={searchquery}")
            htmcontent = await htmcontent.read()
        results = re.findall(r"/watch\?v=(.{11})", str(htmcontent)) # List
        if results != []:
            msg = await ctx.send(f"""**Result #1:** https://youtu.be/{results[0]}
**Search query:** https://www.youtube.com/results?search_query={searchquery}""")
        else:
            await ctx.send(f"No results found.\nSee for yourself: https://www.youtube.com/results?search_query={searchquery}")
            return

        await msg.add_reaction("⏪")
        await msg.add_reaction("◀")
        await msg.add_reaction("⏹")
        await msg.add_reaction("▶")
        await msg.add_reaction("⏩")
        await msg.add_reaction("🎶")

        def check(reaction, user):
                return str(reaction.emoji) in ("⏪", "◀", "⏹", "▶", "⏩", "🎶") and reaction.message == msg and user == ctx.message.author

        page = 1
        while True:
            msg = await ctx.channel.fetch_message(msg.id)
            try:
                reaction, user = await self.client.wait_for("reaction_add", timeout=60.0, check=check)
            except asyncio.TimeoutError:
                await msg.clear_reactions()
                break
            if str(reaction.emoji) == "⏪":
                page = 1
            elif str(reaction.emoji) == "◀":
                if page == 1:
                    page = len(results)
                else:
                    page -= 1
            elif str(reaction.emoji) == "⏹":
                await msg.clear_reactions()
                break
            elif str(reaction.emoji) == "▶":
                if page == len(results):
                    page = 1
                else:
                    page += 1
            elif str(reaction.emoji) == "⏩":
                page = len(results)
            elif str(reaction.emoji) == "🎶":
                voice = get(self.client.voice_clients, guild=ctx.guild)
                if voice and voice.is_playing():
                    voice.stop()
                await ctx.invoke(self.play, url=f"https://youtu.be/{results[page - 1]}")

            await reaction.remove(user)
            await msg.edit(content=f"""**Result #{page}:** https://youtu.be/{results[page - 1]}
**Search query:** https://www.youtube.com/results?search_query={searchquery}""")


    @commands.command(aliases=["keys", "keyboard"], help="Play the piano!")
    async def piano(self, ctx):
        if ctx.author.voice != None:
            channel = ctx.author.voice.channel
            voice = get(self.client.voice_clients, guild=ctx.guild)
            if voice and voice.is_connected():
                await voice.move_to(channel)
            else:
                voice = await channel.connect(self_deaf=True)
        else:
            await ctx.send("You are not connected to a voice channel!")
            return

        view = discord.ui.View()
        keys = [discord.ui.Button(label="C", style=discord.ButtonStyle.grey)]

        for key in keys:
            async def callback(interaction):
                voice.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source=f"88notes/C4.mp3"))
                await asyncio.sleep(1)
                voice.stop()
                await interaction.response.send_message(f"🎵", ephemeral=True)
            
            key.callback = callback
            view.add_item(item=key)
        
        await ctx.send(view=view)
    

    @commands.command(aliases=["reducefilesize"])
    async def compress(self, ctx):
        """ Magically reduces the filesize of an .mp3 file. """

        if len(ctx.message.attachments) < 1:
            await ctx.send("You need to attach a .mp3 file onto the command!")
            return
        elif ctx.message.attachments[0].content_type != "audio/mpeg":
            await ctx.send("The file must be a .mp3 file!")
            return
        else:
            filename = ctx.message.attachments[0].filename
            message = await ctx.send("Processing audio...")

        with open("audio.mp3", "wb") as f:
            f.write(await ctx.message.attachments[0].read())
        
        audio = AudioSegment.from_mp3("audio.mp3")
        audio.export("audio.mp3", format="mp3")
        await ctx.send(file=discord.File("audio.mp3", filename=filename))
        await message.edit(content="Done!")
    

    @commands.command(aliases=["earrape"])
    async def louden(self, ctx, decibels="100"):
        """ Increases the volume of an .mp3 file (in decibels). """

        if len(ctx.message.attachments) < 1:
            await ctx.send("You need to attach a .mp3 file onto the command!")
            return
        elif ctx.message.attachments[0].content_type != "audio/mpeg":
            await ctx.send("The file must be a .mp3 file!")
            return
        elif not decibels.isdigit():
            await ctx.send("Please input a valid number of decibels.")
            return
        else:
            filename = ctx.message.attachments[0].filename
            message = await ctx.send("Processing audio...")

        with open("audio.mp3", "wb") as f:
            f.write(await ctx.message.attachments[0].read())
        
        audio = AudioSegment.from_mp3("audio.mp3")
        audio += float(decibels)

        audio.export("audio.mp3", format="mp3")
        await ctx.send(file=discord.File("audio.mp3", filename=f"{filename[:-4].upper()}.mp3"))
        await message.edit(content="Done!")
    

    @commands.command(aliases=["invertaudio", "reverseaudio"])
    async def reverse(self, ctx):
        """ Inverts an .mp3 file. """

        if len(ctx.message.attachments) < 1:
            await ctx.send("You need to attach a .mp3 file onto the command!")
            return
        elif ctx.message.attachments[0].content_type != "audio/mpeg":
            await ctx.send("The file must be a .mp3 file!")
            return
        else:
            filename = ctx.message.attachments[0].filename
            message = await ctx.send("Processing audio...")

        with open("audio.mp3", "wb") as f:
            f.write(await ctx.message.attachments[0].read())
        
        audio = AudioSegment.from_mp3("audio.mp3")
        audio = audio.reverse()

        audio.export("audio.mp3", format="mp3")
        await ctx.send(file=discord.File("audio.mp3", filename=f"{filename[:-4][::-1]}.mp3"))
        await message.edit(content="Done!")
    

    @commands.command(aliases=["changebitrate", "bitrate"])
    async def bitcrush(self, ctx, bitrate="25"):
        """ Changes the bitrate of a .mp3 audio to a percentage of the original bitrate. """

        if len(ctx.message.attachments) < 1:
            await ctx.send("You need to attach a .mp3 file onto the command!")
            return
        elif ctx.message.attachments[0].content_type != "audio/mpeg":
            await ctx.send("The file must be a .mp3 file!")
            return
        else:
            filename = ctx.message.attachments[0].filename
            message = await ctx.send("Processing audio...")

        with open("audio.mp3", "wb") as f:
            f.write(await ctx.message.attachments[0].read())
        
        audio = AudioSegment.from_mp3("audio.mp3")
        audio = audio.set_frame_rate(int(audio.frame_rate * float(bitrate.replace("%", "")) / 100))

        audio.export("audio.mp3", format="mp3")
        await ctx.send(file=discord.File("audio.mp3", filename=f"{filename[:-4].lower()}.mp3"))
        await message.edit(content="Done!")
    

    @commands.command(aliases=["increasespeed"])
    @commands.is_owner()
    async def quicken(self, ctx, factor="1.5"):
        """ Increases the speed of an .mp3 audio file by some factor. """

        if len(ctx.message.attachments) < 1:
            await ctx.send("You need to attach a .mp3 file onto the command!")
            return
        elif ctx.message.attachments[0].content_type != "audio/mpeg":
            await ctx.send("The file must be a .mp3 file!")
            return
        else:
            filename = ctx.message.attachments[0].filename
            message = await ctx.send("Processing audio...")

        with open("audio.mp3", "wb") as f:
            f.write(await ctx.message.attachments[0].read())
        
        audio = AudioSegment.from_mp3("audio.mp3")
        samples = audio.get_array_of_samples()

        if audio.channels == 2:
            samples = [samples[::2], samples[1::2]]
        else:
            samples = [samples]
        
        newsamples = []
        toggle = 0
        for i, sample in enumerate(samples[0]):
            toggle += (float(factor) - 1) / float(factor)
            if toggle < 1:
                newsamples.append(samples[0][i])
                newsamples.append(samples[1][i])
            else:
                toggle -= 1

        audio = audio._spawn(array.array(audio.array_type, newsamples))
        audio.export("audio.mp3", format="mp3")
        await ctx.send(file=discord.File("audio.mp3", filename=f"{filename[:-4]}.mp3".replace('_', '')))
        await message.edit(content="Done!")
    

    @commands.command(aliases=["decreasespeed"])
    @commands.is_owner()
    async def slowen(self, ctx, factor="1.5"):
        """ Decreases the speed of an .mp3 audio file by some factor. """

        if len(ctx.message.attachments) < 1:
            await ctx.send("You need to attach a .mp3 file onto the command!")
            return
        elif ctx.message.attachments[0].content_type != "audio/mpeg":
            await ctx.send("The file must be a .mp3 file!")
            return
        else:
            filename = ctx.message.attachments[0].filename
            message = await ctx.send("Processing audio...")

        with open("audio.mp3", "wb") as f:
            f.write(await ctx.message.attachments[0].read())
        
        audio = AudioSegment.from_mp3("audio.mp3")
        samples = audio.get_array_of_samples()

        if audio.channels == 2:
            samples = [samples[::2], samples[1::2]]
        else:
            samples = [samples]
        
        newsamples = []
        toggle = 0
        for i, sample in enumerate(samples[0]):
            toggle += (float(factor) - 1) / float(factor)
            newsamples.append(samples[0][i])
            newsamples.append(samples[1][i])
            while toggle >= 1:
                newsamples.append(samples[0][i])
                newsamples.append(samples[1][i])
                toggle -= 1
                toggle += (float(factor) - 1) / float(factor)

        audio = audio._spawn(array.array(audio.array_type, newsamples))
        audio.export("audio.mp3", format="mp3")
        await ctx.send(file=discord.File("audio.mp3", filename=f"{filename[:-4]}.mp3".replace('_', '__')))
        await message.edit(content="Done!")
    

    @commands.command(aliases=["scratchy", "crackle", "crunch"])
    @commands.is_owner()
    async def scratch(self, ctx):
        """ Creates a harsh, scratchy effect on an .mp3 file by randomly deleting samples. """

        if len(ctx.message.attachments) < 1:
            await ctx.send("You need to attach a .mp3 file onto the command!")
            return
        elif ctx.message.attachments[0].content_type != "audio/mpeg":
            await ctx.send("The file must be a .mp3 file!")
            return
        else:
            filename = ctx.message.attachments[0].filename
            message = await ctx.send("Processing audio...")

        with open("audio.mp3", "wb") as f:
            f.write(await ctx.message.attachments[0].read())
        
        audio = AudioSegment.from_mp3("audio.mp3")
        samples = audio.get_array_of_samples()

        if audio.channels == 2:
            samples = [samples[::2], samples[1::2]]
        else:
            samples = [samples]
        
        newsamples = []
        for i, sample in enumerate(samples[0]):
            if random.random() < 0.5:
                newsamples.append(samples[0][i])
                newsamples.append(samples[1][i])
                newsamples.append(samples[0][i])
                newsamples.append(samples[1][i])

        audio = audio._spawn(array.array(audio.array_type, newsamples))
        audio.export("audio.mp3", format="mp3")
        await ctx.send(file=discord.File("audio.mp3", filename=f"{filename[:-4]}.mp3"))
        await message.edit(content="Done!")


async def setup(client):
    await client.add_cog(Music(client))
