import discord
import time
from discord.ext import commands
from discord.utils import get
import random
import asyncio


class Chill(commands.Cog, name="🌲 Chill", description="""
This category is similar to **🎢 Fun**, except they're more relaxed.
Most of these commands work with emojis. This doesn't really have
much relation to the idea of the category, but is just mainly a
coincidence.
"""):
    def __init__(self, client):
        self.client = client
        self.tilesbusy = set()
        self.fishes = {1: "🐟", 2: "🐠", 3: "🐡", 4: "🦈",
                5: "🐬", 6: "🐳", 7: "🐙", 8: "🦑",
                9: "🦀", 10: "🦐", 11: "🦞",
                12: "👢",
                13: "🦪", 14: "🏴‍☠️", 15: "📱", 16: "⬛"}
        self.bakery = {"croissant": "🥐", "bagel": "🥯", "baguette": "🥖",
                        "flatbread": "🫓", "pretzel": "🥨", "bread": "🍞",
                        "donut": "🍩", "pie": "🥧", "birthday cake": "🎂",
                        "slice of cake": "🍰", "cupcake": "🧁", "custard": "🍮",
                        "stuffed flatbread": "🥙"}
        self.beverages = {"coffee": "☕", "tea": "🍵", "tropical": "🍹",
                        "wine": "🍷", "whisky": "🥃", "cocktail": "🍸",
                        "beer": "🍺", "sake": "🍶", "water": "🥤",
                        "juicebox": "🧃", "bubble tea": "🧋", "mate": "🧉",
                        "milk": "🥛", "champagne": "🍾"}
        self.breakfast = {"croissant": "🥐", "egg": "🍳", "pancakes": "🥞",
                        "waffle": "🧇", "bacon": "🥓", "sandwich": "🥪",
                        "bagel": "🥯"}
        self.asian = {"ramen": "🍜", "stew": "🍲", "curry": "🍛",
                        "sushi": "🍣", "bento": "🍱", "dumplings": "🥟",
                        "shrimp": "🍤", "riceball": "🍙", "rice": "🍚",
                        "rice cracker": "🍘", "fishcake": "🍥",
                        "fortune cookie": "🥠", "mooncake": "🥮", "oden": "🍢",
                        "dango": "🍡"}
        self.sweets = {"lollipop": "🍭", "candy": "🍬", "chocolate": "🍫",
                        "popcorn": "🍿", "cookie": "🍪", "cupcake": "🧁",
                        "donut": "🍩"}
        self.icecreamery = {"shaved ice": "🍧", "ice cream": "🍨", "cone": "🍦"}
        self.foreign = {"falafel": "🧆", "paella": "🥘", "taco": "🌮",
                        "burrito": "🌯", "tamale": "🫔"}
        self.fastfood = {"hotdog": "🌭", "burger": "🍔", "fries": "🍟",
                        "pizza": "🍕"}
        self.fruit = {"apple": "🍎", "pear": "🍐", "orange": "🍊",
                        "lemon": "🍋", "banana": "🍌", "watermelon": "🍉",
                        "grapes": "🍇", "blueberries": "🫐", "strawberries": "🍓",
                        "cherries": "🍒", "peach": "🍑", "mango": "🥭",
                        "pineapple": "🍍", "coconut": "🥥", "kiwi": "🥝",
                        "tomato": "🍅", "eggplant": "🍆", "avocado": "🥑",
                        "olives": "🫒", "bellpepper": "🫑", "pepper": "🌶️",
                        "cucumber": "🥒", "corn": "🌽", "carrot": "🥕",
                        "garlic": "🧄", "onion": "🧅", "potato": "🥔",
                        "sweet potato": "🍠"}
        self.other = {"spaghetti": "🍝", "salad": "🥗", "fondue": "🫕",
                        "cheese": "🧀", "steak": "🥩", "meat": "🍗",
                        "takeout": "🥡"}
        pizza = [
        """
        🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫
        🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫
        🟫🟫🟫🟫⬜⬜⬜🟫🟫🟫🟫
        🟫🟫🟫⬜⬜⬜⬜⬜🟫🟫🟫
        🟫🟫⬜⬜⬜⬜⬜⬜⬜🟫🟫
        🟫🟫⬜⬜⬜⬜⬜⬜⬜🟫🟫
        🟫🟫⬜⬜⬜⬜⬜⬜⬜🟫🟫
        🟫🟫🟫⬜⬜⬜⬜⬜🟫🟫🟫
        🟫🟫🟫🟫⬜⬜⬜🟫🟫🟫🟫
        🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫
        🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫
        """,
        """
        ⬛
        ⬛⬛⬛🟧🟧🟧🟧🟧
        ⬛⬛🟧🟧🟥🟨🟨🟧🟧
        ⬛🟧🟧🟨🟨🟨🟥🟥🟧🟧
        ⬛🟧🟨🟨🟨🟨🟥🟥🟨🟧
        ⬛🟧🟨🟥🟥🟨🟨🟨🟨🟧
        ⬛🟧🟨🟥🟥🟨🟨🟨🟨🟧
        ⬛🟧🟧🟨🟨🟨🟨🟥🟧🟧
        ⬛⬛🟧🟧🟥🟨🟨🟧🟧
        ⬛⬛⬛🟧🟧🟧🟧🟧
        ⬛
        """,
        """
        ⬛
        ⬛⬛⬛🟧🟧
        ⬛⬛🟧🟧🟥⬛⬛⬛🟧
        ⬛🟧🟧🟨🟨⬛⬛🟥🟧🟧
        ⬛🟧🟨🟨🟨⬛🟥🟥🟨🟧
        ⬛🟧🟨🟥🟥🟨🟨🟨🟨🟧
        ⬛🟧🟨🟥🟥🟨🟨🟨🟨🟧
        ⬛🟧🟧🟨🟨🟨🟨🟥🟧🟧
        ⬛⬛🟧🟧🟥🟨🟨🟧🟧
        ⬛⬛⬛🟧🟧🟧🟧🟧
        ⬛
        """,
        """
        ⬛
        ⬛⬛⬛🟧🟧
        ⬛⬛🟧🟧🟥
        ⬛🟧🟧🟨🟨
        ⬛🟧🟨🟨🟨
        ⬛🟧🟨🟥🟥🟨🟨🟨🟨🟧
        ⬛🟧🟨🟥🟥🟨🟨🟨🟨🟧
        ⬛🟧🟧🟨🟨🟨🟨🟥🟧🟧
        ⬛⬛🟧🟧🟥🟨🟨🟧🟧
        ⬛⬛⬛🟧🟧🟧🟧🟧
        ⬛
        """,
        """
        ⬛
        ⬛⬛⬛🟧🟧
        ⬛⬛🟧🟧🟥
        ⬛🟧🟧🟨🟨
        ⬛🟧🟨🟨🟨
        ⬛🟧🟨🟥🟥
        ⬛🟧🟨🟥🟥🟨
        ⬛🟧🟧🟨🟨🟨🟨
        ⬛⬛🟧🟧🟥🟨🟨🟧
        ⬛⬛⬛🟧🟧🟧🟧🟧
        ⬛
        """,
        """
        ⬛
        ⬛⬛⬛🟧🟧
        ⬛⬛🟧🟧🟥
        ⬛🟧🟧🟨🟨
        ⬛🟧🟨🟨🟨
        ⬛🟧🟨🟥🟥
        ⬛🟧🟨🟥🟥
        ⬛🟧🟧🟨🟨
        ⬛⬛🟧🟧🟥
        ⬛⬛⬛🟧🟧
        ⬛
        """,
        """
        ⬛
        ⬛⬛⬛🟧🟧
        ⬛⬛🟧🟧🟥
        ⬛🟧🟧🟨🟨
        ⬛🟧🟨🟨🟨
        ⬛🟧🟨🟥⬛
        ⬛🟧🟨⬛⬛
        ⬛🟧⬛⬛⬛
        ⬛⬛⬛⬛⬛
        ⬛⬛⬛⬛⬛
        ⬛
        """,
        """
        ⬛⬛⬛⬛⬛
        ⬛⬛⬛🟧🟧
        ⬛⬛🟧🟧🟥
        ⬛🟧🟧🟨🟨
        ⬛🟧🟨🟨🟨
        ⬛⬛⬛⬛⬛
        ⬛⬛⬛⬛⬛
        ⬛⬛⬛⬛⬛
        ⬛⬛⬛⬛⬛
        ⬛⬛⬛⬛⬛
        ⬛
        """,
        """
        ⬛⬛⬛⬛⬛
        ⬛⬛⬛🟧🟧
        ⬛⬛🟧🟧🟥
        ⬛⬛⬛🟨🟨
        ⬛⬛⬛⬛🟨
        ⬛⬛⬛⬛⬛
        ⬛⬛⬛⬛⬛
        ⬛⬛⬛⬛⬛
        ⬛⬛⬛⬛⬛
        ⬛⬛⬛⬛⬛
        ⬛
        """,
        """
        ⬛⬛⬛⬛⬛
        ⬛⬛⬛⬛⬛
        ⬛⬛⬛⬛⬛
        ⬛⬛⬛⬛⬛
        ⬛⬛⬛⬛⬛
        ⬛⬛⬛⬛⬛
        ⬛⬛⬛⬛⬛
        ⬛⬛⬛⬛⬛
        ⬛⬛⬛⬛⬛
        ⬛⬛⬛⬛⬛
        ⬛
        """]

        def txt2emj(s: str):
            return s.replace(":tbg:", "<:__:1028468329456865310>") \
            .replace(":peach2:", "<:peach2:1028420680854814831>") \
            .replace(":peach1:", "<:peach1:1028420681983066132>") \
            .replace(":brown:", "<:brown1:1028423585674571816>") \
            .replace(":stbl:", "<:blue2:1028423584198176779>") \
            .replace(":blue:", "<:blue1:1028423586828001280>") \
            .replace(":black:", "<:black:1028451145099776070>")

        self.regchair = txt2emj(""":tbg::tbg::tbg::peach2::peach2:
:tbg::tbg::tbg::peach2::peach2:
:tbg::tbg::peach1::peach2::peach2:
:tbg::tbg::tbg::peach2::peach2::brown:
:tbg::tbg::tbg::blue::blue::brown:
:tbg::tbg::tbg::blue::blue::brown:
:tbg::tbg::tbg::blue::blue::brown:
:tbg::tbg::tbg::blue::blue::brown:
:tbg::stbl::stbl::stbl::stbl::brown:
:tbg::stbl::brown::brown::brown::brown:
:tbg::stbl::brown::tbg::tbg::brown:
:tbg::stbl::brown::tbg::tbg::brown:
:tbg::peach2::brown::tbg::tbg::brown:""")
        self.emptychair = txt2emj(""":tbg::tbg::tbg::tbg::tbg:
:tbg::tbg::tbg::tbg::tbg:
:tbg::tbg::tbg::tbg::tbg:
:tbg::tbg::tbg::tbg::tbg::brown:
:tbg::tbg::tbg::tbg::tbg::brown:
:tbg::tbg::tbg::tbg::tbg::brown:
:tbg::tbg::tbg::tbg::tbg::brown:
:tbg::tbg::tbg::tbg::tbg::brown:
:tbg::tbg::tbg::tbg::tbg::brown:
:tbg::tbg::brown::brown::brown::brown:
:tbg::tbg::brown::tbg::tbg::brown:
:tbg::tbg::brown::tbg::tbg::brown:
:tbg::tbg::brown::tbg::tbg::brown:""")
        self.phonechair = txt2emj(""":tbg::tbg::tbg::peach2::peach2:
:tbg::tbg::tbg::peach2::peach2:
:black::tbg::peach1::peach2::peach2:
:black::tbg::tbg::peach2::peach2::brown:
:peach2::blue::blue::blue::blue::brown:
:tbg::tbg::tbg::blue::blue::brown:
:tbg::tbg::tbg::blue::blue::brown:
:tbg::tbg::tbg::blue::blue::brown:
:tbg::stbl::stbl::stbl::stbl::brown:
:tbg::stbl::brown::brown::brown::brown:
:tbg::stbl::brown::tbg::tbg::brown:
:tbg::stbl::brown::tbg::tbg::brown:
:tbg::peach2::brown::tbg::tbg::brown:""")
        self.watchchair = txt2emj(""":tbg::tbg::tbg::peach2::peach2:
:tbg::tbg::tbg::peach2::peach2:
:tbg::tbg::peach1::peach2::peach2:
:tbg::tbg::tbg::peach2::peach2::brown:
:tbg::peach2::black::blue::blue::brown:
:tbg::tbg::tbg::blue::blue::brown:
:tbg::tbg::tbg::blue::blue::brown:
:tbg::tbg::tbg::blue::blue::brown:
:tbg::stbl::stbl::stbl::stbl::brown:
:tbg::stbl::brown::brown::brown::brown:
:tbg::stbl::brown::tbg::tbg::brown:
:tbg::stbl::brown::tbg::tbg::brown:
:tbg::peach2::brown::tbg::tbg::brown:""")
        self.napchair = txt2emj(""":tbg::tbg::tbg::peach2::peach2:💤
:tbg::tbg::tbg::peach2::peach2:
:tbg::tbg::peach1::peach2::peach2:
:tbg::tbg::tbg::peach2::peach2::brown:
:tbg::tbg::tbg::blue::blue::brown:
:tbg::tbg::tbg::blue::blue::brown:
:tbg::tbg::tbg::blue::blue::brown:
:tbg::tbg::tbg::blue::blue::brown:
:tbg::stbl::stbl::stbl::stbl::brown:
:tbg::stbl::brown::brown::brown::brown:
:tbg::stbl::brown::tbg::tbg::brown:
:tbg::stbl::brown::tbg::tbg::brown:
:tbg::peach2::brown::tbg::tbg::brown:""")
        self.upchair = txt2emj(""":tbg::tbg::tbg::peach2::peach1:
:tbg::tbg::tbg::peach2::blue:
:tbg::tbg::peach1::peach2::blue:
:tbg::tbg::tbg::peach2::blue::brown:
:tbg::tbg::tbg::blue::blue::brown:
:tbg::tbg::tbg::blue::blue::brown:
:tbg::tbg::tbg::blue::blue::brown:
:tbg::tbg::tbg::blue::blue::brown:
:tbg::stbl::stbl::stbl::stbl::brown:
:tbg::stbl::brown::brown::brown::brown:
:tbg::stbl::brown::tbg::tbg::brown:
:tbg::stbl::brown::tbg::tbg::brown:
:tbg::peach2::brown::tbg::tbg::brown:""")
        self.outchair = txt2emj(""":tbg::tbg::tbg::peach2::peach2:
:tbg::tbg::tbg::peach2::peach2:
:tbg::tbg::peach1::peach2::peach2:
:tbg::tbg::tbg::peach2::peach2::brown:
:tbg::peach2::blue::blue::blue::brown:
:tbg::tbg::tbg::blue::blue::brown:
:tbg::tbg::tbg::blue::blue::brown:
:tbg::tbg::tbg::blue::blue::brown:
:tbg::stbl::stbl::stbl::stbl::brown:
:tbg::stbl::brown::brown::brown::brown:
:tbg::stbl::brown::tbg::tbg::brown:
:tbg::stbl::brown::tbg::tbg::brown:
:tbg::peach2::brown::tbg::tbg::brown:""")


    @commands.command(aliases=["behappy", "dontworrybehappy", "dwbh"])
    async def dontworry(self, ctx):
        """ Don't worry. Be happy. """
        await ctx.send("https://youtu.be/d-diB65scQU")


    @commands.command(aliases=["forest"])
    async def camp(self, ctx):
        """ Come, sit down. You can stay for as long as you like """
        blank = "<:__:1028468329456865310>"

        sky = [0, 1, 2, 3, 4, 5, 6, 7, "🌤"]
        random.shuffle(sky)
        for object in sky:
            if object != "🌤":
                if random.randint(1, 7) == 1:
                    sky[sky.index(object)] = "☁"
                else:
                    sky[sky.index(object)] = blank

        forest = [0, 1, 2, 3, 4, 5, 6, f"{blank}🏕"]
        for object in forest:
            if object != f"{blank}🏕":
                if random.randint(1, 5) == 1:
                    forest[forest.index(object)] = "🌳"
                else:
                    forest[forest.index(object)] = "🌲"
        while f"{blank}🏕" in (forest[0], forest[7]):
            random.shuffle(forest)

        grass = ["🟩" for i in range(9)]
        if random.randint(1, 2) == 1:
            grass = ["🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", "🟩", 1]
            while 1 == grass[8]:
                random.shuffle(grass)
            if random.randint(1, 4) == 1:
                while forest.index(f"{blank}🏕") in [grass.index(1) - 1, grass.index(1)]:
                    random.shuffle(grass)
                if forest.index(f"{blank}🏕") > grass.index(1):
                    forest[grass.index(1)] = blank
                else:
                    forest[grass.index(1) - 1] = blank
                grass[grass.index(1)] = "🟦"
            else:
                while forest.index(f"{blank}🏕") in [grass.index(1) - 1, grass.index(1), grass.index(1) + 1]:
                    random.shuffle(grass)
                grass[grass.index(1) + 1] = 2
                if forest.index(f"{blank}🏕") > grass.index(1):
                    forest[grass.index(1)] = blank
                    forest[grass.index(2)] = blank
                else:
                    forest[grass.index(1) - 1] = blank
                    forest[grass.index(2) - 1] = blank
                grass[grass.index(1)] = "🟦"
                grass[grass.index(2)] = "🟦"


        await ctx.send(f"{''.join(sky)}\n"
                        f"{''.join(forest)}\n"
                        f"{''.join(grass)}")


    @commands.command(aliases=["christmas", "cmas"])
    async def xmas(self, ctx):
        """
        Merry Christmas!
        `sylandscape` but in a festive mood.
        """

        blank = "<:__:1028468329456865310>"
        items = ["🌲", "🎄", "⛄"]
        terrain = [random.randint(1, 3)]
        for x in range(19):
            if x % random.randint(3, 4) == 0 and terrain[len(terrain) - 1] == terrain[len(terrain) - 2]:
                terrain.append(int(terrain[x]) + random.choice((-1, 1)))
                if terrain[len(terrain) - 1] > 4:
                    terrain[len(terrain) - 1] += -2
                elif terrain[len(terrain) - 1] < 1:
                    terrain[len(terrain) - 1] += 2
            else:
                terrain.append(terrain[len(terrain) - 1])
        l = [[], [], [], [], []]
        for item in terrain:
            l[0].append("⬜")
            if item > 1:
                l[1].append("⬜")
                if item > 2:
                    l[2].append("⬜")
                    if item > 3:
                        l[3].append("⬜")
                    else:
                        l[3].append(blank)
                else:
                    l[2].append(blank)
                    l[3].append(blank)
            else:
                l[1].append(blank)
                l[2].append(blank)
                l[3].append(blank)
            l[4].append(blank)

        e = enumerate(terrain)
        for t, v in e:
            if random.randint(1, 5) < 2:
                l[v][t] = random.choices(items, weights=[9, 2, 3])[0]

        colors = [0x00ff6a, 0xff0000, 0xbdfffd]
        color = random.choice(colors)
        l.reverse()
        embed = discord.Embed(title=random.choice(("Merry Christmas!", "Happy Holidays!")),
            description = "\n".join(["".join(i) for i in l]), color=color)
        await ctx.send(embed=embed)


    @commands.command(aliases=["terrain", "land"])
    async def landscape(self, ctx):
        """ Generates a random terrain with tile emojis """

        blank = "<:__:1028468329456865310>"
        terrain = [random.randint(1, 3)]
        for x in range(19):
            if x % random.randint(3, 4) == 0 and terrain[len(terrain) - 1] == terrain[len(terrain) - 2]:
                terrain.append(int(terrain[x]) + random.choice((-1, 1)))
                if terrain[len(terrain) - 1] > 4:
                    terrain[len(terrain) - 1] += -2
                elif terrain[len(terrain) - 1] < 1:
                    terrain[len(terrain) - 1] += 2
            else:
                terrain.append(terrain[len(terrain) - 1])
        l = [[], [], [], [], []]
        for item in terrain:
            l[0].append("🟩")
            if item > 1:
                l[1].append("🟩")
                if item > 2:
                    l[2].append("🟩")
                    if item > 3:
                        l[3].append("🟩")
                    else:
                        l[3].append(blank)
                else:
                    l[2].append(blank)
                    l[3].append(blank)
            else:
                l[1].append(blank)
                l[2].append(blank)
                l[3].append(blank)
            l[4].append(blank)

        e = enumerate(terrain)
        for t, v in e:
            if random.randint(1, 6) < 2:
                l[v][t] = "🌳"


        for r, y in enumerate(l):
            for c, x in enumerate(y):
                if l[r][c] == "🟩" and r < 3:
                    if l[r + random.randint(1, 2)][c] == "🟩":
                        l[r][c] = "🟫"

        l.reverse()
        embed = discord.Embed(description="\n".join(["".join(i) for i in l]), color=random.randint(0, 16777215))
        await ctx.send(embed=embed)


    @commands.command(aliases=["brewcoffee", "makecoffee"])
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def coffee(self, ctx, member: discord.Member = None, *, msg=None):
        """ Your morning coffee, for you or for anyone else """

        if member == None:
            await ctx.send("Brewing you some coffee...")
            await asyncio.sleep(random.randint(15, 25))
            await ctx.send(f"Here's your coffee {ctx.author.mention}, enjoy!")
            await ctx.send("☕")
        elif member.bot == True:
            await ctx.send("That user is a bot, it won't be able to enjoy the coffee.")
        else:
            await ctx.send(f"Brewing some coffee for {member}...")
            await asyncio.sleep(random.randint(15, 25))
            await ctx.send(f"Done! Sending ☕ to {member} now!")
            message = f"{ctx.message.author} sent you some coffee! Enjoy!"
            if not msg == None:
                message += f"\nMessage: `{msg}`"
            await member.send(message)
            await member.send("☕")

    @commands.command(aliases=["cuppatea", "maketea"])
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def tea(self, ctx, member: discord.Member = None, *, msg=None):
        """ Herbal tea or black tea? Made for you or for someone else """

        if member == None:
            await ctx.send("Making you some tea...")
            await asyncio.sleep(random.randint(15, 25))
            await ctx.send(f"Here's your tea {ctx.author.mention}, enjoy!")
            await ctx.send("🍵")
        elif member.bot == True:
            await ctx.send("That user is a bot, it won't be able to enjoy the tea.")
        else:
            await ctx.send(f"Making some tea for {member}...")
            await asyncio.sleep(random.randint(15, 25))
            await ctx.send(f"Done! Sending 🍵 to {member} now!")
            message = f"{ctx.message.author} sent you some tea! Enjoy!"
            if not msg == None:
                message += f"\nMessage: `{msg}`"
            await member.send(message)
            await member.send("🍵")


    @commands.command(aliases=["wrap", "bubbles", "bubblewrap"])
    async def pop(self, ctx):
        """ Ever felt the sudden urge to get some bubble wrap and just spend your entire day on it? """

        pops = ""
        message = ""
        for foo in range(30):
            pops += "||pop||"
        for foo in range(6):
            message += pops + "\n"
        await ctx.send("Here, have some virtual bubble wrap!\n" + message)


    @commands.command(aliases=["casualfishing", "casualfish"])
    @commands.cooldown(1, 40, commands.BucketType.user)
    async def fish(self, ctx):
        """
        Cast your rod.
        Enjoy the wait
        """

        if random.randint(1, 10) > 6:
            thechoice = random.choice([1, 2, 3, 10, 12, 13, 14])
        elif random.randint(1, 10) > 3:
            thechoice = random.choice([15, 16, 17, 18, 19])
        else:
            thechoice = random.choice([4, 5, 6, 7, 8, 9, 11])

        msg = await ctx.send("Setting up fishing rod...")
        msg2 = await ctx.send("🎣")
        await asyncio.sleep(random.randint(5, 10))
        await msg.edit(content="Waiting for fish...")
        await asyncio.sleep(random.randint(20, 30))
    # Regular
        if thechoice == 1 or thechoice == 13:
            await msg.edit(content=f"You caught a fish, {ctx.message.author.mention}!")
        elif thechoice == 2 or thechoice == 12 or thechoice == 14:
            await msg.edit(content=f"You caught a tropical fish, {ctx.message.author.mention}!")
        elif thechoice == 3:
            await msg.edit(content=f"You caught a pufferfish, {ctx.message.author.mention}!")
        elif thechoice == 10:
            await msg.edit(content=f"You caught a shrimp, {ctx.message.author.mention}. Cool!")
    # Rarer
        if thechoice == 4:
            await msg.edit(content=f"You caught a shark, how {ctx.message.author.mention}??")
        elif thechoice == 5:
            await msg.edit(content=f"You caught a dolphin, {ctx.message.author.mention}! interesting")
        elif thechoice == 6:
            await msg.edit(content=f"Oh wow, you caught a whale, {ctx.message.author.mention}!")
        elif thechoice == 7:
            await msg.edit(content=f"You caught an octopus {ctx.message.author.mention}, that's cool I guess")
        elif thechoice == 8:
            await msg.edit(content=f"You caught an squid {ctx.message.author.mention}, that's cool I guess")
        elif thechoice == 9:
            await msg.edit(content=f"You caught a crab {ctx.message.author.mention}, watch out for those pincers!")
        elif thechoice == 11:
            await msg.edit(content=f"You caught a lobster {ctx.message.author.mention}, that's worth a whole dinner!")
    # Non-fish
        elif thechoice == 12:
            await msg.edit(content=f"You caught a boot {ctx.message.author.mention}, better luck next time I guess")
        elif thechoice == 13:
            await msg.edit(content=f"You caught an oyster {ctx.message.author.mention}, mmmmmm")
        elif thechoice == 14:
            await msg.edit(content=f"You caught a pirate flag {ctx.message.author.mention}, um interesting")
        elif thechoice == 15:
            await msg.edit(content=f"You caught a broken cell phone {ctx.message.author.mention}, um interesting")
        elif thechoice == 16:
            await msg.edit(content=f"You did not catch anything this time {ctx.message.author.mention}, better luck next time!")
        await msg2.edit(content=self.fishes[thechoice])


    @commands.command(aliases=["piza", "pepperoni", "piz"])
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def pizza(self, ctx):
        """ It's pizza time. """

        wait = random.randint(15, 30)
        await ctx.send("Your pizza is being delivered, please wait 15-30 seconds\n🚗", delete_after=wait)
        await asyncio.sleep(wait)
        slice = 0
        msg = await ctx.send(self.pizzaframes[slice])
        await msg.add_reaction("🍕")
        def check(reaction, user):
            return str(reaction.emoji) == "🍕" and user.id != 743131027786170509 and reaction.message == msg
        for i in range(9):
            try:
                reaction, user = await self.client.wait_for("reaction_add", timeout=300.0, check=check)
            except asyncio.TimeoutError:
                await msg.clear_reactions()
            else:
                slice += 1
                await msg.edit(content=self.pizzaframes[slice].replace("⬛", "<:__:1028468329456865310>"))
                await reaction.remove(user)
        await msg.clear_reactions()


    @commands.command(aliases=["football", "ball"])
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def soccer(self, ctx, against="4"):
        """
        A small game of soccer. Except your teammates have abandoned you!
        Details inside.
        """

        try:
            against = int(against)
        except ValueError:
            against = 4
        else:
            if against < 0 or against > 84:
                against = 4

        field = [[0 for i in range(21)] for i in range(7)]
        field[3][1] = 1
        field[3][19] = 3
        field[2][20], field[3][20], field[4][20] = (4, 4, 4)
        you = [3, 1]
        goalie = [3, 19]

        enms = []
        for i in range(against):
            row = random.randint(0, 6)
            column = random.randint(6, 17)
            while field[row][column] == 2:
                row = random.randint(0, 6)
                column = random.randint(6, 17)
            field[row][column] = 2
            enms.append([row, column])

        def emojify(i):
            convert = {0: "🟩", 1: "🟨", 2: "🟥", 3: "⬛", 4: "⬜", 5: "🔳"}
            return convert[i]

        fieldmap = "\n".join(["".join(list(map(emojify, i))) for i in field])

        if ctx.invoked_with == "soccer":
            name = "SOCCER"
        elif ctx.invoked_with == "football":
            name = "FOOTBALL"
        else:
            if ctx.guild.region in (discord.VoiceRegion.japan,
                                    discord.VoiceRegion.southafrica,
                                    discord.VoiceRegion.sydney,
                                    discord.VoiceRegion.us_central,
                                    discord.VoiceRegion.us_east,
                                    discord.VoiceRegion.us_south,
                                    discord.VoiceRegion.us_west,
                                    discord.VoiceRegion.vip_us_east,
                                    discord.VoiceRegion.vip_us_west):
                name = "SOCCER"
            else:
                name = "FOOTBALL"

        embed = discord.Embed(colour=0x2ecc71)
        embed.set_author(name=f"⚽ {name}")
        embed.add_field(name="CONTROLS", value="""Use arrows to move and ⚽ to shoot
Avoid opponents and shoot past the goalie
Opponents cannot move diagonally and will randomly slow down
The goalie is more likely to block the ball the further away you are from it""", inline=False)
        embed.add_field(name="_ _", value=f"🟩 = field\n🟨 = you\n🟥 = opponents\n⬛ = goalie\n⬜ = goal net", inline=False)
        embed.add_field(name="_ _", value=fieldmap, inline=False)
        embed.set_footer(text="Turn 1")
        m = await ctx.send(embed=embed)

        view = discord.ui.View()
        nw = discord.ui.Button(label="↖", style=discord.ButtonStyle.grey, row=0)
        n = discord.ui.Button(label="⬆", style=discord.ButtonStyle.grey, row=0)
        ne = discord.ui.Button(label="↗", style=discord.ButtonStyle.grey, row=0)
        w = discord.ui.Button(label="⬅", style=discord.ButtonStyle.grey, row=1)
        kick = discord.ui.Button(label="⚽", style=discord.ButtonStyle.green, row=1)
        e = discord.ui.Button(label="➡", style=discord.ButtonStyle.grey, row=1)
        sw = discord.ui.Button(label="↙", style=discord.ButtonStyle.grey, row=2)
        s = discord.ui.Button(label="⬇", style=discord.ButtonStyle.grey, row=2)
        se = discord.ui.Button(label="↘", style=discord.ButtonStyle.grey, row=2)
        stop = discord.ui.Button(label="⏹", style=discord.ButtonStyle.red, row=2)

        opts = ("➡", "↗", "↘", "⬆", "⬇", "↖", "↙", "⬅", "⚽", "⏹")
        for i in opts:
            await m.add_reaction(i)

        def check(reaction, user):
            return reaction.emoji in opts and user == ctx.author and reaction.message == m

        async def gameover(outcome):
            if outcome in (0, "l", "lose"):
                embed.colour = 0xe74c3c
                embed.remove_field(0)
                embed.set_field_at(0, name="GAME OVER", value="You lost...\n`0` - `1`", inline=False)
                embed.set_field_at(-1, name="_ _", value=fieldmap, inline=False)
                embed.set_footer(text=f"Turn {turn}")
                await m.edit(embed=embed)
                await m.clear_reactions()
            else:
                embed.colour = 0x2ecc71
                embed.remove_field(0)
                embed.set_field_at(0, name="GAME OVER", value="You won! 🏆\n`1` - `0`", inline=False)
                embed.set_field_at(-1, name="_ _", value=fieldmap, inline=False)
                embed.set_footer(text=f"Turn {turn}")
                await m.edit(embed=embed)
                await m.clear_reactions()

        turn = 1
        while True:
            turn += 1
            try:
                reaction, user = await self.client.wait_for("reaction_add", check=check, timeout=120.0)
            except asyncio.TimeoutError:
                await m.clear_reactions()
                break

            op = reaction.emoji
            await reaction.remove(user)

            if op == "⏹":
                await m.clear_reactions()
                break

            field[you[0]][you[1]] = 0
            if op in ("➡", "↗", "↘"):
                if you[1] > 16:
                    if op == "➡" or (op == "↗" and you == [0, 15]) or (op == "↘" and you == [6, 15]):
                        turn -= 1
                        continue
                else:
                    you[1] += 1
            if op in ("⬆", "↖", "↗"):
                if you[0] < 1:
                    if op == "⬆" or (op == "↖" and you == [0, 0]) or (op == "↗" and you == [0, 15]):
                        turn -= 1
                        continue
                else:
                    you[0] -= 1
            if op in ("⬅", "↖", "↙"):
                if you[1] < 1:
                    if op == "⬅" or (op == "↖" and you == [0, 0]) or (op == "↙" and you == [6, 0]):
                        turn -= 1
                        continue
                else:
                    you[1] -= 1
            if op in ("⬇", "↙", "↘"):
                if you[0] > 5:
                    if op == "⬇" or (op == "↙" and you == [6, 0]) or (op == "↘" and you == [6, 15]):
                        turn -= 1
                        continue
                else:
                    you[0] += 1

            if op == "⚽":
                rolled = 1
                field[goalie[0]][goalie[1]] = 0
                if you[1] < 10:
                    if you[0] in (0, 1, 2):
                        goalie[0] = 2
                    elif you[0] in (4, 5, 6):
                        goalie[0] = 4
                    else:
                        goalie[0] = 3
                elif you[1] < 14:
                    if goalie[0] in (2, 4):
                        goalie[0] = 3
                    else:
                        goalie[0] += random.choice([-1, 1])
                else:
                    pass
                field[goalie[0]][goalie[1]] = 3
                ball = [you[0], you[1]]
                outcome = 0
                while True:
                    rolled += 1
                    field[ball[0]][ball[1]] = 0
                    ball[1] += 1
                    field[you[0]][you[1]] = 1
                    if rolled % 2 == 0:
                        for i in range(len(enms)):
                            if (enms[i][0] - ball[0], enms[i][1] - ball[1]) == (0, 0):
                                fieldmap = "\n".join(["".join(list(map(emojify, i))) for i in field])
                                await gameover(0)
                                break
                            elif ball[1] > enms[i][1]:
                                field[enms[i][0]][enms[i][1]] = 0
                                if field[enms[i][0]][enms[i][1] + 1] not in (1, 2):
                                    enms[i][1] += 1
                                else:
                                    enms[i][0] += random.choice((-1, 1))
                                field[enms[i][0]][enms[i][1]] = 2
                            else:
                                field[enms[i][0]][enms[i][1]] = 0
                                if ball[0] > enms[i][0]:
                                    if field[enms[i][0] + 1][enms[i][1]] not in (1, 2):
                                        enms[i][0] += 1
                                elif ball[0] < enms[i][0]:
                                    if field[enms[i][0] - 1][enms[i][1]] not in (1, 2):
                                        enms[i][0] -= 1
                                else:
                                    pass
                                field[enms[i][0]][enms[i][1]] = 2
                    if field[ball[0]][ball[1]] in (2, 3):
                        outcome = 0
                        break
                    elif field[ball[0]][ball[1]] == 4:
                        field[ball[0]][ball[1]] = 5
                        outcome = 1
                        break
                    elif ball[1] > 19:
                        field[ball[0]][ball[1]] = 5
                        outcome = 0
                        break
                    else:
                        field[ball[0]][ball[1]] = 5

                    fieldmap = "\n".join(["".join(list(map(emojify, i))) for i in field])
                    embed.set_field_at(2, name="_ _", value=fieldmap, inline=False)
                    await m.edit(embed=embed)
                    await asyncio.sleep(1)

                fieldmap = "\n".join(["".join(list(map(emojify, i))) for i in field])
                await gameover(outcome)
                break

            for i in range(len(enms)):
                if random.randint(1, 6) == 1:
                    continue

                distr = enms[i][0] - you[0]
                distc = enms[i][1] - you[1]
                if (distr, distc) == (0, 0):
                    fieldmap = "\n".join(["".join(list(map(emojify, i))) for i in field])
                    await gameover(0)
                    break
                elif abs(distr) > abs(distc):
                    if field[enms[i][0] - int(distr / abs(distr))][enms[i][1]] != 2:
                        field[enms[i][0]][enms[i][1]] = 0
                        enms[i][0] -= int(distr / abs(distr))
                        field[enms[i][0]][enms[i][1]] = 2
                else:
                    if field[enms[i][0]][enms[i][1] - int(distc / abs(distc))] != 2:
                        field[enms[i][0]][enms[i][1]] = 0
                        enms[i][1] -= int(distc / abs(distc))
                        field[enms[i][0]][enms[i][1]] = 2

            if field[you[0]][you[1]] != 2:
                field[you[0]][you[1]] = 1
            else:
                field[you[0]][you[1]] = 2
                fieldmap = "\n".join(["".join(list(map(emojify, i))) for i in field])
                await gameover(0)
                break

            field[goalie[0]][goalie[1]] = 0
            if goalie[0] in (2, 4):
                goalie[0] = 3
            else:
                goalie[0] += random.choice([-1, 1])
            field[goalie[0]][goalie[1]] = 3

            fieldmap = "\n".join(["".join(list(map(emojify, i))) for i in field])

            embed.set_field_at(2, name="_ _", value=fieldmap, inline=False)
            embed.set_footer(text=f"Turn {turn}")
            await m.edit(embed=embed)


    @commands.command(name="tilegame", aliases=["tilesgame"])
    @commands.cooldown(2, 20, commands.BucketType.user)
    @commands.is_owner()
    async def tilegame(self, ctx, do_you_want_help=""):
        """ THIS COMMAND HAS BEEN RETIRED due to internal limits. """

        return

        if do_you_want_help.lower() in ("yes", "help", "h", "y"):
            await ctx.send("""**Welcome to Tiles!**
🟥 tiles will start falling in every column.
Once they hit the 🟩 line, react with their column number.
The game ends once you miss a 🟥 tile or when you hit a wrong column.
Once a 🟥 tile hits the 🟩 line, you should try to react as soon as you can.""")
            return

        if ctx.channel.id in self.tilesbusy:
            await ctx.send("This command is already being used in this channel, try again later or in a different channel.")
            return

        field = [[0 for i in range(5)] for i in range(7)] # row, column      # y, x
        field[5][0], field[5][1], field[5][2], field[5][3], field[5][4] = (2, 2, 2, 2, 2)
        activetiles = []
        online = []

        clrs = []
        clrs += "🟥🟧🟨🟩🟦🟪🟫⬛⬜"

        def emojify(i):
            convert = {0: "<:__:1028468329456865310>", 1: "🟥", 2: "🟩", 3: "🟨", 4: "❎"}
            return convert[i]

        fieldmap = "1️⃣2️⃣3️⃣4️⃣5️⃣\n" + "\n".join(["".join(list(map(emojify, i))) for i in field])
        embed = discord.Embed(colour=random.randint(0, 16777215))
        embed.set_author(name=f"{random.choice(clrs)} TILES")
        embed.add_field(name="_ _", value=fieldmap, inline=False)
        embed.set_footer(text="Score: 0")
        m = await ctx.send(content="Use `sytiles help` for info on how to play.", embed=embed)

        opts = ("1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "⏹")
        for i in opts:
            await m.add_reaction(i)

        async def gameover():
            embed = discord.Embed(colour=random.randint(0, 16777215))
            embed.set_author(name=f"{random.choice(clrs)} TILES")
            embed.add_field(name="GAME OVER", value=f"Final score: `{score}`", inline=False)
            embed.add_field(name="_ _", value=fieldmap, inline=False)
            embed.set_footer(text=f"Score: {score}")
            await m.edit(content="Use `sytiles help` for info on how to play.", embed=embed)
            await m.clear_reactions()

        end = False
        score = 0
        self.tilesbusy.add(ctx.channel.id)
        while True:
            on_line = []
            await asyncio.sleep(0.2)

            field = [[0 for i in range(5)] for i in range(7)] #row, column      #y, x
            field[5][0], field[5][1], field[5][2], field[5][3], field[5][4] = (2, 2, 2, 2, 2)

            for tile in activetiles:
                if tile[0] == 5:
                    on_line = [tile[1]]

            m = await ctx.channel.fetch_message(m.id)
            chosen = [await m.reactions[0].users().flatten(),
            await m.reactions[1].users().flatten(),
            await m.reactions[2].users().flatten(),
            await m.reactions[3].users().flatten(),
            await m.reactions[4].users().flatten()]
            askstop = await m.reactions[5].users().flatten()
            if ctx.author in askstop:
                await gameover()
                end = True
                break

            for i, j in enumerate(chosen):
                if ctx.author in j:
                    await m.reactions[i].remove(ctx.author)
                    if i in on_line:
                        for k in activetiles:
                            if k[0] == 5 and k[1] == i:
                                activetiles[activetiles.index(k)][2] = 3
                                score += 1
                    else:
                        field[5][i] = 4
                        for tile in activetiles:
                            field[tile[0]][tile[1]] = tile[2]
                        fieldmap = "1️⃣2️⃣3️⃣4️⃣5️⃣\n" + "\n".join(["".join(list(map(emojify, i))) for i in field])
                        await gameover()
                        end = True
                        break

            if end == True:
                break

            freezeactivetiles = activetiles[:]
            for tile in freezeactivetiles:
                if tile[0] < 6:
                    tile[0] += 1
                else:
                    activetiles.remove(tile)
                    if tile[2] == 1:
                        await gameover()
                        end = True
                        break
            if end:
                break

            col = random.randint(0, 5)
            if col != 5:
                activetiles.append([0, col, 1]) #row, column, state
            for tile in activetiles:
                field[tile[0]][tile[1]] = tile[2]

            fieldmap = "1️⃣2️⃣3️⃣4️⃣5️⃣\n" + "\n".join(["".join(list(map(emojify, i))) for i in field])
            embed = discord.Embed(colour=random.randint(0, 16777215))
            embed.set_author(name=f"{random.choice(clrs)} TILES")
            embed.add_field(name="_ _", value=fieldmap, inline=False)
            embed.set_footer(text=f"Score: {score}")
            await m.edit(content="Use `sytiles help` for info on how to play.", embed=embed)

        self.tilesbusy.remove(ctx.channel.id)


    @commands.command(aliases=["rest", "cafe", "café", "food", "resto"])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def restaurant(self, ctx, *, food=""):
        """ Eat & Chill """

        shown = "🍞 Bakery"
        items = {"🍞 Bakery": self.bakery, "🥤 Beverages": self.beverages,
                "🥞 Breakfast": self.breakfast, "🍱 Asian": self.asian,
                "🍭 Candyland": self.sweets, "🍦 Ice Creamery": self.icecreamery,
                "🌍 Foreign": self.foreign, "🍟 Fast Food": self.fastfood,
                "🍎 Farmer's Market": self.fruit, "💬 Other": self.other}

        if food == "":
            embed = discord.Embed(colour=random.randint(1, 16777215))
            embed.set_author(name=shown.upper())
            embed.description=f"""Welcome to Serpynth's restaurant!
We have many food categories here.
Use the reactions below to toggle between them.

Find something you like? Use `sy{ctx.invoked_with} <item>`!

_ _"""
            for i in items[shown]:
                embed.add_field(name=i.capitalize(), value=items[shown][i])
            m = await ctx.send(embed=embed)

            def check(reaction, user):
                if (reaction.emoji in [i[0] for i in items] or reaction.emoji == self.client.get_emoji(1028413024610041877)):
                    if reaction.message == m and user == ctx.author:
                        return True
                    else:
                        return False
                else:
                    return False

            for i in items:
                await m.add_reaction(i[0])

            await m.add_reaction("<:exit:1028413024610041877>")

            while True:
                try:
                    reaction, user = await self.client.wait_for("reaction_add", check=check, timeout=60.0)
                except asyncio.TimeoutError:
                    await m.clear_reactions()
                    break

                if reaction.emoji == self.client.get_emoji(1028413024610041877):
                    await m.clear_reactions()
                    break

                await reaction.remove(user)
                chosen = ""
                for i in items:
                    if i[0] == reaction.emoji:
                        shown = i

                embed.clear_fields()
                embed.set_author(name=shown.upper())
                for i in items[shown]:
                    embed.add_field(name=i.capitalize(), value=items[shown][i])
                await m.edit(embed=embed)

        else:
            ok = False
            for i in items:
                for j in items[i]:
                    if food.lower() == j:
                        ok = items[i][j]
                        break

            if ok == False:
                await ctx.send("I'm sorry, but I don't think we have that item here.")

            else:
                await ctx.send("Your order is being processed...")
                await asyncio.sleep(random.randint(10, 14))
                await ctx.send(f"Here's your `{food.lower()}`!")
                m = await ctx.send(ok)
                await m.add_reaction(ok)


    @commands.command(aliases=["chairsim", "chairsimulator", "sit"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def chair(self, ctx):
        """ Thrilling chair simulator, won Best Game Award in 1466 """

        start = time.time()

        embed = discord.Embed(color=discord.Colour.green())
        embed.set_author(name="CHAIR SIMULATOR")
        embed.description = self.regchair
        m = await ctx.send(embed=embed)

        await m.add_reaction("📱")
        await m.add_reaction("⌚")
        await m.add_reaction("😴")
        await m.add_reaction("🙆")
        await m.add_reaction("<:exit:1028413024610041877>")

        def check(reaction, user):
            return user == ctx.author and reaction.message == m and reaction.emoji in [
                                    self.client.get_emoji(1028413024610041877),
                                    "📱", "⌚", "😴", "🙆"]

        notifs = random.randint(0, 3)
        justwokenup = 0
        while True:
            reacted = False
            try:
                reaction, user = await self.client.wait_for("reaction_add", check=check, timeout=60.0)
            except asyncio.TimeoutError:
                embed.clear_fields()
                if random.randint(1, 30) == 1:
                    notifs += 1
                if random.randint(1, 240) == 1:
                    embed.add_field(name="_ _", value = "There is a spider on the wall.", inline=False)
                    await m.edit(embed=embed)
                if random.randint(1, 320) == 1:
                    embed.add_field(name="_ _", value="You\"re feeling a bit hungry.", inline=False)
                    await m.edit(embed=embed)
                if random.randint(1, 320) == 1:
                    embed.add_field(name="_ _", value="You\"re feeling a bit tired.", inline=False)
                    await m.edit(embed=embed)
                if random.randint(1, 400) == 1:
                    embed.add_field(name="_ _", value="You contemplate life.", inline=False)
                    await m.edit(embed=embed)
                if random.randint(1, 400) == 1:
                    embed.add_field(name="_ _", value="An soft breeze passes through the window.", inline=False)
                    await m.edit(embed=embed)
                if random.randint(1, 480) == 1:
                    embed.add_field(name="_ _", value="An ice cream truck passes by.", inline=False)
                    await m.edit(embed=embed)
                if justwokenup > 0:
                    justwokenup -= 1
            else:
                reacted = True
                embed.clear_fields()

            if not reacted:
                continue

            if reaction.emoji == self.client.get_emoji(1028413024610041877):
                embed.color = discord.Colour.gold()
                hrs = "{:,}".format(round((time.time() - start) // 3600))
                min = round((time.time() - start) % 3600 // 60)
                sec = round((time.time() - start) % 60)
                embed.add_field(name="You left the chair", value=f"You sat on the chair for `{hrs}h`, `{min}m` and `{sec}s`!")
                embed.description = self.emptychair
                await m.edit(embed=embed)
                await reaction.remove(user)
                return

            elif reaction.emoji == "📱":
                await m.clear_reactions()
                embed.description = self.phonechair
                embed.add_field(name="_ _",
                            value=f"You check your phone.\nYou have `{'{:,}'.format(notifs)}` new notification{'s' if notifs != 1 else ''}.")
                await m.edit(embed=embed)
                await asyncio.sleep(7.0)
                embed.description = self.regchair
                embed.clear_fields()
                await m.edit(embed=embed)
                await reaction.remove(user)
                notifs = 0

            elif reaction.emoji == "⌚":
                await m.clear_reactions()
                embed.description = self.watchchair

                hrs = "{:,}".format(round((time.time() - start) // 3600))
                min = round((time.time() - start) % 3600 // 60)
                sec = round((time.time() - start) % 60)
                now = int(time.time() // 1) + 14400
                embed.add_field(name="_ _",
                            value=f"The time (UTC) is <t:{now}:T>.\nYou have been sitting on the chair for `{hrs}h`, `{min}m` and `{sec}s`.")
                await m.edit(embed=embed)

                await asyncio.sleep(7.0)
                embed.description = self.regchair
                embed.clear_fields()
                await m.edit(embed=embed)
                await reaction.remove(user)

            elif reaction.emoji == '😴':
                if justwokenup > 0:
                    embed.add_field(name="_ _",
                                value=f"You are unable to fall asleep right now.")
                    await m.edit(embed=embed)
                    await asyncio.sleep(4.0)
                    embed.clear_fields()
                    await m.edit(embed=embed)
                    await reaction.remove(user)
                else:
                    await m.clear_reactions()
                    embed.description = self.napchair
                    embed.add_field(name="_ _",
                                value=f"You close your eyes for a bit.")
                    await m.edit(embed=embed)
                    sleepfor = random.randint(15, 25)
                    await asyncio.sleep(sleepfor)
                    embed.description = self.regchair
                    embed.clear_fields()
                    await m.edit(embed=embed)
                    await reaction.remove(user)
                    start -= round(sleepfor / 1.5, 2)
                    justwokenup = 2

            elif reaction.emoji == "🙆":
                await m.clear_reactions()
                embed.add_field(name="_ _",
                            value=f"You stretch a bit.")
                for i in range(random.randint(3, 4)):
                    embed.description = self.upchair
                    await m.edit(embed=embed)
                    await asyncio.sleep(2)
                    embed.description = self.outchair
                    await m.edit(embed=embed)
                    await asyncio.sleep(2)
                embed.description = self.regchair
                embed.clear_fields()
                await m.edit(embed=embed)
                await reaction.remove(user)

            await m.add_reaction("📱")
            await m.add_reaction("⌚")
            await m.add_reaction("😴")
            await m.add_reaction("🙆")
            await m.add_reaction("<:exit:1028413024610041877>")

async def setup(client):
    await client.add_cog(Chill(client))
