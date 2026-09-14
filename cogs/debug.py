import discord
from discord.ext import commands
from discord.utils import get
from matplotlib import pyplot as plt
import numpy as np
import datetime
from PIL import Image
# from tqdm.asyncio import tqdm
import pyautogui
import pyperclip
import aiohttp
# import pandas
import io
import json
import time
import pydoc
import random
import asyncio
import imagehash

# rcd invoke jsontoembed
class Debug(commands.Cog, name="🔧 Debug", description="""
This category is probably not very useful for you.
Most of these are developer tools, that help develop Serpynth.
Some are commands and concepts being tested.
A few are programming-related commands, which could probably
have been in the 💬 Other category.
And some are just generally useless.
"""):

    def __init__(self, client):
        self.client = client

        with open("commands.json", "r") as f:
            self.commandstats = json.load(f)


    async def earlyaccesscheck(ctx):
        role = ctx.guild.get_role(832656410297892865)
        return (role in ctx.author.roles) or ctx.author.id == 597852310764519434


    @commands.Cog.listener()
    async def on_command(self, ctx):
        if ctx.command.name not in self.commandstats:
            self.commandstats[ctx.command.name] = 1
        else:
            self.commandstats[ctx.command.name] += 1


    #@commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            errortype = "Invalid command"
        elif isinstance(error, commands.MissingRequiredArgument):
            errortype = "Missing argument"
        elif isinstance(error, commands.BadArgument):
            errortype = "Invalid argument"
        elif isinstance(error, commands.CommandOnCooldown):
            errortype = "Command on cooldown"
            t = float(str(error).split()[-1][0:-1])
            hrs = "{:,}".format(round(t // 3600))
            min = round(t % 3600 // 60)
            sec = round(t % 60)
            error = f"You are on cooldown. Try again in {hrs}h, {min}m and {sec}s"
        elif isinstance(error, commands.CheckFailure):
            errortype = "Missing checks"
        elif isinstance(error, commands.BotMissingPermissions):
            errortype = "Bot missing permissions"
        elif isinstance(error, commands.MissingPermissions):
            errortype = "User missing permissions"
        elif isinstance(error, commands.CommandInvokeError):
            if str(error).replace("Command raised an exception: ", "") != "return: ":
                errortype = "Internal error"
            else:
                errortype = None
        else:
            errortype = "Unknown error"

        if not errortype in ("Invalid command", None):
            try:
                await ctx.message.add_reaction("⚠")
                embed = discord.Embed(color=0xff4747)
                embed.set_author(name="A problem occurred:", url=ctx.message.jump_url)
                embed.description = f"{error}"
                await ctx.reply(embed=embed, mention_author=False)
            except Exception as e:
                await ctx.send(e)


    @commands.command(aliases=["pong"])
    async def ping(self, ctx):
        """ Checks client latency & assures proper function. """
        
        msg = await ctx.send(f"""🏓 Pong! ```prolog
LATENCY: {round(self.client.latency, 2) * 1000}ms
CACHED MESSAGES: {len(self.client.cached_messages)}/{self.client.max_messages}
COGS: {len(self.client.cogs)}/10
```""")

        try:
            voice = get(self.client.voice_clients, guild=ctx.guild)
            voice.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=f"Ping.mp3"))
        except:
            pass


    @commands.command(aliases=["bypassay", "bpsay", "bps"])
    @commands.is_owner()
    async def bypasssay(self, ctx, *, message):
        """ Repeats a message, without quote. """

        if message.startswith("--"):
            message = message[2:]
            await ctx.message.delete()
            print(message)
        await ctx.send(message)


    @commands.command(aliases=["closeconnection", "close"])
    @commands.is_owner()
    async def kill(self, ctx):
        """ Closes the program and the bot's connection to Discord. """

        await ctx.send("Are you sure you want to close the bot connection to Discord? (y/n)")
        def check(m):
            return m.content.lower() in ("y", "n") and m.channel == ctx.message.channel and m.author == ctx.message.author
        try:
            msg = await self.client.wait_for("message", timeout=15.0, check=check)
        except asyncio.TimeoutError:
            pass
        else:
            if msg.content.lower() == "y":
                await ctx.send("Okay then. See you again when I'm back online!")
                await self.client.close()
            else:
                await ctx.send("Okay then, I'll stay online.")


    @commands.command(aliases=["pythonhelp"])
    @commands.is_owner()
    async def pyhelp(self, ctx, *, thing="help"):
        """ Returns Python's help message on an object. """

        try:
            exec(f"import {thing}")
        except:
            pass
        l = []
        l += pydoc.render_doc(eval(thing), "Help on %s:")
        for i, j in enumerate(l):
            if j == "":
                l[i] = ""
                l[i + 1] = ""
        lines = "".join(l).split("\n")

        send = ["```"]
        for i in lines:
            if len(send[len(send) - 1] + i) > 1990:
                send[len(send) - 1] += "```"
                send.append("```" + i)
            else:
                send[len(send) - 1] += i + "\n"
        send[len(send) - 1] += "```"

        for i in send:
            await ctx.send(i)
            await asyncio.sleep(2)


    @commands.command(aliases=["subspam"])
    @commands.is_owner()
    async def slowspam(self, ctx, amount: int, *, message):
        """ Repeatedly sends one message per second. """

        for i in range(amount):
            await ctx.send(message)
            await asyncio.sleep(1.0)


    @commands.command()
    async def spam(self, ctx, amount: int, *, message):
        """ Repeatedly sends five messages per five seconds. """

        for i in range(amount):
            await ctx.send(message)


    @commands.command(aliases=["status"])
    @commands.is_owner()
    async def changestatus(self, ctx, status="dnd", type="watching", *, activity="you 👀 | syhelp"):
        """ Changes Serpynth's Discord status and activity. """

        emjstat = {"online": "<:online:791141829692489808>",
                    "offline": "<:offline:791141825275494411>",
                    "idle": "<:idle:791141829126389770>",
                    "dnd": "<:dnd:791141827847782450>"}

        await self.client.change_presence(status=eval(f"discord.Status.{status}"),
                                        activity=discord.Activity(type=eval(f"discord.ActivityType.{type}"),
                                                                    name=activity))

        await ctx.send(f"**Changed status**\n{emjstat[status]} {type.capitalize()} {activity}")


    @commands.command(aliases=["reinvoke"])
    @commands.is_owner()
    async def invoke(self, ctx, *, message=""):
        """ Reinvokes a command already sent by someone. """

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
        await self.client.process_commands(msg)
        await ctx.message.add_reaction('✅')


    @commands.command(aliases=["ag", "import antigravity", "0g"])
    async def antigravity(self, ctx):
        """ I wrote 20 short programs in Python yesterday. It was wonderful. Perl, I'm leaving you. """

        embed = discord.Embed(color=random.randint(0, 16777215))
        embed.set_author(name="Python", url=f"https://xkcd.com/353")
        embed.description = "I wrote 20 short programs in Python yesterday. It was wonderful. Perl, I'm leaving you."
        embed.add_field(name="_ _", value=f"Number: [`353`](https://xkcd.com/353)\n")
        embed.set_image(url="https://imgs.xkcd.com/comics/python.png")
        embed.set_footer(text="https://xkcd.com/")
        embed.timestamp = datetime.datetime(2007, 12, 5)
        await ctx.send(embed=embed)


    @commands.command(aliases=["ok", "okay", "isready"])
    async def ready(self, ctx):
        """ Checks if Serpynth is ready to give replies. """

        if self.client.is_ready():
            await ctx.send("✅ I'm good to go!")
        else:
            await ctx.send("❎ Not ready yet!")


    @commands.command(aliases=["je", "json2em", "jsonembed", "json2embed"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def jsontoembed(self, ctx, *, _json=""):
        """ Creates an embed from JSON code. """

        _json = _json.replace("```json", "").replace("```\n", "").replace("\n```", "").replace("```", "")
        dec = json.JSONDecoder()
        try:
            _json = dec.decode(_json)
            embed = discord.Embed.from_dict(_json)
        except Exception as e:
            await ctx.send(f"An error occured while running this command.\nMake sure that your JSON is in the correct format.\n`{e}`")
            return

        try:
            await ctx.send(embed=embed)
        except discord.HTTPException:
            await ctx.send(embed=discord.Embed(description="​"))


    @commands.command(aliases=["ej", "em2json", "embedjson", "embed2json"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def embedtojson(self, ctx, *, message=""):
        """ Returns a JSON containing data from an embed. """

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
        if len(msg.embeds) < 1:
            await ctx.send("This message does not have any embeds!")
            return

        files = [discord.File(io.StringIO(json.dumps(embed.to_dict(), indent=2, ensure_ascii=False)), filename="embed.json") for embed in msg.embeds]
        await ctx.send(files=files)


    @commands.command(aliases=["recooldown", "rcd", "cd"])
    @commands.is_owner()
    async def resetcooldown(self, ctx, cmd):
        """ Resets the cooldown for a command. """

        thecmd = self.client.get_command(cmd)
        if thecmd == None:
            await ctx.send(f"Command `sy{cmd}` not found.")
        else:
            thecmd.reset_cooldown(ctx)
            await ctx.send(f"Your cooldown for `sy{cmd}` has been reset.")


    @commands.command(aliases=["autocmd", "acmd"])
    @commands.is_owner()
    async def autocommand(self, ctx, cmd, *args):
        """ Automatically runs a specific command in a channel repeatedly. """

        thecmd = self.client.get_command(cmd)
        if thecmd == None:
            await ctx.send(f"Command `sy{cmd}` not found.")
        else:
            checks = True
            for i in thecmd.checks:
                try:
                    checks = await i.__call__(ctx)
                except TypeError:
                    checks = i.__call__(ctx)
                if checks == False:
                    break

            parameters = {}
            try:
                for i in range(len(list(thecmd.clean_params))):
                    parameters[list(thecmd.clean_params)[i]] = args[i]
            except IndexError:
                await ctx.send("All parameters must be filled, even if they were optional.")
                return

            await ctx.send("What do you want your delay in seconds between commands to be?\nMinimum = 10s")

            def check(m):
                try:
                    float(m.content)
                except:
                    return False
                else:
                    if m.channel == ctx.channel and m.author == ctx.author:
                        if float(m.content) >= 10 or ctx.author.id == 597852310764519434:
                            return True
                        else:
                            return False
                    else:
                        return False

            def breakcmd(n):
                return n.channel == ctx.channel and n.author.permissions_in(ctx.channel).manage_channels and n.content.lower() == "end"

            try:
                m = await self.client.wait_for("message", check=check, timeout=25.0)
            except asyncio.TimeoutError:
                pass
            else:
                timeout = float(m.content)
                await ctx.send("Autocommand loop has now started.\nAt any time, type `end` to stop the loop")

                while True:
                    try:
                        n = await self.client.wait_for("message", check=breakcmd, timeout=timeout)
                    except:
                        await ctx.invoke(thecmd, **parameters)
                    else:
                        await ctx.send("Ended autocommand loop.")
                        break


    @commands.command(aliases=["plt", "pyplot", "matplotlib.pyplot", "matplotlib"])
    @commands.cooldown(2, 60, commands.BucketType.user)
    @commands.is_owner()
    @commands.check(earlyaccesscheck)
    async def plot(self, ctx, *, code):
        """ Displays a matplotlib plot, given its code. """

        def fig2img(fig):
            buf = io.BytesIO()
            fig.savefig(buf)
            buf.seek(0)
            img = Image.open(buf)
            return img

        code = code.replace("```python", "").replace("```py", "").replace("```", "")
        code = code.replace("plt.show()", "").replace("print", "")

        if "import" in code:
            await ctx.send("""Your code may not import anything.
`matplotlib.pyplot as plt` and `numpy as np` are already imported for you.""")
            return
        elif "open" in code:
            await ctx.send("""Your code may not open any files.
If you're not actually trying to, you might have to rewrite your variables and/or strings.""")
            return
        elif "save" in code:
            await ctx.send("""Your code may not save any files.
If you're not actually trying to, you might have to rewrite your variables and/or strings.""")
            return
        elif "client" in code:
            await ctx.send(await ctx.send("""Your code may not interact with the bot.
If you're not actually trying to, you might have to rewrite your variables and/or strings."""))
            return
        elif "discord" in code:
            await ctx.send(await ctx.send("""Your code may not interact with the bot.
If you're not actually trying to, you might have to rewrite your variables and/or strings."""))
        elif "ctx" in code:
            await ctx.send(await ctx.send("""Your code may not interact with the bot.
If you're not actually trying to, you might have to rewrite your variables and/or strings."""))
        elif "command" in code:
            await ctx.send(await ctx.send("""Your code may not interact with the bot.
If you're not actually trying to, you might have to rewrite your variables and/or strings."""))
        elif "sleep" in code:
            await ctx.send(await ctx.send("""Your code may not use `time.sleep()` or `asyncio.sleep()`.
If you're not actually trying to, you might have to rewrite your variables and/or strings."""))

        exec(code)
        image = fig2img(plt.gcf())
        image.save("screenshot.png")

        await ctx.send(file=discord.File("screenshot.png"))
        plt.clf()


    @commands.command(aliases=["removecmd"])
    @commands.is_owner()
    async def removecommand(self, ctx, *, command):
        """ Removes a command from the current session. """

        self.client.remove_command(command.lower())
        await ctx.send(f"Removed `{command}` command.")


    @commands.command(aliases=["cm"])
    @commands.is_owner()
    async def copymessage(self, ctx, message=None, clean: bool = True):
        """ Attaches a message's content to the clipboard. """

        if message == None:
            messages = [i async for i in ctx.channel.history(limit=2)]
            message = str(messages[1].id)
        if message.startswith("https://discord.com/channels/"):
            message = message.split("/")[6]
        try:
            msg = await ctx.channel.fetch_message(message)
        except:
            if ctx.message.reference != None:
                msg = await ctx.channel.fetch_message(ctx.message.reference.message_id)
            else:
                await ctx.send("Message ID not found.")
                return

        content = msg.clean_content if clean == True else msg.content
        if content:
            pyperclip.copy(content)
            await ctx.send(f"Successfully copied to clipboard.\n```{content}```")
        else:
            await ctx.send("Your message does not have any copyable content.")


    @commands.command(aliases=["puppeteer", "puppetmaster"])
    @commands.is_owner()
    async def puppet(self, ctx):
        """ (TEST COMMAND) Controls the PC's mouse and/or keyboard. """

        await ctx.message.add_reaction("✅")
        pyautogui.moveTo(2500, 993)
        pyautogui.click()
        pyautogui.typewrite("hello world\n")


    @commands.command(name="the command that is impossible to invoke")
    async def squarebobspongepants(self, ctx):
        """ (TEST COMMAND) Since the command's name contains spaces, it is impossible to invoke. """

        await ctx.send("what")
    

    @commands.command(aliases=["button", "interactions", "interaction"], help="Buttons.")
    @commands.is_owner()
    async def buttons(self, ctx):
        """(TEST COMMAND) Creates a Discord interaction, with buttons!"""

        view = discord.ui.View()
        button = discord.ui.Button(label="Click??", style=discord.ButtonStyle.green)
        select = discord.ui.Select(placeholder="SELECTTTTTTT")
        select.add_option(label="1", value="one", description="I")
        select.add_option(label="2", value="two", description="II")
        select.add_option(label="3", value="three", description="III")
        select.add_option(label="4", value="four", description="IV")


        async def buttoncallback(interaction):
            await interaction.response.send_message(f"{interaction.user} believes that ducks are cool", ephemeral=True)
        
        async def selectcallback(interaction):
            await interaction.response.send_message(f"what is {select.values[0]}")
        
        button.callback = buttoncallback
        select.callback = selectcallback
        view.add_item(item=button)
        view.add_item(item=select)
        await ctx.send(view=view)
    

    @commands.command(aliases=["tiletest"])
    @commands.is_owner()
    async def tilestest(self, ctx, times: int = 1):
        """ (TEST COMMAND) Uses tile emojis to create an image. """

        guild = self.client.get_guild(1028424529804001310)
        send = ""
        send += "<:bc:1028465970521579580>" * times

        await ctx.send(send)
        await ctx.send(len(send))
    

    @commands.command(aliases=["tile"])
    @commands.is_owner()
    async def tileify(self, ctx, width: int = 10):
        """ Generates a series of tiles from a given image. """

        guild = self.client.get_guild(1028452824352292904)
        found = None

        if len(ctx.message.attachments) > 0:
            file = ctx.message.attachments[0]
            if file.content_type.startswith("image/"):
                image = Image.open(io.BytesIO(await file.read()))
                found = True

        if found != True and ctx.message.reference != None:
            message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
            if len(message.attachments) > 0:
                file = message.attachments[0]
                if file.content_type.startswith("image/"):
                    image = Image.open(io.BytesIO(await file.read()))
                    found = True
        
        if not found:
            await ctx.send("No image found.\nAttach an image file when sending the command, " + \
                            "or reply to a message with an image.")
            return
        
        class Dummy:
            async def delete(self):
                pass

        image = image.resize((width, round(image.height * width/image.width)))
        emoji = Dummy()
        value = None

        for y in range(image.height):
            row = ""
            emojis = []

            for x in range(image.width):

                value = image.getpixel((x, y))
                pixel = Image.new("RGBA", (1, 1), color=value)

                with io.BytesIO() as binary:
                    pixel.save(binary, "PNG")
                    binary.seek(0)
                    emoji = await guild.create_custom_emoji(name="xx", image=binary.getvalue())
                    emojis.append(emoji)
                
                row += f"<:{emoji.name}:{emoji.id}> "
        
            await ctx.send(row)
            for emoji in emojis:
                await emoji.delete()



    @commands.command(aliases=[])
    async def collectmessage(self, ctx, *, id=""):
        """ (TEST COMMAND) Finds a message, given a reply, an ID or a jump URL. """

        if id.startswith("https://discord.com/channels/"):
            id = id.split("/")[6]
        try:
            message = await ctx.channel.fetch_message(id)
        except:
            message = None

        if message == None:
            if ctx.message.reference != None:
                message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
            else:
                await ctx.send("Message not found.")
                return
        
        await ctx.send(message.jump_url)


    @commands.command(aliases=["hardcommand", "hc", "writecommand", "wc"])
    @commands.is_owner()
    async def hardcode(self, ctx, *, code):
        """ Writes code directly into Serpynth's files (debug.py). """

        try:
            msg = await ctx.author.send(content=f"""Here's a copy of the `cogs\\debug.py` file, in case something goes wrong.
Jump back to the channel where `sy{ctx.invoked_with}` was executed: <#{ctx.channel.id}>""",
                            file=discord.File("cogs/debug.py"))
        except Exception as e:
            await ctx.send("I was not able to DM you a copy of the `cogs\\debug.py` file. For this reason, the command has been cancelled.")
            return

        code = code.replace("```python", "").replace("```py", "").replace("```", "")
        code = code.split("\n")
        code = "\n".join(map(lambda x: "    " + x, code))

        file = open("cogs/debug.py", "r", encoding="utf-8")
        write = file.read()
        file.close()

        write = write.split("\n")
        write[write.index("    #⫱") + 1] = code
        out = "Your code has successfully been directly implemented into Serpynth's 🔧 **Debug** category."
        try:
            file = open("cogs/debug.py", "w", encoding="utf-8")
            file.write("\n".join(write))
            file.close()
        except:
            out = "Oh no! Something went wrong while writing in the code."

        await ctx.send(f"""{out}
I've DMed you a copy of `cogs\\debug.py` if you want to reset it to its original form.
{msg.jump_url}
Don't forget to `syreload debug` so that the command actually works!""")


    # `syharcode` output
    #⫱

    




    #⟟


async def setup(client):
    await client.add_cog(Debug(client))
