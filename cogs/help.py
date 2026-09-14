from discord.ext import commands
import discord
import random
import asyncio


class Help(commands.Cog, name="ℹ Help", description="""
You new to the bot? You forgot how to use a command? This is the category for
you! `syhelp` is the main command here. Use `syhelp` to list all commands,
`syhelp <command>` to get help on a specific command.
"""):
    def __init__(self, client):
        self.client = client
        self.icons = ["https://cdn.discordapp.com/attachments/749006528182353988/779172326699958292/snek.png",
                    "https://cdn.discordapp.com/attachments/749006528182353988/828409546916495400/turtl.png",
                    "https://cdn.discordapp.com/attachments/749006528182353988/828409587547373619/appl.png",
                    "https://cdn.discordapp.com/attachments/749006528182353988/828409598926258256/egul.png",
                    "https://cdn.discordapp.com/attachments/749006528182353988/828412108005441577/elephont.png",
                    "https://cdn.discordapp.com/attachments/749006528182353988/828411632354590720/shork.png",
                    "https://cdn.discordapp.com/attachments/749006528182353988/863091531435081778/dregon.png"]


    @commands.command(aliases=['hewlp', 'help2', 'h2'], help='this command is no longer supported, use `syhelp` instead')
    async def oldhelp(self, ctx):
        embed = discord.Embed(color=random.randint(0, 16777215))
        embed.set_author(name='COMMANDS', url='https://youtu.be/dQw4w9WgXcQ', icon_url='https://cdn.discordapp.com/attachments/749006528182353988/779172326699958292/snek.png')
        embed.add_field(name='Utility ⚙', value='`autocommand`, `ban`, `clear`, `dice`, `giveaway`, `help`, `inviteinfo`, `kick`, `leaveserver`, `nick`, `profile`, `role`, `snipe`, `textchannel`, `timer`, `unban`, `voicechannel`, `weather`, `wolfram`')
        embed.add_field(name='Fun 🎢', value='`8ball`, `ascii`, `asciitext`, `borger`, `chat`, `checkpassword`, `funfact`, `gameoflife`, `hack`, `hangman`, `httpcat`, `icecream`, `library`, `mock`, `quiz`, `reddit`, `rick`, `rps`, `showerthoughts`, `swordfight`, `turnsbattle`, `turtl`, `xkcd`')
        embed.add_field(name='Music 🎶', value='`helloworld`, `join`, `jukebox`, `leave`, `pause`, `piano`, `play`, `resume`, `speak`, `stop`')
        embed.add_field(name='Chill 🌲', value='`camp`, `christmas`, `coffee`, `dontworry`, `fish`, `football`, `pizza`, `pop`, `soccer`, `tea`')
        embed.add_field(name='Other 💬', value='`about`, `f`, `friends`, `google`, `mimic`, `ping`, `plural`, `randomword`, `say`, `youtube`')
        embed.add_field(name='Unstable/Unfinished 🔧', value='`balance`, `browse`, `buy`, `dig`, `dlmp3`, `dlmp4`, `guide`, `inventory`, `nbibc`, `shop`, `use`')
        embed.add_field(name='Notes ℹ', value='This commands page is outdated. See `syhelp` for the updated commands page.')
        embed.set_footer(text=f'{ctx.message.author}')
        await ctx.send(embed=embed)


    @commands.command(aliases=["olderhelp", "help3", "dh", "h3"])
    @commands.is_owner()
    async def defaulthelp(self, ctx, *, page=""):
        """ Returns discord.py's default command help page. """

        thecmd = self.client.get_command(page)
        thecog = self.client.get_cog(page)
        if page == "":
            await ctx.send_help()
        else:
            if thecmd == None and thecog == None:
                page = page.split()[0]
                if len(ctx.message.role_mentions) + len(ctx.message.mentions) > 0 or "@everyone" in ctx.message.content:
                    page = "@invalid"
                await ctx.send(f"No command called \"{page}\" found.")
            else:
                if len(page.split()) > 1 and thecog == None:
                    page = page.split()[0]
                    if len(ctx.message.role_mentions) + len(ctx.message.mentions) > 0 or "@everyone" in ctx.message.content:
                        page = "@invalid"
                    await ctx.send(f"Command \"{page.lower()}\" has no subcommands.")
                else:
                    m = await ctx.send_help(page)


    @commands.command(aliases=["command", "cmd", "cmds", "commands"])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def help(self, ctx, *, page=""):
        """
        Returns a list of all commands.
        To get help on a specific category or command, use `syhelp <name>`. 
        """

        thecmd = self.client.get_command(page)

        cogmojis = {"help": "ℹ", "fun": "🎢", "utility": "⚙", "chill": "🌲",
        "images": "🖼", "music": "🎶", "arena": "⚔", "other": "💬",
        "debug": "🔧", "jishaku": "👾"}

        REMOVED = tuple()

        yeesnek = random.choices(self.icons, weights=[128, 16, 8, 4, 2, 1, 0.5])[0]
        embed = discord.Embed(color=random.randint(0, 16777215))
        embed.set_author(name="COMMANDS", icon_url=yeesnek)
        embed.set_footer(text=f"{ctx.message.author}")

        if thecmd != None:
            aliases = [thecmd.name]
            aliases.extend(thecmd.aliases)
            aliases = list(map(lambda x: f"`{x}`", aliases))
            cd = thecmd._buckets._cooldown
            if cd != None:
                cd = f"{cd.rate}/{round(cd.per)}s\n(uses per seconds)"
            canrun = True
            for i in thecmd.checks:
                try:
                    if await i(ctx) == False:
                        canrun = False
                        break
                except:
                    if i == False:
                        canrun = False
                        break

            params = list(map(lambda x: f"<{x}>", thecmd.clean_params))
            usage = f"`sy{page.lower()} " + " ".join(params) + "`" if len(params) > 0 else f"`sy{page.lower()}`"
            embed.add_field(name=f"__sy{page.lower()}__",
                            value=thecmd.help, inline=False)
            embed.add_field(name="__Category__",
                            value=thecmd.cog.qualified_name, inline=False)
            embed.add_field(name="__Usage__",
                            value=usage,
                            inline=False)
            embed.add_field(name="__Aliases__",
                            value=", ".join(aliases), inline=False)
            embed.add_field(name="__Cooldown__", value=cd if cd != None else 0, inline=False)
            embed.add_field(name=f"__Can {ctx.author} run it?__",
                            value="✅" if canrun == True else "❎", inline=False)
            msg = await ctx.send(embed=embed)

        elif page.lower() in cogmojis:
            thecog = self.client.get_cog(f"{cogmojis[page.lower()]} {page.lower().capitalize()}")
            commands = thecog.get_commands()
            checkedcommands = commands[:]
            for i in commands:
                try:
                    passchecks = await i.can_run(ctx)
                except Exception as e:
                    checkedcommands.remove(i)
                else:
                    if not passchecks or i.name in REMOVED:
                        checkedcommands.remove(i)

            if checkedcommands == []:
                checkedcommands.append("This cog does not have any commands you can run!")
            checkedcommands = [f"`{i.name}`" for i in checkedcommands]
            embed.description = f"**{thecog.qualified_name}**{thecog.description}"
            embed.add_field(name=f"__Commands__ ({len(checkedcommands)})",
                            value=", ".join(sorted(checkedcommands)),
                            inline=False)
            msg = await ctx.send(embed=embed)

        else:
            freezepage = page
            pages = {}
            page = "1"
            yeesnek = random.choices(self.icons, weights=[128, 16, 8, 4, 2, 1, 0.5])[0]

            for i in range(2):
                embed = discord.Embed(color=random.randint(0, 16777215))
                embed.set_author(name="COMMANDS", icon_url=yeesnek)
                embed.set_footer(text=f"{ctx.message.author}")
                embed.description = """**First time using Serpynth? See `syabout` for an introduction!**"""
                if page == "1":
                    listcogs = ["ℹ Help", "🎢 Fun", "⚙ Utility", "🖼 Images"]
                elif page == "2":
                    listcogs = ["🌲 Chill", "🎶 Music", "⚔ Arena", "💬 Other", "🔧 Debug", "👾 Jishaku"]
                cogs = listcogs[:]
                for i in listcogs:
                    if i not in self.client.cogs.keys():
                        cogs.remove(i)

                for cog in cogs:
                    commands = self.client.cogs[cog].get_commands()
                    checkedcommands = commands[:]
                    for i in commands:
                        try:
                            passchecks = await i.can_run(ctx)
                        except Exception as e:
                            checkedcommands.remove(i)
                        else:
                            if not passchecks or i.name in REMOVED:
                                checkedcommands.remove(i)
                    if checkedcommands == []:
                        continue
                    checkedcommands = [f"`{i.name}`" for i in checkedcommands]
                    embed.add_field(name=cog,
                                    value=", ".join(sorted(checkedcommands)),
                                    inline=False)

                embed.set_footer(text=f"Page {page}/2")
                embed.set_thumbnail(url=yeesnek)
                pages[page] = embed
                page = "2"

            page = freezepage
            if page == "":
                page = "1"
            if page in ("1", "2"):
                msg = await ctx.send(embed=pages[page])
            else:
                msg = await ctx.send(content=f"`{page}` is neither a page, command nor a category.", embed=pages["1"])

            await msg.add_reaction("1️⃣")
            await msg.add_reaction("2️⃣")
            await msg.add_reaction("⏹")
            while True:
                def check(reaction, user):
                    return reaction.emoji in (["1️⃣", "2️⃣", "⏹"]) and reaction.message == msg and user == ctx.author

                try:
                    reaction, user = await self.client.wait_for("reaction_add", check=check, timeout=60.0)
                except asyncio.TimeoutError:
                    try:
                        await msg.clear_reactions()
                    except:
                        pass
                    break
                else:
                    if reaction.emoji == "1️⃣":
                        pages["1"].color = random.randint(0, 16777215)
                        await msg.edit(embed=pages["1"])
                        await reaction.remove(user)
                    if reaction.emoji == "2️⃣":
                        pages["2"].color = random.randint(0, 16777215)
                        await msg.edit(embed=pages["2"])
                        await reaction.remove(user)
                    if reaction.emoji == "⏹":
                        await msg.clear_reactions()
                        break


    @commands.command(aliases=["Serpynth", "info", "serpynth", "sy", "?"])
    async def about(self, ctx):
        """ Introduces myself- Serpynth. """

        yee = self.client.get_user(597852310764519434)
        embed = discord.Embed(colour=random.randint(0, 16777215))
        embed.set_author(name="HELLO!", url="https://youtu.be/Yw6u6YkTgQ4")
        embed.set_thumbnail(url=random.choices(self.icons, weights=[256, 32, 16, 8, 4, 2, 1])[0])
        embed.set_footer(text=f"Created and developed by {yee}")
        embed.description = """Hello there! <:snek:1028410079898259586>
My name is Serpynth™, and I'm a small snake bot
in the big world of Discord.

I've got tools for almost anything you'll need here, ~~but~~
~~honestly, you've got better options for most of them~~.

I'm much better for having fun! I have a few minigames, a few
random generation commands, a few image commands, a
currency/battle system in development, and more!

Personally, I'd say my best commands are `syapplestoapples`,
`syreddit`, `sylife` and `sylifeguide`, `sysnake`, and `sysoccer`/`syfootball`.
... You should go check them out.

_ _
"""
        embed.add_field(name="Server Count", value=f"`{'{:,}'.format(len(self.client.guilds))}`")
        embed.add_field(name="User Count", value=f"`{'{:,}'.format(len(self.client.users))}`")
        embed.add_field(name="Command Count", value=f"`{'{:,}'.format(len(self.client.commands))}`")
        embed.add_field(name="More Help",
                        value="Visit `syhelp` for more commands!\nUse `syhelp <command>` for help on a specific command.\n\n_ _")
        await ctx.send(embed=embed)


    @commands.command(aliases=["friend", "otherbots"])
    async def friends(self, ctx):
        """ Enumerates a few of Serpynth's closest bots, who I grew up with. """

        async def getuser(id):
            out = await self.client.fetch_user(id)
            return out
        embed = discord.Embed(colour=random.randint(0, 16777215))
        embed.set_author(name="FRIENDS")
        embed.description = f"""Friends of Serpynth:

`CringeBot#4381`, developed by `cringemoment#4599` 🪦
`{await getuser(845942001848680448)}`, developed by `{await getuser(556761028214390807)}` 😴
`{await getuser(760919556809293884)}`, developed by `{await getuser(529011890039422976)}` 😴
`{await getuser(895623327882825728)}`, developed by `{await getuser(892883621076156416)}` 😴
"""
        await ctx.send(embed=embed)


async def setup(client):
    await client.add_cog(Help(client))
