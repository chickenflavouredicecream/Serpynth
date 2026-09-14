import discord
from discord.ext import commands
from discord.ext import tasks
import io
import os
import time
import urllib.parse
import random
import json
import asyncio
import aiohttp
import asyncpraw as praw
import string
import datetime
from PIL import Image, ImageDraw, ImageFont

#
class Fun(commands.Cog, name="🎢 Fun", description="""
The commands in this category are for fun.
Some commands are minigames, some take funny things from the internet, some
just do random things."""):

    def __init__(self, client):
        self.client = client
        self.reddit = praw.Reddit(client_id=os.environ["REDDIT-ID"],
                        client_secret=os.environ["REDDIT-SECRET"],
                        password=os.environ["REDDIT-PASSWORD"],
                        user_agent=os.environ["REDDIT-AGENT"],
                        username=os.environ["REDDIT-USER"])
        self.conwaybusy = set()
        f = open("gameoflife.json", "r")
        self.golitems = json.load(f)
        f.close()

        f = open("cards.json", "r")
        self.applecards = json.load(f)
        f.close()
        

        self.summons = {
                "turtle": "0🟩🟩🟩🟩🟩0\n🟩00000🟩\n🟩00000🟩\n🟩00000🟩\n🟩00000🟩\n🟩00000🟩\n0🟩🟩🟩🟩🟩0",
                "phoenix": "0000000\n000🟨000\n00🟨🟧🟨00\n0🟨🟧🟥🟧🟨0\n00🟨🟧🟨00\n000🟨000\n0000000",
                "Serpynth": "0000000\n00🟩🟩000\n0🟥🟩🟩000\n00🟩0000\n0🟩00🟩0🟩\n00🟩🟩0🟩0\n0000000",
                "shark": "0000000\n000🟦000\n00🟦⬜🟦00\n00🟦⬜🟦00\n00🟦⬜🟦00\n000🟦000\n0000000",
                "santa": "0000000\n0000000\n00🟩🟥🟩00\n00🟥⬜🟥00\n00🟩🟥🟩00\n0000000\n0000000",
                "zebra": "0000000\n0000000\n00⬜⬛⬜00\n00⬛⬜⬛00\n00⬜⬛⬜00\n0000000\n0000000",
                "yeti": "0000000\n0000000\n00🟦🟦🟦00\n00🟦⬜🟦00\n00🟦🟦🟦00\n0000000\n0000000",
                "blackhole": "0000000\n0000000\n00⬛⬛⬛00\n00⬛⬛⬛00\n00⬛⬛⬛00\n0000000\n0000000",
                "whale": "00🟦0🟦00\n0000000\n🟦00000🟦\n0000000\n🟦00000🟦\n0000000\n00🟦0🟦00",
                "snake": "0000000\n0000000\n0000000\n🟩🟩🟩🟩🟩🟩🟩\n0000000\n0000000\n0000000",
                "eagle": "🟫🟫0⬜0🟫🟫\n0000000\n0000000\n0000000\n0000000\n0000000\n0000000",
                "flower": "0000000\n0000000\n000⬜000\n00⬜🟨⬜00\n000⬜000\n0000000\n0000000",
                "unicorn": "0000000\n0000000\n000🟪000\n00🟪🟪🟪00\n000🟪000\n0000000\n0000000",
                "apple": "0000000\n0000000\n000🟥000\n00🟥🟥🟥00\n000🟥000\n0000000\n0000000",
                "dragon": "🟩00000🟩\n0000000\n0000000\n000🟥000\n0000000\n0000000\n🟩00000🟩",
                "giraffe": "0000000\n000🟨000\n000🟨000\n000🟨000\n000🟨000\n000🟨000\n0000000",
                "tree": "0000000\n000🟫000\n000🟫000\n000🟫000\n000🟫000\n000🟫000\n0000000",
                "kraken": "000🟦000\n0000000\n0000000\n🟦00000🟦\n0000000\n0000000\n000🟦000",
                "polarbear": "0000000\n0000000\n000⬜000\n00⬜0⬜00\n000⬜000\n0000000\n0000000"

        }
        self.summonemojis = {
                "dragon": "🐲",
                "kraken": "🦑",
                "unicorn": "🦄",
                "snake": "🐍",
                "Serpynth": "<:snek:1028410079898259586>",
                "turtle": "🐢",
                "phoenix": "🔥🐦",
                "giraffe": "🦒",
                "tree": "🌳",
                "blackhole": "⚫",
                "zebra": "🦓",
                "whale": "🐳",
                "yeti": "⛄🐒",
                "santa": "🎅",
                "eagle": "🦅",
                "apple": "🍎",
                "shark": "🦈",
                "flower": "🌼",
                "polarbear": "🐻‍❄️"
        }


    @commands.command(aliases=["8ball", "_8ball", "8", "🎱"])
    async def eightball(self, ctx, *, question=None):
        """
        Answers a yes or no question.
        Truthfulness not guaranteed.
        """

        choice = random.choice(("As I see it, yes.", "Ask again later.",
        "Better not tell you now.",
        "Cannot predict now.",
        "Concentrate and ask again.",
        "Don't count on it.",
        "It is certain.",
        "It is decidedly so.",
        "Most likely.",
        "My reply is no.",
        "My sources say no.",
        "Outlook not so good.",
        "Outlook good.",
        "Reply hazy, try again.",
        "Signs point to yes.",
        "Very doubtful.",
        "Without a doubt.",
        "Yes.",
        "Yes - definitely.",
        "You may rely on it."))
        embed = discord.Embed()
        embed.set_author(name="ASK THE ALL-KNOWING 8BALL")
        embed.add_field(name="Question", value=f"`{question}`")
        embed.add_field(name="_ _", value="🎱")
        embed.add_field(name="Answer", value=f"`{choice}`")
        await ctx.send(embed=embed)


    @commands.command(aliases=["sword", "duel"])
    async def swordfight(self, ctx, opponent: discord.Member):
        """
        Swordfight anyone! en garde
        unfortunately doesn't work very well anymore
        """

        op = opponent
        if random.randint(1, 2) == 1:
            p1 = ctx.message.author
            p2 = op
        else:
            p1 = op
            p2 = ctx.message.author
        class player:
            hp = 100
            en = 20
            sh = False
        p1s = player()
        p2s = player()

        play = False
        conf = await ctx.send(f"{op.mention}, react with ☑ if you are ready.\nOtherwise, react with ❎.\nYou have 20 seconds to respond.")
        await conf.add_reaction("☑")
        await conf.add_reaction("❎")
        for x in range(20):
            await asyncio.sleep(1.0)
            getconf = await ctx.channel.fetch_message(conf.id)
            yes = await getconf.reactions[0].users().flatten()
            no = await getconf.reactions[1].users().flatten()
            if op in yes:
                play = True
                break
            elif op in no:
                play = False
                break
        await conf.delete()
        if play == False:
            await ctx.send(f"{op} is either offline or does not want to fight.")
        else:

            foo = await ctx.send("Both players must react with 🟩 to signalize that they are ready.")
            p1m = await ctx.send(f"**PLAYER ONE: {p1.mention}**\nHP: `{p1s.hp}/100`\nEnergy: `{p1s.en}/20`")
            await ctx.send("**-----------------------------**")
            p2m = await ctx.send(f"**PLAYER TWO: {p2.mention}**\nHP: `{p2s.hp}/100`\nEnergy: `{p2s.en}/20`")
            await p1m.add_reaction("🟩")
            await p2m.add_reaction("🟩")
            itstats = await ctx.send("""**-----------------------------**
⚔ = 5 - 15 damage, -2 energy
🗡 = 0 or 20 damage, -4 energy
🛡 = Blocks next attack, -3 energy
🩹 = Heals 5, +1 energy
⚡ = +5 energy""")
            getp1m = await ctx.channel.fetch_message(p1m.id)
            getp2m = await ctx.channel.fetch_message(p2m.id)
            while True:
                p1bgn = await getp1m.reactions[0].users().flatten()
                p2bgn = await getp2m.reactions[0].users().flatten()
                if p1 in p1bgn and p2 in p2bgn:
                    await getp1m.clear_reaction("🟩")
                    await getp2m.clear_reaction("🟩")
                    break

            await foo.delete()
            await itstats.edit(content="BATTLE WILL START AS SOON AS THIS MESSAGE IS DELETED")
            await p1m.add_reaction("⚔")
            await p1m.add_reaction("🗡")
            await p1m.add_reaction("🛡")
            await p1m.add_reaction("🩹")
            await p1m.add_reaction("⚡")
            await p2m.add_reaction("⚔")
            await p2m.add_reaction("🗡")
            await p2m.add_reaction("🛡")
            await p2m.add_reaction("🩹")
            await p2m.add_reaction("⚡")
            await itstats.delete()

            while True:
                getp1m = await ctx.channel.fetch_message(p1m.id)
                getp2m = await ctx.channel.fetch_message(p2m.id)
                p1p0 = await getp1m.reactions[0].users().flatten()
                p1p1 = await getp1m.reactions[1].users().flatten()
                p1p2 = await getp1m.reactions[2].users().flatten()
                p1p3 = await getp1m.reactions[3].users().flatten()
                p1p4 = await getp1m.reactions[4].users().flatten()
                p2p0 = await getp2m.reactions[0].users().flatten()
                p2p1 = await getp2m.reactions[1].users().flatten()
                p2p2 = await getp2m.reactions[2].users().flatten()
                p2p3 = await getp2m.reactions[3].users().flatten()
                p2p4 = await getp2m.reactions[4].users().flatten()

                if p1 in p1p0 and p1s.en > 1:
                    if p2s.sh == False:
                        p2s.hp -= random.randint(5, 15)
                    p2s.sh = False
                    p1s.en -= 2
                if p2 in p2p0 and p2s.en > 1:
                    if p1s.sh == False:
                        p1s.hp -= random.randint(5, 15)
                    p1s.sh = False
                    p2s.en -= 2
                if p1 in p1p1 and p1s.en > 3:
                    if p2s.sh == False:
                        p2s.hp -= random.choice((0, 20))
                    p2s.sh = False
                    p1s.en -= 4
                if p2 in p2p1 and p2s.en > 3:
                    if p1s.sh == False:
                        p1s.hp -= random.choice((0, 20))
                    p1s.sh = False
                    p2s.en -= 4
                if p1 in p1p2 and p1s.en > 2:
                    p1s.sh = True
                    p1s.en -= 3
                if p2 in p2p2 and p2s.en > 2:
                    p2s.sh = True
                    p2s.en -= 3
                if p1 in p1p3:
                    p1s.hp += 5
                    p1s.en += 1
                if p2 in p2p3:
                    p2s.hp += 5
                    p2s.en += 1
                if p1 in p1p4:
                    p1s.en += 5
                if p2 in p2p4:
                    p2s.en += 5
                await p1m.edit(content=f"**PLAYER ONE: {p1.mention}**\nHP: `{p1s.hp}/100`\nEnergy: `{p1s.en}/20`")
                await p2m.edit(content=f"**PLAYER TWO: {p2.mention}**\nHP: `{p2s.hp}/100`\nEnergy: `{p2s.en}/20`")
                await getp1m.remove_reaction("⚔", p1)
                await getp1m.remove_reaction("🗡", p1)
                await getp1m.remove_reaction("🛡", p1)
                await getp1m.remove_reaction("🩹", p1)
                await getp1m.remove_reaction("⚡", p1)
                await getp1m.remove_reaction("⚔", p1)
                await getp2m.remove_reaction("⚔", p2)
                await getp2m.remove_reaction("🗡", p2)
                await getp2m.remove_reaction("🛡", p2)
                await getp2m.remove_reaction("🩹", p2)
                await getp2m.remove_reaction("⚡", p2)
                await getp2m.remove_reaction("⚔", p2)
                if p1s.hp < 1:
                    await ctx.send(f"**-----------------------------**\n**{p2.mention} is the winner!**")
                    break
                elif p2s.hp < 1:
                    await ctx.send(f"**-----------------------------**\n**{p1.mention} is the winner!**")
                    break


    @commands.command(aliases=["fax", "ff", "funfacts", "fact", "funfact"])
    async def facts(self, ctx):
        """ Generates a random fun fact (funness not guaranteed) """

        file = open("facts.txt")
        facts = file.read().split("\n")
        file.close()

        fact = random.choice(facts)
        while len(fact) > 256:
            fact = random.choice(facts)
        await ctx.send(embed=discord.Embed(title=fact, color=random.randint(0, 16777215)))


    @commands.command(aliases=["hangmen", "hm"])
    async def hangman(self, ctx):
        """
        The rope has been hung around their neck.
        A flick of the lever will drop them down.
        Sentenced to a crime they didn't commit;
        Only your vocabulary can save them now.
        """

        words = open("10000words.txt")
        dict = []
        for line in words:
            for word in line.split():
                dict.append(word)
        words.close()

        word = ""
        wrong = []
        letters = []
        letters += string.ascii_lowercase
        attempts = 0
        tlwrong = 0
        while len(word) < 5 or len(word) > 9:
            word = random.choice(dict)
        letts = []
        for asd in word:
            letts.append("\_")
        find = []
        for asd in word:
            find.append(False)
        msg = await ctx.send(f"""**{ctx.message.author.mention}'s HANGMAN**

        {' '.join(letts)}

        Wrong letters: ```prolog
{' '.join(wrong).upper()} ```

_ _
    """)
        run = True
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel and m.content.lower() in letters
        while run:
            try:
                m = await self.client.wait_for("message", check=check, timeout=60.0)
            except asyncio.TimeoutError:
                await ctx.send("Hangman ended automatically due to 1-minute timeout")
                run = False
                break
            else:
                guess = m.content.lower()
                await m.delete()
                if guess in word:
                    if not guess in letts:
                        indx = 0
                        for letter in word:
                            if guess == letter:
                                find[indx] = True
                            else:
                                find[indx] = False
                            indx += 1
                        indx = 0
                        for item in find:
                            if item == True:
                                letts[indx] = word[indx]
                            indx += 1
                        attempts += 1
                elif not guess in wrong:
                    wrong.append(guess)
                    attempts += 1
                    tlwrong += 1

                await msg.edit(content = f"""**{ctx.message.author.mention}'S HANGMAN**

        {" ".join(letts)}

        Wrong letters: ```prolog
{" ".join(wrong).upper()} ```
        Attempts: `{attempts}`
        Wrong attempts: `{tlwrong}`""")

                if not "\_" in letts:
                    run = False
        await ctx.send(f"_ _\n**GG**\nThe word was: `{word}`\nTotal attempts: `{attempts}`\nTotal wrong attempts: `{tlwrong}`")


    @commands.command(aliases=["quizzes"])
    @commands.cooldown(5, 20, commands.BucketType.user)
    async def quiz(self, ctx, quiztype="none"):
        """ Test your math AND your typing skills! """

        wrong = False
        score = 0
        timelimit = 30
    # add quiz
        if quiztype == "+":
            while not wrong:
                x = random.randint(1, 100)
                y = random.randint(1, 100)
                await ctx.send(f"{x} + {y} \nTime limit: {timelimit}")
                def check(m):
                    return m.content == str(x + y) and m.channel == ctx.message.channel and m.author == ctx.message.author
                try:
                    msg = await self.client.wait_for("message", timeout=timelimit, check=check)
                except asyncio.TimeoutError:
                    wrong = True
                    await ctx.send(f"Time's up! Final score: {score}")
                else:
                    score += 1
                    timelimit = round(timelimit * 3/4)
    # multiply quiz
        elif quiztype == "*":
            while not wrong:
                x = random.randint(2, 12)
                y = random.randint(2, 12)
                await ctx.send(f"{x} * {y} \nTime limit: {timelimit}")
                def check(m):
                    return m.content == str(x * y) and m.channel == ctx.message.channel and m.author == ctx.message.author
                try:
                    msg = await self.client.wait_for("message", timeout=timelimit, check=check)
                except asyncio.TimeoutError:
                    wrong = True
                    await ctx.send(f"Time's up! Final score: {score}")
                else:
                    score += 1
                    timelimit = round(timelimit * 2/3)
    # subtract quiz
        elif quiztype == "-":
            while not wrong:
                x = random.randint(1, 100)
                y = random.randint(1, x)
                await ctx.send(f"{x} - {y} \nTime limit: {timelimit}")
                def check(m):
                    return m.content == str(x - y) and m.channel == ctx.message.channel and m.author == ctx.message.author
                try:
                    msg = await self.client.wait_for("message", timeout=timelimit, check=check)
                except asyncio.TimeoutError:
                    wrong = True
                    await ctx.send(f"Time's up! \nFinal score: {score}")
                else:
                    score += 1
                    timelimit = round(timelimit * 3/4)
    # typing quiz
        elif quiztype == "abc":
            while not wrong:
                phrase = ""
                letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
                "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w",
                "x", "y", "z"]
                for foo in range(random.randint(4, 8)):
                    phrase = phrase + random.choice(letters)
                snd = []
                snd += phrase
                snd = "\u200b".join(snd)
                await ctx.send(f"Type `{snd}` \nTime limit: {timelimit}")
                def check(m):
                    return m.content == str(phrase) and m.channel == ctx.message.channel and m.author == ctx.message.author
                try:
                    msg = await self.client.wait_for("message", timeout=timelimit, check=check)
                except asyncio.TimeoutError:
                    wrong = True
                    await ctx.send(f"Time's up! Final score: {score}")
                else:
                    score += 1
                    timelimit = round(timelimit * 4/5)
        else:
            await ctx.send("Invalid quiz type: Try using `syquiz +`, `syquiz -`, `syquiz *` or `syquiz abc`")


    @commands.command(name="reddit", aliases=["r/", "red"])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def red(self, ctx, subreddit="all", sort="random", *, limit=" "):
        """
        Literally just Reddit.
        But in Discord.
        instantly 8x better
        """

        embed = discord.Embed(colour=0xff4500)
        send = None
        redicon = "https://cdn3.iconfinder.com/data/icons/2018-social-media-logotypes/1000/2018_social_media_popular_app_logo_reddit-512.png"
        if subreddit == "h":
            send = f"""**`syreddit` MINI-TUTORIAL**

__Command usages__
`syreddit` `<subreddit>` (to get random posts from any sorting)
`syreddit` `<subreddit>` `<sorting (hot, new, top, etc.)>` `<limit (number)>`
`syreddit` `<subreddit>` `search` `<query>`
`syreddit` `post` `<id>`

`<subreddit>` - Select a subreddit of your choice to retrieve posts from. Select multiple subreddits using + (e.g., syreddit comedyhell+comedyheaven)
`<sorting>` - Select a sorting. For example, top would return more upvoted posts and new would return newer posts.
`<limit>` - Select a limit of posts to collect. A higher limit would give more diverse results but would take longer. Default is 100, limit is 1000
`<query>` - Search for a particular topic or query from a subreddit.
`<id>` - The ID of a post.

__Examples__
`syreddit memes hot`
`syreddit askreddit search doctor`
`syreddit all top 1000`
`syreddit discordapp`
"""

        elif subreddit == "post":
            submission = await self.reddit.submission(sort.lower())
            try:
                submission.name
            except:
                send = "This ID is not valid!"
            else:
                titl = []
                titl += submission.title
                dotdotdot = False
                while len(titl) > 252:
                    titl.pop(len(titl) - 1)
                    dotdotdot = True
                titl = "".join(titl)
                if dotdotdot:
                    titl += "..."

        elif sort == "random":
            try:
                submission = await self.reddit.subreddit(subreddit)
                submission = await submission.random()
            except:
                await ctx.invoke(self.red, subreddit=subreddit, sort="hot", limit="100")
                return
            else:
                if submission == None:
                    await ctx.invoke(self.red, subreddit=subreddit, sort="hot", limit="100")
                    return
                elif submission != "search":
                    titl = []
                    titl += submission.title
                    dotdotdot = False
                    while len(titl) > 252:
                        titl.pop(len(titl) - 1)
                        dotdotdot = True
                    titl = "".join(titl)
                    if dotdotdot:
                        titl += "..."
                else:
                    send = f"Subreddit `r/{subreddit}` not found"


        elif sort in ("search", "s", "find"):
            try:
                sbrdt = await self.reddit.subreddit(subreddit)
                await sbrdt.load()
                submission = sbrdt.search(str(limit))
                submissions = []
                async for sbm in submission:
                    submissions.append(sbm)
                submission = random.choice(submissions)
            except:
                send = f"Posts from `r/{subreddit}` search `{limit}` not found"
            else:
                titl = []
                titl += submission.title
                dotdotdot = False
                while len(titl) > 252:
                    titl.pop(len(titl) - 1)
                    dotdotdot = True
                titl = "".join(titl)
                if dotdotdot:
                    titl += "..."

        else:
            if limit == " ":
                limit = "100"

            if not limit.isdigit():
                send = f"`{limit}` is not a valid positive integer less than 1000."
            elif int(limit) < 5 and sort == "hot":
                send = "Sorting by hot has a minimum limit of 5."


            elif int(limit) < 1001 and int(limit) > 0:
                try:
                    sbrdt = await self.reddit.subreddit(subreddit)
                    submission = eval(f"sbrdt.{sort}(limit={int(limit)})")
                    submissions = []
                    async for sbm in submission:
                        submissions.append(sbm)
                    submission = random.choice(submissions)
                except Exception as e:
                    send = f"Posts from `r/{subreddit}` sorting `{sort}` not found"
                else:
                    if submission != "search":
                        titl = []
                        titl += submission.title
                        dotdotdot = False
                        while len(titl) > 252:
                            titl.pop(len(titl) - 1)
                            dotdotdot = True
                        titl = "".join(titl)
                        if dotdotdot:
                            titl += "..."
            else:
                send = f"Make sure that your limit is a valid positive integer less than 1000."

        if type(send) == str:
            await ctx.send(content=send)
        else:
            await submission.subreddit.load()
            if submission.over_18:
                if ctx.message.channel.is_nsfw():
                    if submission.selftext != "" and len(submission.selftext) < 2048:
                        embed.set_author(name=f"[NSFW]\n{titl}",
                                        url=f"https://redd.it/{submission.id}",
                                        icon_url=redicon)
                        embed.description = f"||{submission.selftext}||"
                        embed.add_field(name=f"{submission.url}", value="_ _")
                        embed.set_image(url=submission.url)
                        send = embed
                    else:
                        embed.set_author(name=f"[NSFW]\n{titl}",
                                        url=f"https://redd.it/{submission.id}",
                                        icon_url=redicon)
                        embed.add_field(name=f"{submission.url}", value="_ _")
                        embed.set_image(url=submission.url)
                        send = embed
                else:
                    if submission.subreddit.over18:
                        await ctx.send(f"`r/{submission.subreddit}` is NSFW")
                    else:
                        await ctx.send(f"The post that was found is NSFW, try again")
                    return
            else:
                if submission.selftext != "" and len(submission.selftext) < 2048:
                    embed.set_author(name=titl,
                                    url=f"https://redd.it/{submission.id}",
                                    icon_url=redicon)
                    embed.description = submission.selftext
                    embed.add_field(name=f"{submission.url}", value="_ _")
                    embed.set_image(url=submission.url)
                    send = embed
                else:
                    embed.set_author(name=titl,
                                    url=f"https://redd.it/{submission.id}",
                                    icon_url=redicon)
                    embed.add_field(name=f"{submission.url}", value="_ _")
                    embed.set_image(url=submission.url)
                    send = embed

            if submission.author != None:
                embed.add_field(name="_ _",
                    value = f"""
[u/{submission.author.name}✍](https://www.reddit.com/u/{submission.author.name})

[r/{submission.subreddit.display_name}](https://www.reddit.com/r/{submission.subreddit.display_name})
{"{:,}".format(submission.subreddit.subscribers)}👤

[{submission.id}](https://redd.it/{submission.id})""",
                    inline=False)
            else:
                embed.add_field(name="_ _",
                    value = f"""
[r/{submission.subreddit.display_name}](https://www.reddit.com/r/{submission.subreddit.display_name})
{"{:,}".format(submission.subreddit.subscribers)}👤

[{submission.id}](https://redd.it/{submission.id})""",
                    inline=False)
            embed.timestamp = datetime.datetime.fromtimestamp(submission.created_utc)
            embed.set_footer(text=f"[{'{:,}'.format(submission.score)}👍]  [{'{:,}'.format(submission.num_comments)}💬]")

            if "gfycat.com/" in send.fields[0].name or send.fields[0].name.endswith(".gifv"):
                embed.set_image(url=None)
                await ctx.send(content=f"Use `syreddit h` for help with this command." if subreddit == \
                                        "all" and random.randint(1, 3) < 2 else "",
                                embed=send)
                await ctx.send(send.fields[0].name)
            elif "youtube.com/" in send.fields[0].name or "youtu.be/" in send.fields[0].name:
                embed.set_image(url=None)
                await ctx.send(content=f"Use `syreddit h` for help with this command." if subreddit == \
                                        "all"and random.randint(1, 3) == 1 else "",
                                embed=send)
                await ctx.send(send.fields[0].name)
            else:
                correcttype = False
                for i in (".jpg", ".png", ".jpeg", ".gif"):
                    if i in send.fields[0].name.lower():
                        correcttype = True
                if correcttype == False:
                    embed.set_image(url=None)
                await ctx.send(content=f"`syreddit h` for help with this command." if subreddit == \
                                        "all" and random.randint(1, 3) == 1 else "",
                                embed=send)


    @commands.command(aliases=["rockpaperscissors", "roshambo"])
    async def rps(self, ctx, *, choice):
        """
        Play rock-paper-scissors against the bot!
        (definitely not rigged)
        """

        botchoice = random.choice(["rock", "paper", "scissors"])
        if choice.lower() not in ("rock", "paper", "scissors"):
            await ctx.send(f"`{choice}` is not an option, use \"rock\", \"paper\" or \"scissors\".")
            return
        out = {"rock":
            {"rock": "Tie!", "paper": "Bot wins!", "scissors": "You win!"},
            "paper":
                {"rock": "You win!", "paper": "Tie", "scissors": "Bot wins!"},
            "scissors":
                {"rock": "Bot wins!", "paper": "You win!", "scissors": "Tie!"},
            }
        await ctx.send(f"Your choice: `{choice.lower()}`\nBot choice: `{botchoice}`\n**{out[choice.lower()][botchoice]}**")


    @commands.command(aliases=["fight", "tb"])
    async def battle(self, ctx, opponent: discord.Member):
        """ A fight to the death! Just kidding. """

        await ctx.send(f"{opponent.mention}, are you willing to fight {ctx.message.author.mention}? (y/n)")

        def cfrm(m):
            return m.author == opponent and m.channel == ctx.channel and m.content.lower() in ("y", "n")
        def p1mv(m):
            return m.author == p1 and m.channel == ctx.channel and m.content.lower() in ("s", "d", "h")
        def p2mv(m):
            return m.author == p2 and m.channel == ctx.channel and m.content.lower() in ("s", "d", "h")
        try:
            m = await self.client.wait_for("message", check=cfrm, timeout=30.0)
        except asyncio.TimeoutError:
            await ctx.send(f"{opponent} is either offline or does not want to fight right now.")
        else:
            if m.content.lower() == "n":
                await ctx.send(f"{opponent} does not want to fight right now.")
            else:

                if random.randint(1, 2) == 1:
                    p1 = ctx.message.author
                    p2 = opponent
                else:
                    p1 = opponent
                    p2 = ctx.message.author

                turn = True
                run = True
                p1hp = 100
                p2hp = 100

                while run:
                    if turn:
                        await ctx.send(f"**{p1.mention}'S TURN**\nWhat would you like to do?\ns = Attack 15-25 dmg\n" + \
                        f"d = 50% chance of 0 dmg or 40dmg\nh = Heals 15-25 hp\n\nYour HP: `{p1hp}`")
                        m = await self.client.wait_for("message", check=p1mv)
                        if m.content.lower() == "s":
                            dmg = random.randint(15, 25)
                            p2hp -= dmg
                            await ctx.send(f"{p1.mention} did `{dmg}` damage towards {p2.mention}, leaving them with `{p2hp}HP`!")
                        elif m.content.lower() == "d":
                            dmg = random.choice((0, 40))
                            p2hp -= dmg
                            await ctx.send(f"{p1.mention} did `{dmg}` damage towards {p2.mention}, leaving them with `{p2hp}HP`!")
                        elif m.content.lower() == "h":
                            h = random.randint(15, 25)
                            p1hp += h
                            await ctx.send(f"{p1.mention} healed themselves for `{h}`HP, raising their HP up to `{p1hp}`!")
                    else:
                        await ctx.send(f"**{p2.mention}'S TURN**\nWhat would you like to do?\ns = Attack 15-25 dmg\n" + \
                        f"d = 50% chance of 0 dmg or 40dmg\nh = Heals 15-25 hp\n\nYour HP: `{p2hp}`")
                        m = await self.client.wait_for("message", check=p2mv)
                        if m.content.lower() == "s":
                            dmg = random.randint(15, 25)
                            p1hp -= dmg
                            await ctx.send(f"{p2.mention} did `{dmg}` damage towards {p1.mention}, leaving them with `{p1hp}HP`!")
                        elif m.content.lower() == "d":
                            dmg = random.choice((0, 40))
                            p1hp -= dmg
                            await ctx.send(f"{p2.mention} did `{dmg}` damage towards {p1.mention}, leaving them with `{p1hp}HP`!")
                        elif m.content.lower() == "h":
                            h = random.randint(15, 25)
                            p2hp += h
                            await ctx.send(f"{p2.mention} healed themselves for `{h}`HP, raising their HP up to `{p2hp}`!")
                    turn = not turn
                    if p1hp < 1:
                        await ctx.send(f"**{p2.mention} is the winner!**")
                        run = False
                        break
                    elif p2hp < 1:
                        await ctx.send(f"**{p1.mention} is the winner!**")
                        run = False
                        break


    @commands.command(aliases=["books", "book", "ook", "ooks", "shelf", "bs"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def bookshelf(self, ctx, *, title=""):
        """ Serpynth's collection of classic books, right at your fingertips """

        doc = open("books.txt", "r")
        read = doc.read()
        list = read.split('\n')
        random.shuffle(list)
        doc.close()
        found = []
        amount = 0
        for i in list:
            if title.lower() in i.lower():
                found.append(i.replace("â€™", "'"))
                amount += 1
                if amount > 23:
                    break
        embed = discord.Embed(color=random.randint(0, 16777215))
        embed.set_author(name=f"BOOKS {random.choice(('📕', '📗', '📘', '📙'))}")
        for i in found:
            url = "https://snewd.com/ebooks/" + \
            i.split(" | ")[0].replace(" ", "-").replace("'", "").replace(":", "").replace("?", "").replace(".", "").lower()
            embed.add_field(name=i, value=f"[Download]({url})")
        embed.add_field(name="".join(["\_" for ij in range(15)]), value="**[More Books](https://snewd.com/ebooks/)**", inline=False)
        embed.set_footer(text=f"{amount}{'+' if amount > 23 else ''} book{'' if amount == 1 else 's'} found")
        await ctx.send(embed=embed)


    @commands.command(aliases=["lib", "openlibrary"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def library(self, ctx, *, book):
        """ Serpynth's local [public library](https://openlibrary.org/), right at your fingertips """

        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://openlibrary.org/search.json?q={urllib.parse.quote_plus(book)}") as j:
                book = await j.json()

        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://openlibrary.org{book['docs'][0]['key']}.json") as j:
                info = await j.json()

        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://openlibrary.org{info['authors'][0]['author']['key']}.json") as j:
                author_info = await j.json()

        title = info['title']
        words = title.split(" ")
        for i, word in enumerate(words):
            words[i] = word.capitalize()
        title = " ".join(words)

        if type(info.get("description")) == str:
            desc = info["description"]
        elif info.get("description") == None:
            desc = "*No available description*"
        else:
            desc = info["description"]["value"]
        if len(desc) > 1024:
            desc = desc[:1021]
            desc += "..."

        embed = discord.Embed(color=random.randint(0, 16777215))
        embed.set_author(name=f"LIBRARY {random.choice(('📕', '📗', '📘', '📙'))}")
        embed.add_field(name="Description", value=desc, inline=False)
        embed.add_field(name="Author",
                        value=f"[{author_info['name']}](https://openlibrary.org{info['authors'][0]['author']['key']})",
                        inline=False)
        embed.add_field(name=f"{title}", value=f"[Read](https://openlibrary.org{book['docs'][0]['key']} '{title}')")
        embed.set_footer(text="https://openlibrary.org/")
        await ctx.send(embed=embed)


    @commands.command(aliases=["ascitxt", "asciiitxt", "asciitxt", "ascitext"])
    async def asciitext(self, ctx, *, text="Hello!"):
        """ Instantly creates ASCII text art! """

        font = ImageFont.truetype("arialbd.ttf", 15)
        size = font.getsize(text)
        image = Image.new("1", size, 1)
        draw = ImageDraw.Draw(image)
        draw.text((0, 0), text, font=font)
        send = ""
        for rownum in range(size[1]):
            line = []
            for colnum in range(size[0]):
                if image.getpixel((colnum, rownum)):
                    line.append(" "),
                else:
                    line.append("▄"), # ▄
            cont = False
            if "▄" in line:
                cont = True
            if cont:
                send += " ".join(line) + "\n"
        await ctx.send(f'```\n{send}```')


    @commands.command(aliases=["hax", "hacker", "hacks"])
    async def hack(self, ctx, member: discord.Member):
        """
        This command will ||hack|| someone's account!
        Serpynth is not liable for any damages.
        """

        async def asdasd():
            await m.edit(content="\n".join(msg))
            await asyncio.sleep(random.randint(4, 5) + random.random())

        if member.bot:
            emt = """⬛
⬛
⬛
⬛
⬛
⬛
⬛
⬛
⬛
⬛
⬛"""
            m = await ctx.send(f"🟨 Collecting data from {member}...\n{emt}")
            await asyncio.sleep(random.randint(2, 4) + random.random())
            await m.edit(content=f"🟥 An unexpected error occured: `IdentityError: {member} is a bot`\n{emt}")
            return

        msg = [f"🟨 Collecting data from {member}...", "⬛", "⬛", "⬛", "⬛", "⬛", "⬛", "⬛", "⬛", "⬛", "⬛", "⬛"]
        chars = [".", "_", "-"]
        chars += string.ascii_letters
        chars += string.digits
        m = await ctx.send("\n".join(msg))
        await asyncio.sleep(random.randint(4, 5) + random.random())
        msg[0] = "🟩 Collected data"
        if member == ctx.author:
            msg[0] += "\n🟥 `WARNING: You are hacking yourself!`"
        msg[1] = "🟨 Looking for token..."
        await asdasd()
        msg[1] = f"🟩 Found token: `N{''.join([random.choice(chars) for i in range(58)])}`"
        msg[2] = "🟨 Extracting password..."
        await asdasd()
        msg[2] = f"🟨 Logging in to {member}'s account..."
        await asdasd()
        await asyncio.sleep(2.0)
        try:
            hook = await ctx.channel.create_webhook(name="Serpynth Temporary")
            assert random.randint(1, 4) < 4
            await hook.send(content="_ _", username=member.nick if member.nick else member.name, avatar_url=member.avatar_url)
        except:
            msg[2] = f"🟥 An unexpected error occured: `LoginError: password failed (hack.exe, line {random.randint(500, 1300)})`"
        else:
            msg[2] = f"🟩 Login successful"
        try:
            await hook.delete(reason="Serpynth Temporary")
        except:
            pass
        msg[3] = f"🟨 Collecting {member}'s IP address..."
        await asdasd()
        await asyncio.sleep(0.5)
        msg[3] = f"🟩 Found IP address: `{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}`"
        msg[4] = f"🟨 Collecting credit card info..."
        await asdasd()
        if random.randint(1, 3) == 1:
            msg[4] = f"🟥 `WARNING: Credit card not found`"
        else:
            num = " ".join(["".join([str(random.randint(0, 9)) for i in range(4)]) for i in range(4)])
            msg[4] = f"🟩 Collected credit card info; card number: `{num}`"
        msg[5] = f"🟨 Accessing {member}'s files..."
        await asdasd()
        msg[5] = f"🟩 Accessed {member}'s files"
        r1 = random.randint(1, 2)
        r2 = random.randint(3, 8)
        r3 = random.randint(6, 19)
        msg[6] = f"🟨 Installing `slithyr_webdriver-{r1}.{r2}.{r3}-x64.exe` (26.57 MB)..."
        await asdasd()
        await asyncio.sleep(6.0)
        msg[6] = f"🟩 Installed `slithyr_webdriver-{r1}.{r2}.{r3}-x64.exe` in `c:\\program files\\`"
        msg[7] = f"🟨 Running file..."
        await asdasd()
        await asyncio.sleep(3.0)
        msg[7] = "🟩 Accessed browser; return message `200 OK`"
        msg[8] = "🟨 Switching default browser..."
        await asdasd()
        if random.randint(1, 3) == 1:
            msg[8] = f"🟥 An unexpected error occured: `KeyError: unknown browser '������' (hack.exe, line {random.randint(700, 1300)})`"
        else:
            msg[8] = f"🟩 Switched {member}'s default search engine to `{random.choice(('Yahoo', 'Bing'))}`"
        msg[9] = "🟨 Modifying hardware..."
        await asdasd()
        msg[9] = f"🟨 Heating CPU..."
        msg[10] = "🟨 Setting up `slithyr_virus`..."
        await asdasd()
        msg[10] = "🟩 Completed `slithyr_virus` setup"
        await asdasd()
        msg[9] = f"🟩 CPU has reached `{random.randint(65, 80)}°C`"
        msg[11] = "🟨 Cleaning up..."
        await m.edit(content="\n".join(msg))
        await asyncio.sleep(random.randint(2, 3) + random.random())
        msg[11] = f"✅ Successfully hacked {member}"
        await m.edit(content="\n".join(msg))


    @commands.command(aliases=["gol", "conwaysgameoflife", "cellularautomaton", "life"])
    @commands.cooldown(1, 25, commands.BucketType.user)
    async def gameoflife(self, ctx):
        """
        A zero-player game. Nobody is allowed to play.
        A cellular automaton. Limited to 100 generations, to prevent destabilization.
        """

        if ctx.channel.id in self.conwaybusy:
            await ctx.send("This command is already being used in this channel, try again later or in a different channel.")
            return

        embed = discord.Embed(colour=0x2ecc71)
        embed.set_author(name="What will be your starting configuration?")
        embed.description = """Send it in a multi-line code block (text surrounded with "\`\`\`"),
where `0` = dead and `1` = alive.

For example,
\`\`\`00000000000000
00000000000000
00000000000000
00000000000000
00000010000000
00000001000000
00000111000000
00000000000000
00000000000000
00000000000000\`\`\`"""
        embed.add_field(name="_ _", value="""Width must be less than 25, height must be less than 41.
Widths greater than 18 may not appear properly on mobile devices.
Type `cancel` to cancel.

For any generation,
- a dead cell with exactly 3 neighbours will become alive.
- an alive cell with more than 3 or less than 2 neighbours will die.
- an alive cell with either 2 or 3 neighbours stays alive.

**Use `sygameoflifeguide` for more help.**""")

        await ctx.send(embed=embed)

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        m = await self.client.wait_for("message", check=check)

        if m.content.lower() in ("cancel", "stop", "quit", "exit"):
            await ctx.send("Command has been cancelled.")
            return

        for i in m.content:
            if i not in ("", "\n", " ", "0", "1", "⬜", "⬛", "`"):
                await ctx.send("This is not the correct format!")
                return

        m = m.content.replace(" ", "").replace("```", "").replace("⬜", "1").replace("⬛", "0")

        grid = []
        for i, j in enumerate(m.split("\n")):
            grid.append([])
            grid[i] += j
            grid[i] = list(map(int, grid[i]))
        # grid.pop(0)

        freezegrid = grid[:]
        for i in freezegrid:
            if len(i) < 1:
                grid.remove(i)

        w = 0
        for i in grid:
            if len(i) > w:
                w = len(i)
        if w < 10:
            w = 10
        h = len(grid)
        if h < 10:
            h = 10

        if w > 24 or h > 40:
            await ctx.send("Your starting configuration is too large!")
            return

        while len(grid) < 10:
            grid.append([0 for i in range(w)])

        for i in grid:
            while len(i) < w:
                i.append(0)

        # grid = [[0 for i in range(w)] for i in range(h)]
        def emojify(i):
            convert = {0: "⬛", 1: "⬜"}
            return convert[i]

        gridmap = "\n".join(["".join(list(map(emojify, i))) for i in grid])

        embed = discord.Embed(colour=0xf1c40f)
        embed.set_author(name="CONWAY'S GAME OF LIFE")
        embed.add_field(name="_ _", value=f"```{gridmap}```", inline=False)
        embed.set_footer(text="Generation 1/100")
        m = await ctx.send(embed=embed)
        await m.add_reaction('⏹')

        def surroundings(y, x):
            count = 0
            surrtiles = ((-1, 0), (-1, 1), (0, 1), (1, 1),
                        (1, 0), (1, -1), (0, -1), (-1, -1))
            for i in surrtiles:
                row = y
                column = x
                if row > (h - 2) and i[0] > 0:
                    row = -1
                if column > (w - 2) and i[1] > 0:
                    column = -1
                if row < 1 and i[0] < 0:
                    row = h
                if column < 1 and i[1] < 0:
                    column = w
                if grid[row + i[0]][column + i[1]] == 1:
                    count += 1
            return count

        def check(reaction, user):
            return reaction.emoji == "⏹" and user == ctx.author and reaction.message == m

        self.conwaybusy.add(ctx.channel.id)

        gen = 1
        while True:
            gen += 1
            try:
                reaction, user = await self.client.wait_for("reaction_add", check=check, timeout=1.0)
            except asyncio.TimeoutError:
                pass
            else:
                embed.colour = 0x33cc66
                await m.edit(embed=embed)
                break

            nextgrid = [i[:] for i in grid]
            for y, row in enumerate(grid):
                for x, column in enumerate(row):
                    if surroundings(y, x) == 3:
                        nextgrid[y][x] = 1
                    if surroundings(y, x) > 3:
                        nextgrid[y][x] = 0
                    if surroundings(y, x) < 2:
                        nextgrid[y][x] = 0
            # == 3 alive, > 3 dead, < 2 dead
            gridmap = "\n".join(["".join(list(map(emojify, i))) for i in nextgrid])
            embed = discord.Embed(colour=0xf1c40f)
            embed.set_author(name="CONWAY'S GAME OF LIFE")
            embed.add_field(name="_ _", value=f"```{gridmap}```", inline=False)
            embed.set_footer(text=f"Generation {gen}/100")
            await m.edit(embed=embed)

            if nextgrid == grid or gen > 99:
                embed.colour = 0x33cc66
                await m.edit(embed=embed)
                break
            else:
                grid = [i[:] for i in nextgrid]

        self.conwaybusy.remove(ctx.channel.id)


    @commands.command(aliases=["golguide", "lifeguide", "lifehelp", "lg"])
    @commands.cooldown(5, 5, commands.BucketType.user)
    async def gameoflifeguide(self, ctx, *, item=""):
        """ Various cool patterns to try out using `sygameoflife`. """

        embed = discord.Embed(colour=0xf1c40f)
        embed.set_author(name="GUIDE TO CONWAY'S GAME OF LIFE")
        if item.lower() in self.golitems:
            if item.lower() not in ("lwss", "mwss", "hwss", "37p4h1v0", "30p5h2v0", "25p3h1v0.1", "31p8h4v0"):
                name = f"__{' '.join([word.capitalize() for word in item.lower().split()])}__"
            else:
                name = f"__{item.upper()}__"

            if item.lower() in ("nothing", "void"):
                self.golitems["void"]["conf"] = "\n".join(["".join(["0" for i in range(24)]) for j in range(40)])
            if item.lower() == "soup":
                self.golitems[item]["conf"] = "\n".join(["".join([random.choice(["0", "1"]) for i in range(24)]) for j in range(40)])

            embed.add_field(name=name,
                            value=f"```{self.golitems[item]['conf'].replace('0', '⬛').replace('1', '⬜')}```", inline=False)
            embed.add_field(name="__Type__", value=self.golitems[item]["type"].capitalize())
            if item.lower() not in ("zebra stripes", "venetian blinds", "squaredance", "soup"):
                embed.add_field(name="__Starting Cells__", value=self.golitems[item]["conf"].count("1"))
            else:
                embed.add_field(name="__Density__", value=round(self.golitems[item]["conf"].count("1") / \
                                                            (self.golitems[item]["conf"].count("0") + self.golitems[item]["conf"].count("1")), 4))
            if self.golitems[item]["period"] != None:
                embed.add_field(name="__Period__", value=self.golitems[item]["period"])
            if self.golitems[item]["lifespan"] != None:
                embed.add_field(name="__Lifespan__", value=self.golitems[item]["lifespan"])
            embed.add_field(name="__Configuration__",
                            value="\`\`\`\n" + self.golitems[item]["conf"] + "\n\`\`\`", inline=False)
            if self.golitems[item]["notes"] != None:
                embed.add_field(name="__Notes__", value=self.golitems[item]["notes"])
            if item.lower() not in ("zebra stripes", "venetian blinds", "squaredance", "soup", "void"):
                embed.add_field(name="".join(["\_" for ij in range(20)]),
                value="**If you're gonna copy-paste this into `sygameoflife`, it is advised to add a few extra empty rows and columns.**",
                inline=False)
        elif item.lower() in ("categories", "cats", "ctgs", "category"):
            embed.description = """_ _
**MAIN CATEGORIES**
Still Life: A pattern that does nothing. It\'s just there.
Oscillator: A pattern that cycles between appearances.
Spaceship: An oscillator that, when its cycle is completed, finds itself in a new place.
Methuselah: A small pattern that explodes chaotically. For these, the wider your area, the better.

There are more (sub)categories too, but they aren't as important or interesting as the ones above.

__**SUBCATEGORIES**__
**Agar**: A pattern covering the entire plane that is periodic in both space and time.
**Barberpole**: See `bipole`, `tripole`, [__and more__](https://www.conwaylife.com/wiki/Barberpole)
**Billiard Table**: An oscillator whose rotor is enclosed in the stator.
**Conduit**: A pattern that can interact with an active object without being damaged.
**Constellation**: A pattern that is made of two or more independent islands.
**Familiar Four**: A common constellation made of four identical objects.
**Fuse**: A line of cells being "burnt" from at least one end, sometimes leaving a trail.
**Gun**: An oscillator that emits spaceships every cycle.
**Induction Coil**: An object that is used to stabilize an edge of another pattern.
**Island**: An isolated part of an object that does not touch any other island.
**Lake**: A still life that has a closed surface made from "dominoes".
**Muttering Moat**: An oscillator whose rotor consists of a closed chain of cells.
**Rake**: A puffer that leaves spaceships behind.
**Predecessor**: A pattern that evolves into another after a few generations.
**Puffer**: A spaceship that leaves debris behind.
**Rotor**: The parts of an oscillator that do change.
**Soup**: A randomized starting pattern.
**Spark**: A pattern that dies, normally thrown from oscillators and spaceships.
**Stator**: The parts of an oscillator that do not change.
**Tagalong**: An object that can be attached to a spaceship to be pulled along.
**xWSS**: A LWSS, a MWSS or a HWSS."""

            embed.add_field(name="".join(["\_" for ij in range(20)]),
                        value="https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life\nhttps://conwaylife.com/wiki/Main_Page")

        elif item == "":
            stl, osc, sps, mtl = ([], [], [], [])
            for i in self.golitems:
                if self.golitems[i]["type"] == "still life":
                    stl.append(i)
                elif self.golitems[i]["type"] == "oscillator":
                    osc.append(i)
                elif self.golitems[i]["type"] == "spaceship":
                    sps.append(i)
                elif self.golitems[i]["type"] == "methuselah":
                    mtl.append(i)
            stl.sort()
            osc.sort()
            sps.sort()
            mtl.sort()

            embed.description = f"""This command should be used for help with `sygameoflife`.

**YOU SHOULD READ THIS 👇**

**GAME RULES:**
For any generation,
- every \⬛ are dead cells and every \⬜ are alive cells.
- a dead cell with exactly 3 neighbours will become alive.
- an alive cell with more than 3 or less than 2 neighbours will die.
- an alive cell with either 2 or 3 neighbours stays alive.

Use `sy{ctx.invoked_with} categories` for information on the categories.
Use `sy{ctx.invoked_with} void` for a 40 x 24 grid with absolutely nothing.
Use `sy{ctx.invoked_with} soup` for a 40 x 24 grid where every cell is randomized.
Use `sy{ctx.invoked_with} <name>` for more information on any pattern below.

**If you're gonna copy-paste a pattern into `sygameoflife`, it is advised to add a few extra empty rows and columns.**

_ _"""
            embed.add_field(name="Still Lifes", value=f"{', '.join(['`' + i + '`' for i in stl])}", inline=False)
            embed.add_field(name="Oscillators", value=f"{', '.join(['`' + i + '`' for i in osc])}", inline=False)
            embed.add_field(name="Spaceships", value=f"{', '.join(['`' + i + '`' for i in sps])}", inline=False)
            embed.add_field(name="Methuselahs", value=f"{', '.join(['`' + i + '`' for i in mtl])}", inline=False)
            embed.add_field(name="".join(["\_" for ij in range(20)]),
                            value="https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life\nhttps://conwaylife.com/wiki/Main_Page")

        else:
            embed.set_image(url="http://upload.wikimedia.org/wikipedia/commons/e/e5/Gospers_glider_gun.gif?w=144")
            embed.description = f"Item `{item.lower()}` is not in Serpynth's Game of Life dictionary."
            embed.add_field(name="".join(["\_" for ij in range(20)]),
                            value="https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life\nhttps://conwaylife.com/wiki/Main_Page")

        await ctx.send(embed=embed)


    @commands.command(aliases=["rating", "rank", "ranking"])
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def rate(self, ctx, *, thing: str = ""):
        """
        Ask Serpynth for their opinion on anything.
        (Do NOT take this command seriously.)
        """

        for i in r"!%*?\_`|~":
            thing = thing.replace(i, "")
        if thing.replace(" ", "") == "":
            await ctx.send("You need to give me something to rate!")
            return
        if len(thing) > 50:
            await ctx.send("This thing is too long!\nMake sure that its name is 50 letters or less.")
            return

        dat = json.load(open("ranking.json", "r"))

        if thing.lower() not in dat:
            dat[thing.lower()] = [random.randint(0, 99) + random.random(), # score
                                    random.randint(0, 16777215), # colour
                                    ctx.author.id, # created-by
                                    time.time() # created-at
                                    ]
            dat["~"].append(dat[thing.lower()][0])
            dat["~"].sort(reverse=True)
            json.dump(dat, open("ranking.json", "w"))

        lenbar = round(dat[thing.lower()][0] / 10)
        this = str(dat["~"].index(dat[thing.lower()][0]) + 1)[len(str(dat["~"].index(dat[thing.lower()][0]) + 1)) - 1]

        suffixes = {"0": "th", "1": "st", "2": "nd", "3": "rd", "4": "th",
                    "5": "th", "6": "th", "7": "th", "8": "th", "9": "th"}

        if str(dat["~"].index(dat[thing.lower()][0]) + 1) in ("11", "12", "13", "111", "112", "113", "211", "212", "213", "311", "312", "313"):
            suffix = "th"
        else:
            suffix = suffixes[this]
        messages = {
        0: ["I absolutely despise this.", "This really disgusts me.", "Get that thing away from me!", "I'd rather commit sykill."],
        1: ["I really hate this.", "I would pay you to *not* give me this.", "I feel sick.", "I feel nauseous."],
        2: ["I hate this.", "Ew.", "This sucks."],
        3: ["I don't like this.", "This annoys me.", "I'd rather not."],
        4: ["It could be better.", "It's not *that* bad.", "It could be worse, though."],
        5: ["I don't have a strong opinion on this.", "Meh.", "It's okay, I guess."],
        6: ["It's kinda alright.", "It's pretty okay.", "It's not bad, I guess."],
        7: ["This is kinda nice.", "This is nice.", "It's cool."],
        8: ["I like this.", "This is pretty cool.", "It's pretty nice!", "This is good!"],
        9: ["I like this!", "This is amazing!", "This is really cool!"],
        10: ["This is brilliant!!!", "This is absolutely amazing!!", "WOW!!!"]
        }

        embed = discord.Embed(color=dat[thing.lower()][1])
        embed.title = "RATE MACHINE"
        embed.description = f"""
Rating {thing.upper()}

Score: `{round(dat[thing.lower()][0], 2)}/100`
{''.join(["◼" for i in range(lenbar)])}{''.join(["◻" for i in range(10 - lenbar)])}

Ranked `{dat["~"].index(dat[thing.lower()][0]) + 1}{suffix}` out of `{len(dat["~"])}`

"{random.choice(messages[lenbar])}"

"""
        if dat[thing.lower()][2] == ctx.author.id:
            embed.set_footer(text="You are the first to rate this item on Serpynth!")
        embed.timestamp = datetime.datetime.fromtimestamp(dat[thing.lower()][3])
        await ctx.send(embed=embed)


    @commands.command(aliases=["activity", "activities", "boring"])
    @commands.cooldown(2, 1, commands.BucketType.user)
    async def bored(self, ctx, type=""):
        """ Feeling bored? Serpynth will fix that for you. Maybe. """

        if type.lower() in ["education", "recreational", "social", "diy", "charity", "cooking", "relaxation", "music", "busywork"]:
            ac = f"https://www.boredapi.com/api/activity?type={type.lower()}/"
        else:
            ac = "https://www.boredapi.com/api/activity/"
        async with aiohttp.ClientSession() as session:
            async with session.get(ac) as info:
                info = await info.json()

        embed = discord.Embed(colour=random.randint(0, 16777215))
        embed.set_author(name="BORED?")
        embed.add_field(name=info["activity"], value=info["type"].capitalize() if info["type"] != "diy" else "DIY")
        embed.add_field(name="_ _", value=f"""Participants: `{info["participants"]}`
Price: `{round(info["price"] * 100)}/100`""", inline=False)
        embed.set_footer(text="https://www.boredapi.com/")
        await ctx.send(embed=embed)


    @commands.command(aliases=["guessthenumber"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def gtn(self, ctx):
        """ Can you guess what number Serpynth is thinking of? """

        number = random.randint(1, 100)
        await ctx.send("I have selected a random number between 1 and 100 (inclusive). Your job is to guess it.")
        nms = list(map(str, range(1, 101)))
        nms.extend(["exit", "quit", "end"])

        guesses = 0
        win = False
        while True:
            def check(m):
                return m.channel == ctx.channel and m.author == ctx.author and m.content in nms

            try:
                m = await self.client.wait_for("message", check=check, timeout=60.0)
            except asyncio.TimeoutError:
                break

            guesses += 1
            if m.content in ("exit", "quit", "end"):
                break
            elif int(m.content) > number:
                await ctx.send("My number is `less` than your guess.")
            elif int(m.content) < number:
                await ctx.send("My number is `greater` than your guess.")
            else:
                win = True
                await ctx.send(f"**GAME OVER**\nYou got it in `{guesses}` guesses!")

        if win == False:
            await ctx.send(f"**GAME OVER**\nYou left the game.")
        elif win == "ended already, cmon":
            pass
        win = "ended already, cmon"


    @commands.command(aliases=["guessyournumber"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def gyn(self, ctx):
        """ Can Serpynth guess what number you're thinking of? """

        def check(reaction, user):
            return reaction.emoji == "👍" and reaction.message == m and user == ctx.author

        m = await ctx.send("Select an integer between 1 and 100 (inclusive).\nReact with 👍 once you have one.")
        await m.add_reaction("👍")
        try:
            reaction, user = await self.client.wait_for("reaction_add", check=check, timeout=60.0)
        except asyncio.TimeoutError:
            await m.clear_reactions()
            return

        possibilities = list(range(1, 101))

        def median(v):
            v.sort()
            hi_midpoint = len(v) // 2

            if len(v) % 2 == 0:
                return  (v[hi_midpoint - 1] + v[hi_midpoint]) / 2
            else:
                return v[len(v) // 2]

        await ctx.send("For every guess I make, I want you to tell me if your number is higher than, lower than or equal to my guess. (>, <, =)")

        guesses = 0
        win = False
        while True:
            guesses += 1
            guess = median(possibilities)
            bg = guess
            await ctx.send(f"`{guess}`")

            def check(m):
                return m.channel == ctx.channel and m.author == ctx.author and m.content in (">", "<", "=", "quit", "exit", "end")

            try:
                m = await self.client.wait_for("message", check=check, timeout=60.0)
            except asyncio.TimeoutError:
                break

            if m.content == ">":
                freezepossibilities = possibilities[:]
                for i in freezepossibilities:
                    if i <= guess:
                        possibilities.remove(i)
                        bg = i
            elif m.content == "<":
                freezepossibilities = possibilities[:]
                for i in freezepossibilities:
                    if i >= guess:
                        possibilities.remove(i)
                        bg = i
            elif m.content == "=":
                if "." in str(guess):
                    win = None
                    break
                else:
                    win = True
                    break
            else:
                win = False
                break

            if len(possibilities) < 1:
                win = None
                break

        if win == True:
            await ctx.send(f"**GAME OVER**\nI won in `{guesses}` guesses!")
        elif win == None:
            await ctx.send(f"""**GAME OVER**\nAre you sure you followed the given rules?
My best guess is `{bg}`{", which is not an integer" if "." in str(guess) else ""}.""")
        elif win == "ended already, cmon":
            pass
        else:
            await ctx.send(f"**GAME OVER**\nYou left the game.")
        win = "ended already, cmon"


    @commands.command(aliases=["summoning"])
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def summon(self, ctx):
        """ An ancient Mayan summoning ritual, brought to Discord via Serpynth """

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        clrs = []
        clrs += "🟥🟧🟨🟩🟦🟪🟫⬛⬜"

        embed = discord.Embed(color=random.randint(0, 16777215))
        embed.set_author(name="SUMMONING")
        embed.description = """Create a summoning circle (which doesn't necessarily have to be a circle).
Make a 7x7 square of only colour tile emojis, in some pattern.
Then, send it."""

        embed.add_field(name="_ _", value="""For example,
🟩🟩🟥⬜🟥🟩🟩
🟩🟥🟨⬜🟨🟥🟩
🟥🟨🟨⬛🟨🟨🟥
⬜⬜⬛🟥⬛⬜⬜
🟥🟨🟨⬛🟨🟨🟥
🟩🟥🟨⬜🟨🟥🟩
🟩🟩🟥⬜🟥🟩🟩""")
        await ctx.send(embed=embed)

        try:
            async with ctx.channel.typing():
                m = await self.client.wait_for("message", check=check, timeout=600.0)
        except asyncio.TimeoutError:
            return
        pattern = m.content.replace(" ", "").split("\n")
        if len(pattern) != 7:
            await ctx.send("You didn't summon anything, because your summoning circle isn't set up correctly.")
            return

        for i in pattern:
            if len(i) != 7:
                await ctx.send("You didn't summon anything, because your summoning circle isn't set up correctly.")
                return
            for j in i:
                if j not in clrs:
                    await ctx.send("You didn't summon anything, because your summoning circle isn't set up correctly.")
                    return

        embed = discord.Embed()
        embed.set_author(name="SUMMONING")
        embed.description = f"""Summoning circle has been created!

{m.content}

Now spawning..."""
        msg = await ctx.send(embed=embed)

        theone = None
        for i in self.summons:
            good = True
            for j, k in enumerate(self.summons[i]):
                if k != "0":
                    if m.content[j] != k:
                        good = False
                        break
            if good == True:
                theone = i
                break

        cons = ["b", "c", "d", "f", "g", "h", "j", "k", "l", "m", "n", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
        embed = discord.Embed(colour=discord.Colour.green() if theone != None else discord.Colour.gold())
        embed.set_author(name="SUMMONING")
        if theone != None:
            embed.description = f"""
{m.content}

You summoned {"a" if theone[0].lower() in cons else "an"} {theone}!"""
        else:
            embed.description = f"""
{m.content}

You didn't summon anything this time. Try again!"""
        await asyncio.sleep(random.randint(5, 10))
        await msg.edit(content=self.summonemojis[theone] if theone != None else None, embed=embed)


    @commands.command(aliases=["koth", "king", "hill"])
    async def kingofthehill(self, ctx):
        """ A variation on King of the Hill, through Discord """

        embed = discord.Embed(colour=random.randint(0, 16777215))
        embed.set_author(name="KING OF THE HILL")
        embed.description = """WELCOME TO KING OF THE HILL!
This server is an experiment.

In this server, everyone has the permissions to kick others.
However, since nobody actually has a role (except for Yee#2462 and Serpynth),
nobody can kick anyone, unless you use `sykick @member`.
Kicking others will get you points, however, if you yourself are kicked,
you lose all of them. You can check your personal highscore and current score
with `syscore` in any server.

Since this entire thing is based around Serpynth, nobody will be able to do anything when they are offline.

Have fun!


_ _"""

        embed.add_field(name="YOU MAY...", value="""- Create truces and teams, but I will not enforce them.
- Target one individual several times. You will have to stop eventually, right?
- Be as salty as you need to be.
- Kick yourself out of the server. However, this will still clear all of your points.
- Discuss outside of the server, in other channels or through DMs.""", inline=False)

        embed.add_field(name="RULES", value="""1. Don't be offensive in any way.
2. Don't post NSFW content.
3. Try to minimize swearing.""", inline=False)

        embed.add_field(name="PERMANENT INVITES", value="""
[To information channel](https://discord.gg/hTDCvP28hZ)
[To main text channel](https://discord.gg/SzMUwWfgrf)
[To main voice channel](https://discord.gg/nkzWUskX6w)""", inline=False)
        await ctx.send(content="https://discord.gg/hTDCvP28hZ", embed=embed)


    @commands.command(aliases=["silence", "silent", "sc"])
    async def silencecontest(self, ctx, opponent: discord.Member):
        """ A great tool to get someone else to shut up """

        embed = discord.Embed(colour=0x000000)
        embed.set_author(name="SILENCE!")
        embed.description = "The rules of the game are simple. First to send one message anywhere loses."
        embed.add_field(name="Players", value=f"{ctx.author.mention}\n{opponent.mention}")
        msg = await ctx.send(embed=embed)

        players = (ctx.author, opponent)
        def check(m):
            return m.author in players

        m = await self.client.wait_for("message", check=check)
        await msg.reply(f"""**GAME OVER**\n{m.author.mention} lost; {players[players.index(m.author) - 1].mention} is the winner!
Losing message: {m.jump_url}""", mention_author=False)


    @commands.command(aliases=["appl", "apple", "apples", "a2a"])
    @commands.cooldown(1, 240, commands.BucketType.user)
    async def applestoapples(self, ctx):
        """ 
        Starts a game of in-Discord Apples to Apples.
        Instructions and rules are in the command.
        """

        embed = discord.Embed(colour=0xe74c3c)
        embed.set_author(name="APPLES TO APPLES")
        embed.description = f"""Welcome to Apples to Apples! <:appl:832628199141539880>
This game is a multiplayer game, so you'll need more than yourself to play.

RULES
- Everyone playing is given 7 numbered cards, which will be sent to them via DMs.
- {ctx.author.mention} will be the judge on the first round.
- A random adjective will be given. Everyone except the judge should send the
number of the card that would fit the adjective the most.
- You are allowed to try to convince the judge why yours is the best.
- The judge should then choose the best answer; the one that fits the adjective
the most.
- Everyone other than the judge will get another card, so they'll still have 7.
- The winner of the round gets to keep the adjective, gains a point, and
becomes the next judge.
- Throughout the whole game, you can say "quit" if you want to quit.
[Official Rules](https://service.mattel.com/instruction_sheets/N1488-0920.pdf)

EXAMPLE ROUND
Alice is the judge. Bob and Carol are also playing.
The adjective is "delicious".
Bob checks his DMs and he thinks that "Pizza" would be a good card.
"Pizza" has the number 20, so he goes back to the channel they're playing
in and sends "20".
Carol does not have any good cards for this adjective, and believes she has
no chance of winning. She decides to play her least interesting card, which
is  "Trapezoids". By getting rid of her bad cards, she has a chance of getting a better one.
Alice has decided "Pizza" is better. Bob gains a point and becomes the next judge."""
        embed.add_field(name="_ _", value=("**React with 🙋 if you want to join!**"
                        f"\n**{ctx.author.mention} may start the game by reacting with 👍.**"), inline=False)


        join = await ctx.send(embed=embed)

        await join.add_reaction("🙋")
        await join.add_reaction("👍")

        def checkstart(reaction, user):
            return reaction.message == join and reaction.emoji =="👍" and user == ctx.author

        await self.client.wait_for("reaction_add", check=checkstart)
        NEWLINE = "\n"
        join = await ctx.channel.fetch_message(join.id)
        players = [i async for i in join.reactions[0].users()]
        if not ctx.author in players:
            players.insert(0, ctx.author)
        if self.client.user in players:
            players.remove(self.client.user)

        if len(players) < 3:
            await ctx.send("You can't play this game with less than 3 players!")
            return

        cards = {}
        points = {}
        for player in players:
            cards[player] = {}
            points[player] = 0
            for i in range(7):
                card = str(random.randint(0, len(self.applecards["cards"]) - 1))
                cards[player][card] = self.applecards["cards"][card]
            mycards = [f"`{i}`: {self.applecards['cards'][i]}" for i in cards[player]]

            embed = discord.Embed(colour=0xf1c40f)
            embed.set_author(name="YOUR CARDS")
            embed.description = "These are your cards. It is best to keep them hidden from everyone else!"
            embed.add_field(name="_ _", value="\n".join(mycards), inline=False)
            embed.add_field(name="_ _", value=f"Jump back to the game: {ctx.channel.mention}")
            try:
                await player.send(embed=embed)
            except:
                await ctx.send(f"I was unable to send {player.mention} a DM, therefore, they are unable to play.")
                players.remove(player)
                del cards[player]

        judge = ctx.author
        embed = discord.Embed(colour=0x2ecc71)
        embed.set_author(name="THE GAME IS NOW STARTING!!")
        embed.description = f"__PLAYERS__\n{NEWLINE.join([i.mention for i in players])}\n\n__JUDGE__\n{judge.mention}"
        await ctx.send(embed=embed)
        await asyncio.sleep(3.0)

        while True:
            count = 0
            adj = random.choice(list(self.applecards["adjectives"])).upper()

            embed = discord.Embed(colour=0xe74c3c)
            embed.set_author(name="APPLES TO APPLES")
            embed.description = f"The adjective is `{adj}`!"
            embed.add_field(name="_ _", value=f"This round's judge is {judge.mention}.")
            embed.add_field(name="_ _", value=f"{count}/{len(players) - 1} have submitted a card!")
            game = await ctx.send(embed=embed)

            def check(m):
                if m.content.isdigit():

                    return m.channel == ctx.channel and (m.author in players) and m.author != judge \
                        and -1 < int(m.content) < len(self.applecards["cards"]) and m.content in cards[m.author]
                else:
                    return m.content.lower() == "quit"

            playedcards = {}
            while True:
                m = await self.client.wait_for("message", check=check)
                if m.content.lower() == "quit":
                    await ctx.send(f"{m.author.mention} has left the game.")
                    players.remove(player)
                    del cards[player]

                    if len(players) < 3:
                        embed = discord.Embed(colour=0xf1c40f)
                        embed.set_author(name="GAME OVER")
                        embed.description = "There are not enough people to continue playing."
                        embed.add_field(name="FINAL SCORES", value=NEWLINE.join([f"{i.mention}: `{points[i]}`" for i in points]))
                        await ctx.send(embed=embed)
                        return
                    continue

                playedcards[m.content] = m.author
                count += 1
                embed.remove_field(1)
                del cards[m.author][m.content]
                if count == len(players) - 1:
                    embed.add_field(name="JUDGING TIME!",
                                    value=NEWLINE.join(["`" + i + "`: " + self.applecards["cards"][i] for i in playedcards]))
                    embed.add_field(name="_ _", value="Send the number of the one you think is the best.", inline=False)
                    await game.edit(embed=embed)
                    break
                else:
                    embed.add_field(name="_ _", value=f"{count}/{len(players) - 1} have submitted a card!")
                    await game.edit(embed=embed)

            def check(m):
                return m.channel == ctx.channel and m.author == judge and m.content in playedcards

            m = await self.client.wait_for("message", check=check)
            winner = playedcards[m.content]
            points[winner] += 1
            await winner.send(f"You've gained a point for the adjective `{adj}`!\n"
                            f"You now have `{points[winner]}` point{'s' if points[winner] != 1 else ''}.")
            judge = winner

            for player in players:
                if len(cards[player]) < 7:
                    for i in range(7 - len(cards[player])):
                        card = str(random.randint(0, len(self.applecards["cards"]) - 1))
                        cards[player][card] = self.applecards["cards"][card]
                        mycards = [f"`{i}`: {self.applecards['cards'][i]}" for i in cards[player]]
                        embed = discord.Embed(colour=0xf1c40f)
                        embed.set_author(name="YOUR CARDS")
                        embed.description = "These are your cards. It is best to keep them hidden from everyone else!"
                        embed.add_field(name="_ _", value="\n".join(mycards), inline=False)
                        embed.add_field(name="_ _", value=f"Jump back to the game: {ctx.channel.mention}")
                        try:
                            await player.send(embed=embed)
                        except:
                            await ctx.send(f"I was unable to send {player.mention} a DM, therefore, they are unable to play.")
                            players.remove(player)
                            del cards[player]


    @commands.command(aliases=["roulette", "rickroulette", "rr"])
    @commands.cooldown(2, 1, commands.BucketType.user)
    async def russianroulette(self, ctx, links: int = 6):
        """ Avoid the rickroll. Be rewarded. """

        if links > 9 or links < 2:
            links = 6

        urls = ["https://youtu.be/Wl9oUBgFk6Y", "https://youtu.be/Kj2hNx2rTm4",
                "https://youtu.be/J-fXTRHApRc", "https://youtu.be/v1K4EAXe2oo",
                "https://youtu.be/sXxbkjlHvf4", "https://youtu.be/J---aiyznGQ",
                "https://youtu.be/q6EoRBvdVPQ", "https://youtu.be/GInovXm59Ew",
                "https://youtu.be/MFmr_TZLpS0", "https://youtu.be/pHXDMe6QV-U?t=47",
                "https://youtu.be/GJDNkVDGM_s", "https://youtu.be/dgha9S39Y6M?t=35",
                "https://youtu.be/LDU_Txk06tM?t=75", "https://youtu.be/oavMtUWDBTM",
                "https://youtu.be/vAvcxeXtBz0", "https://youtu.be/Wl959QnD3lM",
                "https://youtu.be/3uQzdlVsLXY", "https://youtu.be/13pgxOCHKh0",
                "https://youtu.be/7Zm1hPbmzPw", "https://youtu.be/j8qp3ITVqY0",
                "https://youtu.be/_hUedwT-DOs", "https://youtu.be/Yw6u6YkTgQ4",
                "https://youtu.be/N_1fdxnZt_A", "https://youtu.be/dP5jVCyfJjA",
                "https://youtu.be/jF1wh1COW8o", "https://youtu.be/Hl6G8-2CPP0",
                "https://youtu.be/YSgOfBC0crg", "https://youtu.be/9hhrJowPx_g",
                "https://youtu.be/3B-ptWQOHzY", "https://youtu.be/fjhS6bwuxVc",
                "https://youtu.be/v3i8vsIUA7Q", "https://youtu.be/wAUK9hVgmNI",
                "https://youtu.be/MKxe1UEfRe8", "https://youtu.be/CMNry4PE93Y",
                "https://youtu.be/UOoJGtu9FnI", "https://youtu.be/E3Pv4c4Qz9w",
                "https://youtu.be/eWM2joNb9NE", "https://youtu.be/nQ7c-WqrlPY",
                "https://youtu.be/NhBktFVTjf8", "https://youtu.be/hkihSS2kX9g",
                "https://youtu.be/c7BVtGnlxT8", "https://youtu.be/akGpGA3jYek",
                "https://youtu.be/St7X_TcGiS8", "https://youtu.be/PH0QPZefNm4",
                "https://youtu.be/QSS3GTmKWVA", "https://youtu.be/NonAH--fF_Q",
                "https://youtu.be/QniU6nSkW8Q", "https://youtu.be/mMh9A_4u2ic",
                "https://youtu.be/LZgeIReY04c", "https://youtu.be/6-7NDP8V-6A",
                "https://youtu.be/9U9eIizzjb4", "https://youtu.be/JubwyDZuacM",
                "https://youtu.be/D-UmfqFjpl0", "https://youtu.be/WOLPMBqIu_E",
                "https://youtu.be/IP9NCpvtw5s", "https://youtu.be/_B0CyOAO8y0?t=14",
                "https://youtu.be/nKNithr9OH4?t=19", "https://youtu.be/2JYJF9L5YW4",
                "https://youtu.be/Wl9oUBgFk6Y"]
        ricks = ["https://youtu.be/dQw4w9WgXcQ", "https://youtu.be/IO9XlQrEt2Y",
                "https://youtu.be/GHMjD0Lp5DY?t=11", "https://youtu.be/34Ig3X59_qA",
                "https://youtu.be/cvh0nX08nRw", "https://youtu.be/-51AfyMqnpI",
                "https://youtu.be/MRW7d7PIZ6U", "https://youtu.be/sO4wVSA9UPs?t=27",
                "https://youtu.be/G8iEMVr7GFg"]
        select = random.sample(urls, links)
        select[random.randint(0, links - 1)] = random.choice(ricks)
        for i, j in enumerate(select):
            select[i] = f"ᅠ ᅠ [`[→  #{i + 1}{' ' if i < 9 else ''} ←]`]({j} 'Take your pick, don\'t click the rick!') ᅠ ᅠ "

        UNDERSCORE = "\_"
        NEWLINE = "\n"
        embed = discord.Embed(colour=0xf1c40f)
        embed.set_author(name="RUSSIAN ROULETTE", url="https://youtu.be/dQw4w9WgXcQ")
        embed.description = f"""There are {links} buttons below, and one is a rickroll.
    Choose a button to click. Don't get rickrolled and you'll be blessed!

    *I mean, you can click as many as you want or none at all,*
    *but that kinda ruins the point.*

    *Play fair!*
    *If you click a rick, you have legally been rickrolled, even if you don't watch it.*

    """
        embed.add_field(name=UNDERSCORE * 22, value=f"_ _\n{NEWLINE.join(select)}")
        embed.add_field(name=UNDERSCORE * 22, value="_ _\n_ _", inline=False)
        embed.set_image(url="https://cdn.discordapp.com/attachments/749006528182353988/854021145551175690/image_1.jpg")
        embed.set_footer(text="Make sure to Trust this Domain for full effect")
        await ctx.send(embed=embed)


async def setup(client):
    await client.add_cog(Fun(client))
