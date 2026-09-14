import discord
import json
import datetime
import math
import time
from discord.ext import tasks
from discord.ext import commands
from discord.utils import get
import random
import asyncio


#########################################################
######{ id: [doubloons, {'item': quantity}, hp, {'effect': time}, {'item': cooldown_time}, deadtime(None)] }
######channel must be named "arena"
#########################################################

class Arena(commands.Cog, name="⚔ Arena", description="""
Welcome to the Arena! Use `syguide` for more help on this group of commands.
These commands allow you to collect money (doubloons), buy weapons and items,
and battle others.
"""):
    def __init__(self, client):
        self.client = client

        itemstatsfile = open("shop.json", "r")
        self.itemstats = json.load(itemstatsfile)
        itemstatsfile.close()

        self.effecticons = {"heal": "🩹",
                        "flame": "🔥",
                        "freeze": "❄",
                        "crit": "💥",
                        "poison": "🧪",
                        "stun": "💫"}

        self.effectunits = {"heal": "hp",
                        "flame": "",
                        "freeze": "s",
                        "crit": "%",
                        "poison": "mins",
                        "stun": "s"}


        def plural(word):
            word = word.lower()
            chars = []
            chars += word.lower()

            pluralizations = {"craft": "",
                              "man": "--en",
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
                          "piano": "pianos", "halo": "halos", "human": "humans"}

            if word in ("sheep", "series", "species", "deer", "moose", "fish", "swine", "buffalo", "shrimp", "trout"):
                return word
            elif word in exceptions:
                return exceptions[word]
            else:
                for key in pluralizations:
                    if word.endswith(key):
                        for i in pluralizations[key]:
                            if i == "-":
                                chars.pop(-1)
                            else:
                                chars.append(i)
                        return word


    @tasks.loop(seconds=10)
    async def timers(self):
        readdoc = open("invs.txt", "r")
        dict = eval(readdoc.read())
        readdoc.close()
        for i in dict:
            for j in dict[i][3]:
                if dict[i][3][j] < time.time():
                    del dict[i][3][j]
            for k in dict[i][4]:
                if dict[i][4][k] < time.time():
                    del dict[i][4][k]
        writedoc = open("invs.txt", "w")
        writedoc.write(str(dict))
        writedoc.close()


    @timers.before_loop
    async def before_timers(self):
        await self.client.wait_until_ready()


    def cog_unload(self):
        self.timers.cancel()


    @commands.command(aliases=["bal", "bank", "doubs", "doubloons"], help="checks how much money you have")
    async def balance(self, ctx, member: discord.Member = None):
        if member == None:
            member = ctx.author
        readdoc = open("invs.txt", "r")
        dict = eval(readdoc.read())
        readdoc.close()
        try:
            dict[member.id]
        except KeyError:
            dict[member.id] = [0, {}, 100, {}, {}, None]
        await ctx.send(f"{member.mention} has `${'{:,}'.format(dict[member.id][0])}`. {'🪙' if dict[member.id][0] > 0 else ''}")


    @commands.command(aliases=["inv", "bag", "items", "backpack"], help="looks at all items you currently have")
    async def inventory(self, ctx, member: discord.Member = None):
        if member == None:
            member = ctx.author
        readdoc = open("invs.txt", "r")
        dict = eval(readdoc.read())
        readdoc.close()
        try:
            dict[member.id]
        except KeyError:
            dict[member.id] = [0, {}, 100, {}, {}, None]
        inv = dict[member.id][1]
        send = ""
        for i in inv:
            send += f"{i} x{inv[i]}\n"
        await ctx.send(f"{member.mention}'s inventory:\n```prolog\n{send}{' ' if len(inv) < 1 else ''}```")


    @commands.command(aliases=["mystats", "stats"], help="shows someone\"s Arena stats")
    async def userstats(self, ctx, member: discord.Member = None):
        if member == None:
            member = ctx.author
        readdoc = open("invs.txt", "r")
        dict = eval(readdoc.read())
        readdoc.close()
        try:
            dict[member.id]
        except KeyError:
            dict[member.id] = [0, {}, 100, {}, {}, None]
        stats = dict[member.id]
        embed = discord.Embed(color=random.randint(0, 16777215))
        embed.set_author(name=f"{member}", icon_url=member.avatar.url)
        embed.description = f"""Balance: `${stats[0]}`
Item variety in inventory: `{len(stats[1])}`
HP: `{stats[2]}/100`
Dead?: `{False if stats[5] == None else True}`"""
        embed.set_footer(text="Use syuserinfo for non-arena based stats")
        await ctx.send(embed=embed)


    @commands.command(aliases=["purchase"], help="buy a weapon or item with your doubloons")
    async def buy(self, ctx, id=None, quantity="1"):
        quantity = int(quantity)
        if id == None:
            await ctx.invoke(self.shop, search="1")
        else:
            readdoc = open("invs.txt", "r")
            dict = eval(readdoc.read())
            readdoc.close()
            try:
                dict[ctx.author.id]
            except KeyError:
                dict[ctx.author.id] = [0, {}, 100, {}, {}, None]

            found = False
            for i in self.itemstats:
                item = self.itemstats[i]
                if item["id"] == id:
                    found = True
                    break

            if found == False:
                await ctx.send(f"Item ID `{id}` not found.")
            elif quantity == 1:
                if dict[ctx.author.id][0] < item['cost']:
                    await ctx.send(f"""You do not have enough to buy `{id}`!
You currently have `${dict[ctx.author.id][0]}`
`{id}` costs `${item["cost"]}`
You need `${item["cost"] - dict[ctx.author.id][0]}` more to buy this item.""")
                else:
                    dict[ctx.author.id][0] -= item["cost"]
                    if i in dict[ctx.author.id][1]:
                        dict[ctx.author.id][1][i] += item["uses"]
                    else:
                        dict[ctx.author.id][1][i] = item["uses"]
                    await ctx.send(f"Successfully purchased `{id}`.\nYou now have `${dict[ctx.author.id][0]}`")
                    writedoc = open("invs.txt", "w")
                    writedoc.write(str(dict))
                    writedoc.close()
            else:
                if dict[ctx.author.id][0] < item['cost'] * quantity:
                    await ctx.send(f"""You do not have enough to buy `{quantity}` `{self.plural(id)}`!
You currently have `${dict[ctx.author.id][0]}`
`{quantity}` `{self.plural(id)}` cost `${item["cost"] * quantity}`
You need `${item["cost"] * quantity - dict[ctx.author.id][0]}` more to buy this item.""")
                else:
                    dict[ctx.author.id][0] -= item["cost"] * quantity
                    if i in dict[ctx.author.id][1]:
                        dict[ctx.author.id][1][i] += item["uses"] * quantity
                    else:
                        dict[ctx.author.id][1][i] = item["uses"] * quantity
                    await ctx.send(f"Successfully purchased {quantity} `{self.plural(id)}`.\nYou now have `${dict[ctx.author.id][0]}`")
                    writedoc = open("invs.txt", "w")
                    writedoc.write(str(dict))
                    writedoc.close()


    # ~1.2 per dig
    @commands.command(aliases=["shovel"], help="the best way to collect doubloons")
    #@commands.is_owner()
    @commands.cooldown(2, 3600, commands.BucketType.user)
    async def dig(self, ctx):
        readdoc = open("invs.txt", "r")
        dict = eval(readdoc.read())
        readdoc.close()
        try:
            dict[ctx.author.id]
        except KeyError:
            dict[ctx.author.id] = [0, {}, 100, {}, {}, None]

        get = random.choices([0, 1, 2, 3, 4], [11, 10, 8, 4, 1])[0]
        await ctx.send(f"""You dug up `{get}` doubloon{"s" if get != 1 else ""}{"! 🪙" if get > 0 else "."}
You now have `{"{:,}".format(dict[ctx.author.id][0] + get)}` doubloons.""")
        dict[ctx.author.id][0] += get

        writedoc = open("invs.txt", "w")
        writedoc.write(str(dict))
        writedoc.close()


    @commands.command(aliases=["attack"], help="use items on yourself or someone else")
    @commands.is_owner()
    async def use(self, ctx, itemused, member: discord.Member = None):
        if member == None:
            member = ctx.author
        readdoc = open("invs.txt", "r")
        dict = eval(readdoc.read())
        readdoc.close()
        try:
            dict[ctx.author.id]
        except KeyError:
            dict[ctx.author.id] = [0, {}, 100, {}, {}, None]
        me = dict[ctx.author.id]
        try:
            dict[member.id]
        except KeyError:
            dict[member.id] = [0, {}, 100, {}, {}, None]
        you = dict[member.id]

        item = None
        for i in self.itemstats:
            if self.itemstats[i]["id"] == itemused:
                itemname = i
                itemid = self.itemstats[i]["id"]
                item = self.itemstats[i]
                break

        def getitem(id):
            for i in self.itemstats:
                if self.itemstats[i]["id"] == id:
                    return i
                    break
            return None

        if item == None:
            await ctx.send(f"Item ID `{itemused}` does not exist.")
        elif me[1] == {}:
            await ctx.send("You do not have anything, what are you gonna do?")
        elif you[0] == 0 and you[1] == {}:
            await ctx.send(f"`{member}` does not have anything, what are you gonna achieve?")
        elif me[5] == None:
            await ctx.send("You are dead; you can't do anything.")
        elif you[5] == None:
            await ctx.send(f"`{member}` is already dead.")
        elif me[1][itemname] < 1:
            await ctx.send(f"You do not own `{itemid}`.")
        elif (item["requires"] != None) and item["requires"] not in me[2]:
            await ctx.send(f"This item requires you to have `{item['requires']}`. Go `sybuy` it.")
        elif itemname in me[4]:
            await ctx.send("This item is on cooldown.")
        elif (item["requires"] != None):
            if getitem(item["requires"]) in me[4]:
                await ctx.send("The item this requires is on cooldown.")
        elif "stun" in me[3]:
            await ctx.send("You are currently stunned.")
        else:
            me[1][itemname] -= 1
            me[4][itemname] = time.time() + item["cooldown"]
            if me[1][itemname] > 1:
                del me[1][itemname]

            if item["type"] == "self":
                me[2] -= item["damage"]
                if "heal" in item["effects"]:
                    me[2] += item["effects"]["heal"]
                if "flame" in item["effects"]:
                    me[2] -= random.randint(0, item["effects"]["flame"])
                if "crit" in item["effects"]:
                    if random.randint(1, 100) <= item["effects"]["crit"]:
                        me[2] -= item["damage"]
                        time.time()
                if "poison" in item["effects"]:
                    me[3]["poison"] = time.time() + (item["effects"]["poison"] * 60)
                if "stun" in item["effects"]:
                    me[3]["stun"] = time.time() + item["effects"]["stun"]
                if "freeze" in item["effects"]:
                    me[3]["freeze"] = time.time() + item["effects"]["freeze"]
            elif item["type"] == "munition":
                await ctx.send("""This item is munition; it cannot be used by itself.
Instead, `syuse` something that requires this item. For example, if you're trying to use a bow, use `syuse arrow`.""")
            else:
                you[2] -= item["damage"]
                if "heal" in item["effects"]:
                    you[2] += item["effects"]["heal"]
                if "flame" in item["effects"]:
                    you[2] -= random.randint(0, item["effects"]["flame"])
                if "crit" in item["effects"]:
                    if random.randint(1, 100) <= item["effects"]["crit"]:
                        you[2] -= item["damage"]
                        time.time()
                if "poison" in item["effects"]:
                    you[3]["poison"] = time.time() + (item["effects"]["poison"] * 60)
                if "stun" in item["effects"]:
                    you[3]["stun"] = time.time() + item["effects"]["stun"]
                if "freeze" in item["effects"]:
                    you[3]["freeze"] = time.time() + item["effects"]["freeze"]
            writedoc = open("invs.txt", "w")
            writedoc.write(str(dict))
            readdoc.close()
