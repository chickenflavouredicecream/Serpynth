import discord
import io
from discord.ext import commands
from discord.ext import tasks
import urllib.parse
import random
import asyncio
import aiohttp
import asyncpraw as praw
import os
import datetime
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps


class Images(commands.Cog, name="🖼 Images", description="""
These commands work with images!
Some give you random images, some edit your profile picture, etc."""):

    def __init__(self, client):
        self.client = client
        self.reddit = praw.Reddit(client_id=os.environ["REDDIT-ID"],
                        client_secret=os.environ["REDDIT-SECRET"],
                        password=os.environ["REDDIT-PASSWORD"],
                        user_agent=os.environ["REDDIT-AGENT"],
                        username=os.environ["REDDIT-USER"])
#["3", 2, 3, 4, True, 1]
        self.httpnames = {
        0: "Heaven|👼",
        100: "Continue|💬",
        101: "Switching Protocols|↔",
        102: "Processing|💬",
        200: "OK|👌",
        201: "Created|🖼",
        202: "Accepted|🉑",
        204: "", # No Content
        206: "Partial Content|🌗",
        207: "Multi-Status|<:offline:791141825275494411><:online:791141829692489808><:idle:791141829126389770><:dnd:791141827847782450>",
        300: "Multiple Choices|🔢",
        301: "Moved Permanently|📦",
        302: "Found|👇",
        303: "See Other|💬",
        304: "Not Modified",
        305: "Use Proxy",
        307: "Temporary Redirect|➡",
        400: "Bad Request|👎",
        401: "Unauthorized|🆔",
        402: "Payment Required|💸",
        403: "Forbidden|🧙‍♂️",
        404: "Not Found|❓",
        405: "Method Not Allowed|❌",
        406: "Not Acceptable|🚫",
        408: "Request Timeout|⏰",
        409: "Conflict|⚔",
        410: "Gone|🚶‍♂️",
        411: "Length Required|🐍",
        412: "Precondition Failed",
        413: "Payload Too Large|🐘",
        414: "Request-URI Too Long|📏",
        415: "Unsupported Media Type|💿",
        416: "Request Range Not Satisfiable",
        417: "Expectation Failed|🇦",
        418: "I'm a Teapot|🫖",
        420: "Enhance Your Calm|🚬",
        421: "Misdirected Request",
        422: "Unprocessable Entity|👤",
        423: "Locked|🔒",
        424: "Failed Dependency",
        425: "Too Early|🌄",
        426: "Upgrade Required|⬆",
        429: "Too Many Requests|🥺🥺🥺🥺🥺🥺🥺🥺🥺🥺🥺🥺🥺🥺🥺🥺🥺🥺🥺🥺🥺🥺🥺🥺🥺🥺🥺🥺🥺🥺🥺🥺🥺🥺🥺🥺🥺🥺🥺🥺",
        431: "Request Header Fields Too Large|📏",
        444: "", # No Response
        451: "Unavailable For Legal Reasons|⚖",
        499: "Client Closed Request|🔚",
        500: "Internal Server Error",
        501: "Not Implemented",
        502: "Bad Gateway Gate|🚪",
        503: "Service Unavailable|⌚",
        504: "Gateway Timeout|🚪⏰",
        506: "Variant Also Negotiates|🗣",
        507: "Insufficient Storage|🗃",
        508: "Loop Detected|🔄",
        509: "Bandwidth Limit Exceeded|📏",
        510: "Not  E x t e n d e d",
        511: "Network Authentication Required|✅",
        599: "Network Connect Timeout Error|⏰"
        }

    @tasks.loop(seconds=300)
    async def automeme(self):
        channel = self.client.get_channel()
        try:
            subreddit = await self.reddit.subreddit("memes")
            submission = await subreddit.random()
            while submission.over_18:
                submission = await subreddit.random()
            if not submission.is_self:
                embed = discord.Embed(colour=0x2f3136)
                embed.set_author(name=submission.title, url=f"https://redd.it/{submission.id}")
                embed.set_image(url=submission.url)
                await channel.send(embed=embed)
        except:
            pass

    @automeme.before_loop
    async def before_automeme(self):
        await self.client.wait_until_ready()

    def cog_unload(self):
        self.automeme.cancel()


    @commands.command(aliases=["asci", "asciii", "asciiimage", "asciimage"])
    async def ascii(self, ctx, member: discord.Member = None):
        """ Recreates a profile picture in ASCII art. """

        if member == None:
            avt = ctx.author.avatar
        else:
            avt = member.avatar
        image = Image.open(io.BytesIO(await avt.read()))
        CHARS = [" ", ".", ":", ";", "+", "*", "?", "%", "S", "#", "@"]
        def resize(image, neww = 31):
            w, h = image.size
            ratio = h/w
            newh = int(neww * ratio)
            resimage = image.resize((neww, newh))
            return resimage

        def pixtoascii(image):
            pixs = image.getdata()
            chars = " ".join([CHARS[int((p[0] * 0.299 + p[1] * 0.587 + p[2] * 0.114) // 25)] for p in pixs])
            return chars

        newimgdata = pixtoascii(resize(image))
        pixcount = len(newimgdata)
        asciiimage = "\n".join(newimgdata[i:(i + 62)] for i in range(0, pixcount, 62))
        await ctx.send(f"```{asciiimage}```")


    @commands.command(aliases=["xkcdcomics", "xk"])
    async def xkcd(self, ctx, number: int = None):
        """ One of the most well-known comic strips for nerds, brought to Discord. """

        if number == None:
            number = random.randint(1, 2633)
        cont = True
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(f"https://xkcd.com/{number}/info.0.json") as j:
                    info = await j.json()
            except:
                cont = False

        if cont:
            embed = discord.Embed(color=random.randint(0, 16777215))
            embed.set_author(name=info["title"], url=f"https://xkcd.com/{number}")
            embed.description = info["alt"]
            embed.add_field(name="_ _", value=f"Number: [`{number}`](https://xkcd.com/{number})\n")
            embed.set_image(url=info["img"])
            embed.set_footer(text="https://xkcd.com/")
            embed.timestamp = datetime.datetime(int(info["year"]), int(info["month"]), int(info["day"]))
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"xkcd comic `{number}` not found")


    @commands.command(aliases=["https", "http", "httpcat", "httpcats", "httpscat", "httpscats", "webcats"])
    async def webcat(self, ctx, code=""):
        """ `200 OK` """

        codes = [0, 100, 101, 102, 200, 201, 202, 204, 206, 207, 300, 301, 302, 303, 304, 305,
        307, 400, 401, 402, 403, 404, 405, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417,
        418, 420, 421, 422, 423, 424, 425, 426, 429, 431, 444, 451, 499, 500, 501, 502, 503,
        504, 506, 507, 508, 509, 510, 511, 599]

        if code == "":
            code = random.choice(codes)
            while code == 0:
                code = random.choice(codes)
        else:
            try:
                code = int(code)
            except:
                pass
            if code not in codes:
                code = 404

        embed = discord.Embed()

        if code in (100, 101, 102, 300, 301, 302, 303, 304, 305, 307):
            embed.colour = 0xffff00
        if code in (200, 201, 202, 203, 206, 207):
            embed.colour = 0x00ff00
        if code in (400, 401, 402, 403, 404, 405, 406, 408, 409, 410, 411,
                    412, 413, 414, 415, 416, 417, 421, 422, 423, 424, 425,
                    426, 429, 431, 451, 499, 500, 502, 503, 504, 506, 507,
                    508, 509, 510, 511, 599):
            embed.colour = 0xff0000
        if code == 418:
            embed.colour = 0x9932cc
        if code == 420:
            embed.colour = 0x008a00
        if code in (204, 444, 501):
            embed.colour = 0x000000
        if code == 0:
            embed.colour = 0x87ceff

        embed.set_author(name=str(code) + ": " + self.httpnames[code].split("|")[0], url=f"https://http.cat/{code}")
        if "|" in self.httpnames[code]:
            if code != 418:
                embed.add_field(name=self.httpnames[code].split("|")[1], value="_ _")
            else:
                embed.add_field(name=self.httpnames[code].split("|")[1], value="https://www.google.com/teapot")
        embed.set_image(url=f"https://http.cat/{code}")
        embed.set_footer(text=f"https://http.cat/")
        await ctx.send(embed=embed)


    @commands.command(aliases=["cats", "meow", "purr"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.is_owner()
    async def cat(self, ctx):
        """ https://youtu.be/VN6kPoA5jrA\n(this command does not work at the moment) """

        async with aiohttp.ClientSession() as session:
            async with session.get("https://aws.random.cat/meow") as info:
                info = await info.json()

        embed = discord.Embed(colour=random.randint(0, 16777215))
        embed.set_author(name="🐱 CATS!")
        embed.set_image(url=info["file"].replace("\\", ""))
        embed.set_footer(text="https://aws.random.cat/")
        await ctx.send(embed=embed)


    @commands.command(aliases=["foxes"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def fox(self, ctx):
        """ Finds the nicest pictures of the nices foxes. """

        async with aiohttp.ClientSession() as session:
            async with session.get("https://randomfox.ca/floof/") as info:
                info = await info.json()

        embed = discord.Embed(colour=random.randint(0, 16777215))
        embed.set_author(name="🦊 FOXES!")
        embed.set_image(url=info["image"].replace("\\", ""))
        embed.set_footer(text="https://randomfox.ca/floof/")
        await ctx.send(embed=embed)


    @commands.command(aliases=["doggo", "dogs", "woof"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def dog(self, ctx):
        """ Finds a picture of a good boy. """

        async with aiohttp.ClientSession() as session:
            async with session.get("https://dog.ceo/api/breeds/image/random") as info:
                info = await info.json()

        embed = discord.Embed(colour=random.randint(0, 16777215))
        embed.set_author(name="🐶 DOGS!")
        embed.set_image(url=info["message"].replace("\\", ""))
        embed.set_footer(text="https://dog.ceo/dog-api/")
        await ctx.send(embed=embed)


    @commands.command(aliases=["rp", "redpandas"])
    @commands.is_owner()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def redpanda(self, ctx):
        """ Finds a picture of a red panda.\n(this command does not work at the moment) """

        async with aiohttp.ClientSession() as session:
            async with session.get("https://some-random-api.ml/img/red_panda") as info:
                info = await info.json()

        embed = discord.Embed(colour=random.randint(0, 16777215))
        embed.set_author(name="🔴🐼 RED PANDAS!")
        embed.set_image(url=info["link"])
        embed.set_footer(text="https://some-random-api.ml/")
        await ctx.send(embed=embed)


    @commands.command(aliases=["ducks", "ducc", "quack"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def duck(self, ctx):
        """ Summons a duck from thin air. """

        async with aiohttp.ClientSession() as session:
            async with session.get("https://random-d.uk/api/random") as info:
                info = await info.json()

        embed = discord.Embed(colour=random.randint(0, 16777215))
        embed.set_author(name="🦆 DUCKS!")
        embed.set_image(url=info["url"].replace("\\", ""))
        embed.set_footer(text="https://random-d.uk/")
        await ctx.send(embed=embed)


    @commands.command(aliases=["snek", "snakes"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def snake(self, ctx):
        """ SSNNNAAAAKKKESSSSS??????? """

        async with ctx.channel.typing():
            subreddit = await self.reddit.subreddit("snake")
            submission = await subreddit.random()
            correcttype = False
            while not correcttype:
                submission = await subreddit.random()
                correcttype = False
                for i in (".jpg", ".png", ".jpeg", ".gif"):
                    if i in submission.url:
                        correcttype = True

            embed = discord.Embed(colour=random.randint(0, 16777215))
            embed.set_author(name="🐍 SNAKES!", url=f"https://www.reddit.com/{submission.id}")
            embed.set_image(url=submission.url)
            embed.set_footer(text="https://www.reddit.com/r/snakes/")
            await ctx.send(embed=embed)


    @commands.command(aliases=["hoot", "owls"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def owl(self, ctx):
        """ Collects a random image of an owl.\n(command may be slow) """

        async with ctx.channel.typing():
            subreddit = await self.reddit.subreddit("superbowl")
            submission = await subreddit.random()
            correcttype = False
            while not correcttype:
                submission = await subreddit.random()
                correcttype = False
                for i in (".jpg", ".png", ".jpeg", ".gif"):
                    if i in submission.url:
                        correcttype = True

            embed = discord.Embed(colour=random.randint(0, 16777215))
            embed.set_author(name="🦉 OWLS!", url=f"https://www.reddit.com/{submission.id}")
            embed.set_image(url=submission.url)
            embed.set_footer(text="https://www.reddit.com/r/superbowl/")
            await ctx.send(embed=embed)


    @commands.command(aliases=["memes"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def meme(self, ctx):
        """ Collects a random meme from [r/memes](https://reddit.com/r/memes/).\n(command may be slow) """

        async with ctx.channel.typing():
            subreddit = await self.reddit.subreddit("memes")
            submission = await subreddit.random()
            correcttype = False
            while not correcttype or submission.over_18:
                submission = await subreddit.random()
                correcttype = False
                for i in (".jpg", ".png", ".jpeg", ".gif"):
                    if i in submission.url:
                        correcttype = True

            title = []
            title += submission.title
            dotdotdot = False
            while len(title) > 252:
                title.pop(len(title) - 1)
                dotdotdot = True
            title = "".join(title)
            if dotdotdot:
                title += "..."

            embed = discord.Embed(colour=random.randint(0, 16777215))
            embed.set_author(name=title, url=f"https://www.reddit.com/{submission.id}")
            embed.set_image(url=submission.url)
            embed.set_footer(text="The command \"syreddit memes\" exists, you know")
            await ctx.send(embed=embed)


    @commands.command(aliases=["minecraft", "mc", "achieve", "minecraftachievement"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def achievement(self, ctx, *, text="your text here"):
        """ Generates a fake Minecraft achievement message. """

        embed = discord.Embed(colour=random.randint(0, 16777215))
        text = urllib.parse.quote_plus(text)
        embed.set_author(name="MINECRAFT")
        embed.set_image(url=f"https://minecraftskinstealer.com/achievement/{random.randint(1, 39)}/Achievement+Get%21/{text}")
        embed.set_footer(text="https://minecraftskinstealer.com/achievement/")
        await ctx.send(embed=embed)



    @commands.command(aliases=["greyscale", "gray", "grey"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def grayscale(self, ctx, member: discord.Member = None):
        """ Removes the colours from a profile picture. """

        if member == None:
            avt = ctx.author.avatar
        else:
            avt = member.avatar
        image = Image.open(io.BytesIO(await avt.read()))

        def resize(image, neww=300):
            w, h = image.size
            ratio = h/w
            newh = int(neww * ratio)
            resimage = image.resize((neww, newh))
            return resimage

        image = resize(image).convert("L")
        with io.BytesIO() as binary:
            image.save(binary, "PNG")
            binary.seek(0)
            await ctx.send(file=discord.File(fp=binary, filename="grayed.png"))


    @commands.command(aliases=["widen", "stretch", "big"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def wide(self, ctx, member: discord.Member = None, stretch=500):
        """ Comedically stretches out a profile picture horizontally. """

        if member == None:
            avt = ctx.author.avatar
        else:
            avt = member.avatar

        if stretch > 5000 or stretch < -290:
            stretch = 500

        image = Image.open(io.BytesIO(await avt.read()))

        def resize(image, neww=300):
            w, h = image.size
            ratio = h/w
            newh = int(neww * ratio)
            resimage = image.resize((neww + stretch, newh))
            return resimage

        image = resize(image)
        with io.BytesIO() as binary:
            image.save(binary, "PNG")
            binary.seek(0)
            await ctx.send(file=discord.File(fp=binary, filename="widened.png"))


    @commands.command(aliases=["lq", "lowdefinition"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def lowquality(self, ctx, member: discord.Member = None, quality=30):
        """ Removes pixels from a profile picture. """

        if member == None:
            avt = ctx.author.avatar
        else:
            avt = member.avatar

        if quality > 1000 or quality < 1:
            quality = 50

        image = Image.open(io.BytesIO(await avt.read()))

        def resize(image, neww=quality):
            w, h = image.size
            ratio = h/w
            newh = int(neww * ratio)
            resimage = image.resize((neww, newh))
            return resimage

        image = resize(resize(image), 300)
        with io.BytesIO() as binary:
            image.save(binary, "PNG")
            binary.seek(0)
            await ctx.send(file=discord.File(fp=binary, filename="lowquality.png"))


    @commands.command(aliases=["mdb", "mandelbrotify"])
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def mandelbrot(self, ctx, quality=100):
        """ Generates a graphic of the Mandelbrot set. """

        if quality > 1500 or quality < 2:
            quality = 100

        image = Image.effect_mandelbrot((300, 300), (-2, -1.5, 1, 1.5), quality)
        with io.BytesIO() as binary:
            image.save(binary, "PNG")
            binary.seek(0)
            await ctx.send(file=discord.File(fp=binary, filename="mandelbrot.png"))


    @commands.command(aliases=["gaussiannoise", "gaussianoise"])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def noise(self, ctx, randomness=100):
        """ Generates an image where each pixel is randomized. """

        image = Image.effect_noise((300, 300), randomness)
        with io.BytesIO() as binary:
            image.save(binary, "PNG")
            binary.seek(0)
            await ctx.send(file=discord.File(fp=binary, filename="noise.png"))


    @commands.command(aliases=["disintegrate", "thanosify", "thanos"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def dissolve(self, ctx, member: discord.Member = None, spread=50):
        """ Scatters the pixels on a profile picture. """

        if spread > 200 or spread < 1:
            spread = 50

        if member == None:
            avt = ctx.author.avatar
        else:
            avt = member.avatar
        image = Image.open(io.BytesIO(await avt.read()))

        def resize(image, neww=300):
            w, h = image.size
            ratio = h/w
            newh = int(neww * ratio)
            resimage = image.resize((neww, newh))
            return resimage

        image = resize(image).effect_spread(spread)
        with io.BytesIO() as binary:
            image.save(binary, "PNG")
            binary.seek(0)
            await ctx.send(file=discord.File(fp=binary, filename="dissolved.png"))


    @commands.command(aliases=["blurry"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def blur(self, ctx, member: discord.Member = None, intensity=3):
        """ Blurs a profile picture. """

        if member == None:
            user = ctx.author
            avt = ctx.author.avatar
        else:
            user = member
            avt = member.avatar
        image = Image.open(io.BytesIO(await avt.read()))

        if user.avatar.is_animated():
            await ctx.send("Unfortunately, this command does not work with animated profile pictures.")
            return

        def resize(image, neww=300):
            w, h = image.size
            ratio = h/w
            newh = int(neww * ratio)
            resimage = image.resize((neww, newh))
            return resimage

        image = resize(image).filter(ImageFilter.GaussianBlur(intensity))
        with io.BytesIO() as binary:
            image.save(binary, "PNG")
            binary.seek(0)
            await ctx.send(file=discord.File(fp=binary, filename="blurred.png"))


    @commands.command(aliases=["edge", "findedges"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def edges(self, ctx, member: discord.Member = None):
        """ Highlights the edges on a profile picture. """

        if member == None:
            user = ctx.author
            avt = ctx.author.avatar
        else:
            user = member
            avt = member.avatar
        image = Image.open(io.BytesIO(await avt.read()))

        if user.avatar.is_animated():
            await ctx.send("Unfortunately, this command does not work with animated profile pictures.")
            return

        def resize(image, neww=300):
            w, h = image.size
            ratio = h/w
            newh = int(neww * ratio)
            resimage = image.resize((neww, newh))
            return resimage

        image = resize(image).filter(ImageFilter.CONTOUR)
        with io.BytesIO() as binary:
            image.save(binary, "PNG")
            binary.seek(0)
            await ctx.send(file=discord.File(fp=binary, filename="edges.png"))


    @commands.command(aliases=["embossed"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def emboss(self, ctx, member: discord.Member = None):
        """ Provides an embossed effect on a profile picture. """

        if member == None:
            user = ctx.author
            avt = ctx.author.avatar
        else:
            user = member
            avt = member.avatar
        image = Image.open(io.BytesIO(await avt.read()))

        if user.avatar.is_animated():
            await ctx.send("Unfortunately, this command does not work with animated profile pictures.")
            return

        def resize(image, neww=300):
            w, h = image.size
            ratio = h/w
            newh = int(neww * ratio)
            resimage = image.resize((neww, newh))
            return resimage

        image = resize(image).filter(ImageFilter.EMBOSS)
        with io.BytesIO() as binary:
            image.save(binary, "PNG")
            binary.seek(0)
            await ctx.send(file=discord.File(fp=binary, filename="embossed.png"))


    @commands.command(aliases=["detail", "wash"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def clean(self, ctx, member: discord.Member = None):
        """ Provides a profile picture with a polished look. """

        if member == None:
            user = ctx.author
            avt = ctx.author.avatar
        else:
            user = member
            avt = member.avatar
        image = Image.open(io.BytesIO(await avt.read()))

        if user.avatar.is_animated():
            await ctx.send("Unfortunately, this command does not work with animated profile pictures.")
            return

        def resize(image, neww=300):
            w, h = image.size
            ratio = h/w
            newh = int(neww * ratio)
            resimage = image.resize((neww, newh))
            return resimage

        image = resize(image).filter(ImageFilter.DETAIL)
        with io.BytesIO() as binary:
            image.save(binary, "PNG")
            binary.seek(0)
            await ctx.send(file=discord.File(fp=binary, filename="cleaned.png"))


    @commands.command(aliases=["bw", "gray2", "blackwhite"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def blackandwhite(self, ctx, member: discord.Member = None):
        """ Rounds each pixel on a profile picture to either black or white. """

        if member == None:
            avt = ctx.author.avatar
        else:
            avt = member.avatar
        image = Image.open(io.BytesIO(await avt.read()))

        def resize(image, neww=300):
            w, h = image.size
            ratio = h/w
            newh = int(neww * ratio)
            resimage = image.resize((neww, newh))
            return resimage

        image = resize(image).convert("1")
        with io.BytesIO() as binary:
            image.save(binary, "PNG")
            binary.seek(0)
            await ctx.send(file=discord.File(fp=binary, filename="blackandwhite.png"))


    @commands.command(aliases=["inverse"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def invert(self, ctx, member: discord.Member = None):
        """ Inverts the colours on a profile picture. """

        if member == None:
            avt = ctx.author.avatar
        else:
            avt = member.avatar
        image = Image.open(io.BytesIO(await avt.read()))

        def resize(image, neww=300):
            w, h = image.size
            ratio = h/w
            newh = int(neww * ratio)
            resimage = image.resize((neww, newh))
            return resimage

        image = ImageOps.invert(resize(image).convert("RGB"))
        with io.BytesIO() as binary:
            image.save(binary, "PNG")
            binary.seek(0)
            await ctx.send(file=discord.File(fp=binary, filename="inverted.png"))


    @commands.command(aliases=["softwaregore"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def glitch(self, ctx, member: discord.Member = None):
        """ Creates a corrupted look on a profile picture. """

        if member == None:
            avt = ctx.author.avatar
        else:
            avt = member.avatar
        image = Image.open(io.BytesIO(await avt.read()))

        def resize(image, neww=300):
            w, h = image.size
            ratio = h/w
            newh = int(neww * ratio)
            resimage = image.resize((neww, newh))
            return resimage

        image = ImageOps.equalize(resize(image).convert("RGB"))
        with io.BytesIO() as binary:
            image.save(binary, "PNG")
            binary.seek(0)
            await ctx.send(file=discord.File(fp=binary, filename="glitched.png"))


    @commands.command(aliases=["border"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def frame(self, ctx, member: discord.Member = None, colour=7500):
        """Creates a border around a profile picture. """

        if member == None:
            avt = ctx.author.avatar
        else:
            avt = member.avatar
        image = Image.open(io.BytesIO(await avt.read()))

        def resize(image, neww=300):
            w, h = image.size
            ratio = h/w
            newh = int(neww * ratio)
            resimage = image.resize((neww, newh))
            return resimage

        image = ImageOps.expand(resize(image).convert("RGB"), border=10, fill=colour)
        with io.BytesIO() as binary:
            image.save(binary, "PNG")
            binary.seek(0)
            await ctx.send(file=discord.File(fp=binary, filename="framed.png"))


    @commands.command(aliases=["post"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def posterize(self, ctx, member: discord.Member = None, bits=2):
        """ Runs a posterizing filter on a profile picture. """

        if member == None:
            avt = ctx.author.avatar
        else:
            avt = member.avatar
        image = Image.open(io.BytesIO(await avt.read()))

        if bits > 8 or bits < 1:
            bits = 1

        def resize(image, neww=300):
            w, h = image.size
            ratio = h/w
            newh = int(neww * ratio)
            resimage = image.resize((neww, newh))
            return resimage

        image = ImageOps.posterize(resize(image).convert("RGB"), bits)
        with io.BytesIO() as binary:
            image.save(binary, "PNG")
            binary.seek(0)
            await ctx.send(file=discord.File(fp=binary, filename="posterized.png"))


    @commands.command(aliases=["solar"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def solarize(self, ctx, member: discord.Member = None, threshold=128):
        """ Runs a solarizing filter on a profile picture. """

        if member == None:
            avt = ctx.author.avatar
        else:
            avt = member.avatar
        image = Image.open(io.BytesIO(await avt.read()))

        def resize(image, neww=300):
            w, h = image.size
            ratio = h/w
            newh = int(neww * ratio)
            resimage = image.resize((neww, newh))
            return resimage

        image = ImageOps.solarize(resize(image).convert("RGB"), threshold)
        with io.BytesIO() as binary:
            image.save(binary, "PNG")
            binary.seek(0)
            await ctx.send(file=discord.File(fp=binary, filename="solarized.png"))


    @commands.command(aliases=["pfp", "avatar"])
    async def profile(self, ctx, member: discord.Member = None):
        """ Displays a user's profile picture. """

        if member == None:
            user = ctx.author
        else:
            user = member
        avatar_as = lambda s: user.avatar.with_format(s) if (s == "gif") == (user.avatar.is_animated()) else None
        embed = discord.Embed(color=user.color)
        embed.add_field(name="_ _", value=f"""[`.webp`]({avatar_as("webp")}) [`.jpeg`]({avatar_as("jpeg")})
[`.jpg `]({avatar_as("jpg")}) [`.png `]({avatar_as("png")})""")
        embed.set_author(name=f"{user.name.upper()}'S PROFILE PICTURE")
        embed.set_image(url=user.avatar)
        await ctx.send(embed=embed)

    
    @commands.command(aliases=["catboys"])
    @commands.is_owner()
    async def catboy(self, ctx):
        """ I'm not gay I swear\n(this command does not work at the moment) """

        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.catboys.com/img") as response:
                info = await response.json()

        embed = discord.Embed(colour=discord.Colour.random())
        embed.set_author(name="catboys owo?")
        embed.set_image(url=info["url"])
        embed.set_footer(text="https://catboys.com/")

        await ctx.send(embed=embed)
    

    @commands.command(aliases=["catgirls"])
    @commands.is_owner()
    async def neko(self, ctx, *, options="neko"):
        """
        Various anime things
        Available options: 
        `smug`, `woof`, `gasm`, `8ball`, `goose`, `cuddle`, `avatar`,
        `slap`, `pat`, `gecg`, `feed`, `fox_girl`, `lizard`, `ngif`,
        `neko`, `hug`, `meow`, `kiss`, `wallpaper`, `tickle`, `spank`
        """

        if options.lower() == "spank" and not ctx.channel.is_nsfw():
            embed = discord.Embed(colour=discord.Colour.random())
            embed.description = "ayayay go find a nsfw channel to use this in jeez"
            await ctx.send(embed=embed)
            return

        if options.lower() not in ("smug", "woof", "gasm", "8ball", "goose", "cuddle", "avatar", 
                        "slap", "pat", "gecg", "feed", "fox_girl", "lizard", "ngif",
                        "neko", "hug", "meow", "kiss", "wallpaper", "tickle", "spank"):
            options = "neko"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://nekos.life/api/v2/img/{options.lower().replace(' ', '_')}") as response:
                info = await response.json()

        embed = discord.Embed(colour=discord.Colour.random())
        embed.set_author(name="N Ë K O O O")
        embed.set_image(url=info["url"])
        embed.set_footer(text="https://nekos.life/")

        await ctx.send(embed=embed)


async def setup(client):
    await client.add_cog(Images(client))
