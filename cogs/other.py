import discord
from discord import app_commands
from discord.ext import commands
from discord.utils import get
import discord.utils
import random
import numpy as np
import asyncio
import json
import string
import re
import aiohttp
from gtts import gTTS as tts
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

#dictionary
class Other(commands.Cog, name="💬 Other", description="""
This category is for commands that don't really fit anywhere else. Most of them
are hovering between **🎢 Fun** and **⚙ Utility**, but not really in either.
Many of these commands appeared very early in Serpynth's lifetime, and are quite
simple.
"""):
    def __init__(self, client):
        self.client = client


        words = open("10000words.txt")
        dict = []
        for line in words:
            for word in line.split():
                dict.append(word)
        words.close()

        words = open("6801nouns.txt")
        nouns = []
        for line in words:
            for word in line.split():
                nouns.append(word)
        words.close()


    @commands.command(aliases=["repeat", "repeatafterme"], help="echoes a message to you")
    async def say(self, ctx, *, message):
        await ctx.send(f'{" ".join(ctx.message.clean_content.split()[1:])}\n\n-{ctx.author}')


    @commands.command(aliases=["randomdict", "rw", "word"], help="gets a random english word")
    async def randomword(self, ctx):
        bookicon = random.choice(("📚", "📔", "📕", "📖", "📗", "📘", "📙", "🔖", "📑", "📜", "🔠", "🔤", "🔡", "📝", "📓", "🗒", "📒", "📔"))
        await ctx.send(f'Random word: `{random.choice(self.dict)}` {bookicon}')


    @commands.command(aliases=["rn", "noun"], help="gets a random noun")
    async def randomnoun(self, ctx):
        bookicon = random.choice(("📚", "📔", "📕", "📖", "📗", "📘", "📙", "🔖", "📑", "📜", "🔠", "🔤", "🔡", "📝", "📓", "🗒", "📒", "📔"))
        await ctx.send(f"Random noun: `{random.choice(self.nouns)}` {bookicon}")


    @commands.command(aliases=["pluralize", "plur"], help="attempts to pluralizes a word")
    async def plural(self, ctx, *, word):
        word = word.lower()
        chars = []
        chars += word.lower()

        pluralizations = {"craft": "",
                          "man": "--en",
                          "fe": "--ves",
                          "um": "--a",
                          "is": "--es",
                          "us": "--i",
                          "sh": "es",
                          "ch": "es",
                          "x": "es",
                          "z": "es",
                          "o": "es",
                          "s": "es",
                          "f": "-ves",
                          "": "s"}
        exceptions = {"child": "children", "goose": "geese", "tooth": "teeth", "foot": "feet",
                      "mouse": "mice", "person": "people", "die": "dice", "louse": "lice",
                      "ox": "oxen", "larva": "larvae", "octopus": "octopuses", "roof": "roofs",
                      "belief": "beliefs", "chef": "chefs", "chief": "chiefs", "photo": "photos",
                      "piano": "pianos", "halo": "halos", "human": "humans", "passerby": "passersby",
                      "do": "dos", "pro": "pros"}

        if word in ("sheep", "series", "species", "deer", "moose", "fish", "swine", "buffalo", "shrimp", "trout"):
            pass
        elif word in exceptions:
            word = exceptions[word]
        else:
            for key in pluralizations:
                if word.endswith(key):
                    for i in pluralizations[key]:
                        if i == "-":
                            chars.pop(-1)
                        else:
                            chars.append(i)
                    break
            word = "".join(chars)
        await ctx.send(f'Result: `{word}`')


    @commands.command(aliases=["search"], help="search for something on Google")
    async def google(self, ctx, *, query):
        await ctx.send(f"Search link: https://www.google.com/search?q={query.replace(' ', '+')}")


    @commands.command(aliases=["hello", "helloworld!"], help="`console.log(\"Hello, World!\");`")
    async def helloworld(self, ctx):
        await ctx.send("https://youtu.be/Yw6u6YkTgQ4")


    @commands.command(aliases=["nomic", "sfm", "speakforme", "nomike", "tts"], help="speaks for you if you don't have a mic")
    async def speak(self, ctx, *, msg):
        if ctx.author.voice != None:
            channel = ctx.author.voice.channel
            voice = get(self.client.voice_clients, guild=ctx.guild)
            if voice and voice.is_connected():
                await voice.move_to(channel)
            else:
                voice = await channel.connect()
            speak = tts(msg)
            speak.save("audio.mp3")
            try:
                voice.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source="audio.mp3"))
            except discord.ClientException:
                await ctx.send("Audio is currently being used somewhere in your server, please stop it before using the command")
            else:
                await ctx.send(f"Now speaking in `{channel.name}`")
        else:
            await ctx.send("You are not connected to a voice channel!")


    # Requires Chromedriver: https://chromedriver.chromium.org/
    @commands.command(aliases=["browser", "surf", "chrome", "web"], help="surf the internet, one HTML item at a time")
    @commands.is_owner()
    async def browse(self, ctx, *, site="https://html.duckduckgo.com/html"):
        try:
            async with ctx.message.channel.typing():
                set = await ctx.send("Setting up chrome...")
                opts = Options()
                opts.add_argument("--mute-audio")
                opts.headless = True
                browser = webdriver.Chrome("chromedriver.exe", options=opts)
                browser.set_window_size(1600, 1200)
                await set.edit(content="Setting up chrome...\nFinding site...")
                browser.get(site)
                await set.edit(content="Setting up chrome...\nFinding site...\nCreating UX...")

                def check(m):
                    if m.author == ctx.author and m.channel == ctx.channel:
                        if m.content.startswith("click "):
                            return True
                        if m.content.startswith("link "):
                            return True
                        elif m.content.startswith("type "):
                            return True
                        elif m.content.startswith("scroll "):
                            return True
                        elif m.content.startswith("size "):
                            return True
                        elif m.content.startswith("refresh"):
                            return True
                        elif m.content.startswith("end"):
                            return True
                        else:
                            return False
                    else:
                        return False

                def check2(m2):
                    return m2.author == ctx.author and m2.channel == ctx.channel

                browser.save_screenshot("screenshot.png")
                file = discord.File("screenshot.png", filename="screenshot.png")
                embed = discord.Embed()
                embed.set_author(name=browser.current_url, url=browser.current_url)
                embed.add_field(name="NAVIGATION CONTROLS", value="`click element`: Clicks a button by id or class" +
                    "\n`link text`: Clicks a link by its text" +
                    "\n`type element`: Type something into a text box by id or class" +
                    "\n`scroll up/down`: Scrolls either up or down" +
                    "\n`size x, y`: Sets screen size in pixels (Default: 1600, 1200)" +
                    "\n`refresh`: Refreshes the screen, updating the interface" +
                    "\n`end`: Ends the browsing session" +
                    "\n**Prefixes are not used for navigation.**")
                embed.set_image(url="attachment://screenshot.png")
                embed.set_footer(text=f"Requested by {ctx.message.author}")
                bp = await ctx.send(embed=embed, file=file)
                await set.delete()
                run = True
                while run:
                    try:
                        m = await self.client.wait_for("message", check=check, timeout=180.0)
                    except asyncio.TimeoutError:
                        await ctx.send("Browsing session ended automatically due to 3-minute timeout")
                        run = False
                        break
                    else:

                        if m.content.startswith("click "):
                            try:
                                browser.find_element_by_id(m.content.replace("click ", "")).click()
                            except exceptions.NoSuchElementException:
                                try:
                                    browser.find_element_by_class_name(m.content.replace("click ", "")).click()
                                except exceptions.NoSuchElementException:
                                    er = await ctx.send("No element found.")
                                except Exception as e:
                                    er = await ctx.send(f"Error: {e}")
                            except Exception as e:
                                er = await ctx.send(f"Error: {e}")

                        elif m.content.startswith("link "):
                            try:
                                browser.find_element_by_link_text(m.content.replace("link ", "")).click()
                            except exceptions.NoSuchElementException:
                                try:
                                    browser.find_element_by_partial_link_text(m.content.replace("link ", "")).click()
                                except exceptions.NoSuchElementException:
                                    er = await ctx.send("No element found.")
                                except Exception as e:
                                    er = await ctx.send(f"Error: {e}")
                            except Exception as e:
                                er = await ctx.send(f"Error: {e}")

                        elif m.content.startswith("type "):
                            try:
                                search = browser.find_element_by_id(m.content.replace("type ", ""))
                            except exceptions.NoSuchElementException:
                                try:
                                    search = browser.find_element_by_class_name(m.content.replace("type ", ""))
                                except exceptions.NoSuchElementException:
                                    er = await ctx.send("No element found.")
                                except Exception as e:
                                    er = await ctx.send(f"Error: {e}")
                                else:
                                    try:
                                        search.clear()
                                    except:
                                        pass
                                    q = await ctx.send("What would you like to input?")
                                    m2 = await self.client.wait_for("message", check=check2)
                                    search.send_keys(m2.content)
                                    search.submit()
                                    await m2.delete()
                                    await q.delete()
                            except Exception as e:
                                er = await ctx.send(f"Error: {e}")
                            else:
                                try:
                                    search.clear()
                                except:
                                    pass
                                q = await ctx.send("What would you like to input?")
                                m2 = await self.client.wait_for("message", check=check2)
                                search.send_keys(m2.content)
                                search.submit()
                                await m2.delete()
                                await q.delete()

                        elif m.content.startswith("scroll "):
                            html = browser.find_element_by_tag_name("html")
                            if m.content.replace("scroll ", "").replace(" ", "").lower() == "up":
                                html.send_keys(Keys.PAGE_UP)
                            else:
                                html.send_keys(Keys.PAGE_DOWN)

                        elif m.content.startswith("size "):
                            size = m.content.replace("size", "").split(",")
                            if len(size) == 2:
                                try:
                                    size[0] = int(size[0])
                                    size[1] = int(size[1])
                                except Exception as e:
                                    er = await ctx.send(f"Error: {e}")
                                else:
                                    if size[0] > 99 and size[0] < 3001 and size[1] > 99 and size[1] < 2501:
                                        browser.set_window_size(size[0], size[1])
                                    else:
                                        er = await ctx.send("Error: `x` must be between 100 and 3000 and `y` must be between 100 and 2500")
                            else:
                                er = await ctx.send("Error: Invalid arguments")

                        elif m.content.startswith("refresh"):
                            pass

                        else:
                            await ctx.send(f"You are now leaving Serpynth's Discord browser. Bye!")
                            browser.quit()
                            run = False

                        if run == True:
                            browser.save_screenshot("screenshot.png")
                            file = discord.File("screenshot.png", filename="screenshot.png")
                            embed = discord.Embed()
                            embed.set_author(name=browser.current_url, url=browser.current_url)
                            embed.add_field(name="NAVIGATION CONTROLS", value="`click element`: Clicks a button by id or class"+
                                "\n`link text`: Clicks a link by its text" +
                                "\n`type element`: Type something into a text box by id or class" +
                                "\n`scroll up/down`: Scrolls either up or down" +
                                "\n`size x, y`: Sets screen size in pixels (Default: 1600, 1200)" +
                                "\n`refresh`: Refreshes the screen, updating the interface" +
                                "\n`end`: Ends the browsing session" +
                                "\n**Prefixes are not used for navigation.**")
                            embed.set_image(url="attachment://screenshot.png")
                            embed.set_footer(text=f"Requested by {ctx.message.author}")
                            await bp.delete()
                            bp = await ctx.send(embed=embed, file=file)

                        try:
                            await er.delete()
                        except:
                            pass
                        await m.delete()

        except Exception as e:
            raise e
            try:
                browser.quit()
            except:
                pass


    @commands.command(aliases=["suggest", "suggestions", "botidea"], help="submit bot ideas for Serpynth")
    @commands.cooldown(2, 3600, commands.BucketType.user)
    async def suggestion(self, ctx, *, suggestion):
        me = await self.client.fetch_user(597852310764519434)
        def check(m):
            return m.content.lower() in ("y", "n", "yes", "no") and m.author == ctx.author and m.channel == ctx.channel

        m1 = await ctx.send("Do you want your suggestion to be anonymous? (y/n)")
        try:
            m = await self.client.wait_for("message", check=check, timeout=120.0)
        except asyncio.TimeoutError:
            pass
        else:
            if m.content.lower() in ("n", "no"):
                await me.send(f"**RECIEVED A SUGGESTION:**\n{ctx.author}: {suggestion}")
                await ctx.send("Suggestion sent.", delete_after=3.0)
            else:
                await me.send(f"**RECIEVED A SUGGESTION:**\n{suggestion}")
                await ctx.send("Suggestion sent.", delete_after=3.0)
                await m.delete()
                await ctx.message.delete()
                await m1.delete()


    @commands.command(aliases=["payrespects", "respect", "respects", "payrespect"], help="press F to pay respects")
    async def F(self, ctx, *, reason=None):
        if reason == None:
            msg = await ctx.send(f"Press 🇫 to pay respects")
        else:
            msg = await ctx.send(f"Press 🇫 to pay respects\n> {reason}")
        await msg.add_reaction("🇫")
        originalmsg = msg

        def check(reaction, user):
                return str(reaction.emoji) == "🇫" and reaction.message == msg

        while True:
            msg = await ctx.channel.fetch_message(msg.id)
            try:
                reaction, user = await self.client.wait_for("reaction_add", timeout=120.0, check=check)
            except asyncio.TimeoutError:
                break
            reactions = len(await msg.reactions[0].users().flatten())
            await msg.edit(content=originalmsg.content + f"\n`{reactions}` {'people' if reactions != 1 else 'person'} payed respects.")


    @commands.command(aliases=["mimic", "imp", "imitate", "imi"], help="testing with webhooks")
    @commands.has_permissions(manage_webhooks=True)
    async def impersonate(self, ctx, member: discord.Member, *, send=None):
        if ctx.author.id == 597852310764519434:
            await ctx.message.delete()
        hook = await ctx.channel.create_webhook(name="Mimic", reason=f"Mimic of {member}")
        await hook.send(content=send, username=member.nick if member.nick != None else member.name, avatar_url=member.display_avatar.url)
        await hook.delete(reason=f"Mimic of {member}")


    @commands.command(aliases=["borgor", "burger", "burgor"], help="🍔")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def borger(self, ctx):
        await ctx.send("⬛⬛⬛⬛⬛🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨⬛⬛⬛⬛⬛\n"
                        "⬛⬛🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨⬛⬛\n"
                        "⬛🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨⬛\n"
                        "⬛🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨⬛")
        await ctx.send("⬛⬛🟩🟩🟩🟥🟥🟥🟥🟥🟥🟥🟥🟥🟩🟩🟥🟥⬛⬛\n"
                        "⬛⬛⬛🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩⬛⬛⬛\n"
                        "⬛⬛🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫⬛⬛\n"
                        "⬛⬛🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫⬛⬛\n"
                        "⬛⬛⬛🟧🟧🟧🟧🟧🟧🟧🟧🟧🟧🟧🟧🟧🟧⬛⬛⬛")
        await ctx.send("⬛🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨⬛\n"
                        "⬛🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨⬛\n"
                        "⬛⬛🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨⬛⬛\n"
                        "⬛⬛⬛⬛⬛🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨⬛⬛⬛⬛⬛")
        if ctx.author.is_on_mobile() == True:
            await ctx.send(f"Note: If you're on mobile, you might not be able to see the full image")

    @commands.command(aliases=["crosschat", "message"], help="chatting across multiple servers!")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def chat(self, ctx, *, message=None):

        discrim = ctx.message.author.discriminator
        finalmsg = ""
        check = False
        limit = False
        chars = [' ']
        chars += string.ascii_letters
        chars += string.digits
        chars += string.punctuation
        chars.remove("`")
        namechars = []
        namechars += ctx.message.author.name
        name = ""
        for char in namechars:
            if char in chars:
                name += char
            else:
                check = True
        if message != None:
            msgchars = []
            msgchars += message
            themsg = ""
            for char in msgchars:
                if char in chars:
                    themsg += char
                else:
                    check = True
        else:
            themsg = message
        if message != None:
            if len(message) > 150:
                limit = True
    # Tags
        if ctx.message.author.id == 597852310764519434:
            discrim = f"{ctx.message.author.discriminator}(dev)"
        if ctx.message.author.id == 529011890039422976:
            discrim = f"{ctx.message.author.discriminator}(undone)"
        if ctx.message.author.id == 696811705619054633:
            discrim = f"{ctx.message.author.discriminator}(cringe)"
        if ctx.message.author.id == 556761028214390807:
            discrim = f"{ctx.message.author.discriminator}(dee)"

        readdoc = open("chat.txt", "r") # Reads file
        list = eval(readdoc.read())
        readdoc.close()
    # Sends message
        if message != None and limit == False:
            writedoc = open("chat.txt", "w") # Edits file
            list.append(f"{name}#{discrim}: {themsg}")
            writedoc.write(str(list))
            finalmsg += f"Sent message: `{message}`\n"
            writedoc.close()
    # Shows chat
        thechat = ""
        while len(list) > 15:
            list.pop(0)
        for item in list:
            thechat += f"{item}\n"
        finalmsg += f"```apache\n{thechat}```"
        if check == True and message != None and limit == False:
            finalmsg += ("Since you had invalid characters in either your message or username, they have been removed.\n"
                            "The `sychat` command only supports letters, numbers or simple punctuation.\n")
        if limit == True:
            finalmsg += "Message has not been sent: Surpassed character limit of 150"
        await ctx.send(finalmsg)


    @commands.command(aliases=["pw", "checkpassword", "password"], help="looks at a password and sees how strong it is")
    async def passwordcheck(self, ctx, *, password):
        # Password length
        sclen = len(password) / 2

        # Common words
        scwords = None
        f = open("6801nouns.txt", "r")
        nouns = f.read().split("\n")
        f.close()
        if password.lower() in nouns:
            scwords = len(password) / 3
        else:
            for n in nouns:
                if n in password.lower() and len(n) > 3:
                    if scwords == None:
                        scwords = 10 - len(n) / 2
                    else:
                        scwords = np.mean([len(n) / 3, scwords])
        if scwords == None:
            count = 0
            for i in password:
                count += 0 if i in string.digits else 1
            if count > 0:
                scwords = count

        # Numbers
        if scwords != None:
            scints = np.mean([sclen, scwords])
        else:
            scints = sclen
        enp = enumerate(password)
        lcount = 0
        for n in range(0, 10):
            for i, v in enp:
                try:
                    intv = int(v)
                except ValueError:
                    lcount += 1
                else:
                    if intv == n:
                        if len(password) != i + 1:
                            if int(password[i + 1]) in (intv, intv + 1, intv - 1):
                                chain = True
                                chtype = int(password[i + 1]) - int(password[i])

                            else:
                                chain = False
                            while chain:
                                if int(password[i + 1]) in intv + chtype:
                                    chain = True
                                    scints = np.mean([scints, scints, scints, 0])
                                else:
                                    chain = False
                                    break

            # Characters
        if scwords != None:
            scsyms = np.mean([sclen, scwords, scints])
        else:
            scsyms = np.mean([sclen, scints])
        for i in password:
            if i in string.ascii_letters:
                pass
            elif i in string.digits:
                scsyms += (scsyms + 0.1) / scsyms
            elif i in string.punctuation:
                scsyms += (scsyms + 0.5) / scsyms
            else:
                scsyms += (scsyms + 1) / scsyms

            # Finishing up
        if scwords == None:
            scwords = np.mean([scints, sclen, scsyms])
        total = round(np.mean([sclen, scwords, scints, scsyms]), 1)

        await ctx.send(f"Score: `{total}/10`")


    @commands.command(aliases=["echo"], help="try this out, it's really cool")
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def rick(self, ctx):
        message = await ctx.send("We're no strangers to love")
        await asyncio.sleep(2)
        await message.edit(content="You know the rules and so do I")
        await asyncio.sleep(3)
        await message.edit(content="A full commitment's what I'm thinking of")
        await asyncio.sleep(3)
        await message.edit(content="You wouldn't get this from any other guy")
        await asyncio.sleep(2.5)
        await message.edit(content="I just wanna tell you how I'm feeling")
        await asyncio.sleep(3)
        await message.edit(content="Gotta make you understand")
        await asyncio.sleep(2.5)
        await message.edit(content="Never gonna give you up")
        await asyncio.sleep(1.8)
        await message.edit(content="Never gonna let you down")
        await asyncio.sleep(1.8)
        await message.edit(content="Never gonna run around and desert you")
        await asyncio.sleep(3)
        await message.edit(content="Never gonna make you cry")
        await asyncio.sleep(1.8)
        await message.edit(content="Never gonna say goodbye")
        await asyncio.sleep(1.8)
        await message.edit(content="Never gonna tell a lie and hurt you")
        await asyncio.sleep(3)
        await message.edit(content="https://youtu.be/dQw4w9WgXcQ")


    @commands.command(aliases=["turtl"], help="wacky")
    async def turtle(self, ctx):
        await ctx.send("https://youtu.be/Wl9oUBgFk6Y")


    @commands.command(aliases=["fly", "hover"], help="waw it's a flying drone")
    async def drone(self, ctx):
        y = random.randint(4, 8)
        x = random.randint(1, 8)
        send = "_ _\n" * (10 - y)
        send += "<:__:1028468329456865310>" * x + "<:drone:1028412786017062992>\n"
        send += "\n" * (y)
        await ctx.send(send + "waw it's flying oh mah god")


    @commands.command(aliases=["autotainment", "rj", "randomfunny"], help="https://youtu.be/j4Ph02gzqmY")
    async def randomjoke(self, ctx, joke=None):
        if joke == None:
            joke = random.choice(["Why did the chicken cross the road?",
                                "What did one acorn say to the other?",
                                "How do you calm down a raging bull?",
                                "Knock knock.\nWho's there?",
                                "What is a pillow's favourite genre of music?",
                                "How many bakers does it take to change a light bulb?",
                                "How did the shark catch the stingray?"])

        embed = discord.Embed(colour=random.randint(0, 16777215))
        embed.set_author(name="AUTOTAINMENT")
        embed.description = f"{joke}\n`{random.choice(self.nouns).upper()}`\n\nhttps://youtu.be/j4Ph02gzqmY"
        embed.set_footer(text="haha funny")
        await ctx.send(embed=embed)


    @commands.command(aliases=["bin", "binarycounter"], help="binary counter")
    async def binary(self, ctx):
        decval = 0
        binval = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        emojify = lambda i: ("0️⃣", "◼") if i == 0 else ("1️⃣", "◻")
        invert = lambda i: 0 if i == 1 else 1

        def plusone(look=(-1)):
            binval[look] = invert(binval[look])
            if binval[look] == 0:
                plusone(look=(look - 1))
            else:
                return binval

        embed = discord.Embed(colour=0x000000)
        embed.set_author(name="BINARY COUNTER")
        embed.description = f"Decimal value: `{decval}`"
        embed.add_field(name="_ _", value=f"{''.join([emojify(i)[0] for i in binval])}\n{''.join([emojify(i)[1] for i in binval])}")
        m = await ctx.send(embed=embed)

        await m.add_reaction("➕")
        await m.add_reaction("⏹")

        def check(reaction, user):
            return user == ctx.author and reaction.emoji in ("➕", "⏹") and reaction.message == m

        while True:
            try:
                reaction, user = await self.client.wait_for("reaction_add", check=check, timeout=60)
            except asyncio.TimeoutError:
                await m.clear_reactions()
                break

            if reaction.emoji == "➕":
                await reaction.remove(user)
                if decval < 63:
                    decval += 1
                    plusone()
                else:
                    pass

            if reaction.emoji == "⏹":
                await m.clear_reactions()
                break

            embed = discord.Embed(colour=(0x000000 if binval[-1] == 0 else 0xfffffe))
            embed.set_author(name="BINARY COUNTER")
            embed.description = f"Decimal value: `{decval}`"
            embed.add_field(name="_ _", value=f"{''.join([emojify(i)[0] for i in binval])}\n{''.join([emojify(i)[1] for i in binval])}")
            await m.edit(embed=embed)


    @commands.command(help="egg")
    async def egg(self, ctx):
        await ctx.send("You found this egg!")
        await ctx.send("🥚")


    @commands.command(aliases=["curse", "satanify", "satan"], help="weird glitch text")
    async def zalgo(self, ctx, *, text):
        chars = ["̀", "́", "̂", "̃", "̄", "̅", "̆", "̇", "̈", "̉", "̊", "̋", "̌", "̍", "̎", "̏",
                "̐", "̑", "̒", "̓", "̔", "̕", "̖", "̗", "̘", "̙", "̚", "̛", "̜", "̝", "̞", "̟",
                "̠", "̡", "̢", "̣", "̤", "̥", "̦", "̧", "̨", "̩", "̪", "̫", "̬", "̭", "̮", "̯",
                "̰", "̱", "̲", "̳", "̴", "̵", "̶", "̷", "̸", "̹", "̺", "̻", "̼", "̽", "̾", "̿",
                "̀", "́", "͂", "̓", "̈́", "ͅ", "͆", "͇", "͈", "͉", "͊", "͋", "͌", "͍", "͎",
                "͐", "͑", "͒", "͓", "͔", "͕", "͖", "͗", "͘", "͙", "͚", "͛", "͜", "͝", "͞", "͟",
                "͠", "͡", "͢", "ͣ", "ͤ", "ͥ", "ͦ", "ͧ", "ͨ", "ͩ", "ͪ", "ͫ", "ͬ", "ͭ", "ͮ", "ͯ"]
        words = []
        words += text
        newwords = words[:]
        for i, j in enumerate(words):
            for a in range(random.randint(10, 20)):
                newwords[i] += random.choice(chars)
        words = "".join(newwords)
        await ctx.send(words)


    @commands.command(aliases=["inversedict", "undefine", "rd", "reversedict", "makeword"], help="creates a word out of a definition")
    async def reversedictionary(self, ctx, *, definition):
        with open("roots.json", encoding="utf-8") as f:
            dictionary = json.load(f)

        segments = []
        remains = []

        for definition_word in definition.split():
            has_root = False
            for root in dictionary:
                rootmeaning = root["meaning"].lower().split()
                if definition_word.lower() in rootmeaning:
                    if definition_word.lower() not in ("a", "and", "or", "of"):
                        segments.append(root["root"].split(",")[0])
                        has_root = True
            if not has_root:
                remains.append(definition_word)

        for segment in segments:
            if segment.startswith("-") and segment.endswith("-"):
                continue
            if segment.startswith("-"):
                segments.remove(segment)
                segments.insert(0, segment)
            if segment.endswith("-"):
                segments.remove(segment)
                segments.insert(-1, segment)

        remains.insert(0, "".join(segments))
        word = "".join(remains).replace("-", "")
        if word[-1] in ("i", "u"):
            word += "e"
        word.replace("(", "").replace(")", "")
        await ctx.send(f"**{discord.utils.escape_markdown(definition)}**: `{word}`")


async def setup(client):
    await client.add_cog(Other(client))