######{ id: [doubloons, {"item": quantity}, hp, {"effect": time}, {"item": cooldown_time}, deadtime(None)] }


    @commands.command(aliases=["market", "store"], help="visits the store, see what you can buy")
    async def shop(self, ctx, *, search="1"):
        try:
            int(search)
        except:
            method = "search"
        else:
            method = "page"
        embed = discord.Embed(color=random.randint(0, 16777215))
        embed.set_author(name="SERPYNTH'S SHOP", icon_url="https://cdn.discordapp.com/attachments/749006528182353988/779172326699958292/snek.png")

        if method == "page":
            totalpages = math.ceil(len(self.itemstats) / 6)
            pagenum = int(search) if int(search) <= totalpages and int(search) > 0 else (totalpages if int(search) > totalpages else 1)
            embed.set_footer(text = f"Page {pagenum}/{totalpages}")
            page = list(self.itemstats.keys())[6 * (pagenum - 1): (6 * pagenum)]

            for i in page:
                item = self.itemstats[i]
                desc = f"Type: `{item['type']}`\nCost: `${item['cost']}`\nID: `{item['id']}`\nUses: `{item['uses']}`\nCooldown: `{item['cooldown']}s`"
                if item["damage"] > 0:
                    desc += f"\nDamage: `{item['damage']}`"
                if item["requires"] != None:
                    desc += f"\nRequires: `{item['requires']}`"
                for j in item["effects"]:
                    desc += f"\n{j.capitalize()} {self.effecticons[j]}: `{item['effects'][j]}{self.effectunits[j]}`"
                embed.add_field(name=f"{i}", value=desc)

        elif method == "search":
            items = []
            for i in self.itemstats:
                item = self.itemstats[i]
                if search.lower() in i.lower() or search.lower() in item["id"]:
                        items.append(i)
                        if len(items) > 5:
                            break

            for i in items:
                item = self.itemstats[i]
                desc = f"Type: `{item['type']}`\nCost: `${item['cost']}`\nID: `{item['id']}`\nUses: `{item['uses']}`\nCooldown: `{item['cooldown']}s`"
                if item["damage"] > 0:
                    desc += f"\nDamage: `{item['damage']}`"
                if item["requires"] != None:
                    desc += f"\nRequires: `{item['requires']}`"
                for j in item["effects"]:
                    desc += f"\n{j.capitalize()} {self.effecticons[j]}: `{item['effects'][j]}{self.effectunits[j]}`"
                embed.add_field(name=str(i), value=desc)

            if len(items) == 0:
                embed.add_field(name=f"No items found containing \"`{search}`\"", value="_ _")

        embed.add_field(name="".join(["\_" for ij in range(25)]),
                        value="All costs are in doubloons.\nUse `sybuy <ID>` to buy an item.\nUse `syguide` for other help.",
                        inline=False)
        await ctx.send(embed=embed)


    @commands.command(aliases=["arenahelp", "ahelp"], help="help on the Arena system")
    async def guide(self, ctx, *, page=""):
        if not page.lower() in ("commands", "shop", "currency", "doubloons", "battle", "stats", "effects"):
            await ctx.send("""**What topic do you need help with?**
```apache
Commands
Doubloons (currency)
Battle
Stats
Effects```
Use `syguide <topic>` to find help for a certain topic.
This is a guide for the arena system. If you want a list of all commands, use `syhelp` instead.
""")
        elif page.lower() in ("commands"):
            await ctx.send("""**COMMANDS**
`syguide <page>`
`sybalance <@member>` - Checks how many doubloons you, or someone else, currently has.
`syinventory <@member>` - Checks what items you, or someone else, currently has.
`sydig` - Dig for doubloons. You average 1.2 doubloons per dig.
`systats` - Gets the statistics about you or someone else: How many doubloons they have, their HP, etc.
`syshop <page>` - Visits the shop. Do `syshop <item>` to find info on a certain item or `syshop <page>` to find weapons on other pages.
`sybuy <ID> <quantity>` - Buys an item, with your doubloons, from the shop. You can find the ID of any item in "ID: `    `".
`syuse <ID> <@member>` - Uses an item that you own on another member, or if that item is meant to apply on yourself, it will automatically do so.
""")
        elif page.lower() in ("currency", "doubloons"):
            await ctx.send("""**DOUBLOONS**
Doubloons are Serpynth's main currency. You collect them by using `sydig`,
which averages 1.2 doubloons per use. Note that the command can only be used
twice per hour.

You can check how many doubloons you currently have by using `sybal`.
If you want to check anyone else's balance, use `sybal <@member>`.

You can spend your doubloons at the `syshop`, to buy weapons and battle other users.
Look for an item you want in the `syshop`, find its ID (which is in the stats), and
use `sybuy <ID>` to buy it. Of course, you will not be able to buy it if you don't
have enough doubloons.
""")
        elif page.lower() in ("battle"):
            await ctx.send("""**BATTLE**
Everyone starts with 100HP, meaning that people have to deal 100 damage to you to kill you.
Once you die, half of your doubloons go to the person who killed you, and you cannot participate in fights for 24 hours.
You also lose a total of 3 uses on random items in your inventory when you die.
Use `syuse <ID> <@member>` to use an item, subtracting 1 use from it. If it is a weapon, you will attack your opponent with it.
If you use an item that requires another item, both items will lose 1 use.
""")
        elif page.lower() in ("stats"):
            await ctx.send("""**ITEM STATS**
Every item has a set of stats, depending on what type of item it is.

**ITEM TYPES**
`weapon` - Used offensively, normally does damage to your opponent
`self` - Normally used defensively, effects apply to yourself
`munition` - Item whose only purpose is to allow some other items, who require it, to be used
`ammo` - Item that requires its `munition` to be used, e.g., `arrow` requires `bow`
`skill` - Item(?) that has a large or infinite number of uses

**EVERY ITEM HAS**
Type: `type` - The type of item it is: weapon, self, munition, ammo, etc. (More details above)
Cost: `$number` - How much it costs to buy that item
ID: `id` - The ID of the item, used in commands `sybuy <ID>` and `syuse <ID>`
Uses: `number` - The number of uses you get from the item per purchase, before it breaks
Cooldown `seconds` - The time, in seconds, that is required to wait before its next use

**WEAPONS OFTEN HAVE**
Damage: `number` - How much damage it inflicts to your opponent

**AMMOS OFTEN HAVE**
Damage: `number` - See above
Requires: `id` - The item, that is required to own, to be able to use this ammo

For information about effects, see `syguide effects`.
""")
        elif page.lower() in ("effects"):
            await ctx.send("""**EFFECTS**
Heal 🩹: `heal` - Heals the person who has been applied this item by `heal`
Flame 🔥: `max` - Does a random amount of extra damage from 0 to `max`
Freeze ❄: `duration` - Doubles the cooldown on all items of the receiver for `duration` seconds
Crit 💥: `percent` - Has a `percent`% chance of doing double damage
Poison 🧪: `duration` - Deals an extra 5 damage per minute for a total of `duration` minutes
Stun 💫: `duration` - Your opponent cannot use anything for `duration` seconds, and cooldowns will not go down during that time
Durable 💎: `percent` - Has a `percent`% chance of not losing a use after being used
""")


async def setup(client):
    await client.add_cog(Arena(client))
