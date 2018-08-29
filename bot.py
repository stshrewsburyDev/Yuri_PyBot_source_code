"""
Yuri PyBot Source Code
Made By Steven Shrewsbury (AKA: stshrewsburyDev)
"""

from libs.debug_logs import *

INFO("setting things up, please wait...")

DEBUG("importing needed libraries...")
from discord.ext import commands
from discord.ext.commands import Bot
import discord, asyncio, os, time, random, platform, requests
INFO("task complete")

DEBUG("setting up custom libraries...")
import libs.help_lists as h_lists
import libs.vars_lists as var_list
import libs.utils as utils
INFO("task complete")

DEBUG("setting up client...")
BOT_TOKEN = str(os.environ.get("BOT_TOKEN"))
BOT_LOG_WEBHOOK_URL = str(os.environ.get("BOT_LOG_WEBHOOK_URL"))
Client = discord.Client()
client = commands.Bot(command_prefix="y!")
client.remove_command("help")
bot_embed_colour = discord.colour.Colour.dark_purple()
bot_error_embed_colour = discord.colour.Colour.dark_red()

bot_launch_time = time.time()
bot_launch_time_string = str(time.strftime("%H")) + ":" + str(time.strftime("%M")) + ":" + str(time.strftime("%S"))
bot_launch_date_string = str(time.strftime("%d")) + "/" + str(time.strftime("%m")) + "/" + str(time.strftime("%y"))
INFO("task complete")

@client.event
async def on_ready():
    LOG("logged in as:")
    next_log = "\t~ bot user name:" + str(client.user.name)
    LOG(next_log)
    next_log = "\t~ bot user ID:" + str(client.user.id)
    LOG(next_log)
    LOG("bot is now active")
    LOG("\t bot launched at:")
    next_log = "\t\t" + bot_launch_time_string
    LOG(next_log)
    next_log = "\t\t" + bot_launch_date_string
    LOG(next_log)
    client.loop.create_task(playing_msg_loop())

def send_webhook_log(description, thumbnail, extra_fields):
    embed_log = {}

    embed_log["title"] = "Yuri PyBot Log:"
    embed_log["description"] = description
    embed_log["thumbnail"] = {"url": thumbnail}
    embed_log["color"] = int("6d00b3", 16)

    if len(extra_fields) != 0:
        embed_log["feilds"] = []
        for feild in extra_fields:
            embed_log['fields'].append({"name":feild[0],"value":feild[1]})

    data = {"embeds": [embed_log]}
    requests.post(BOT_LOG_WEBHOOK_URL, json=data)

@client.event
async def on_server_join(server):
    webhook_desc = "Joined New Server: **" + str(server) + "**"
    send_webhook_log(description=webhook_desc,
                     thumbnail=server.icon_url,
                     extra_fields=[])

    thanks_for_adding_msg = discord.Embed(title="",
                                          description=("**Thanks For Adding Me To " + str(server.name) + "**\n" + var_list.thanks_for_adding_msg_contents),
                                          colour=bot_embed_colour)
    thanks_for_adding_msg.set_author(name="Hello!",
                                     icon_url=client.user.avatar_url)
    await client.send_message(server.owner,
                              embed=thanks_for_adding_msg)

@client.event
async def on_server_remove(server):
    webhook_desc = "Left Server: **" + str(server) + "**"
    send_webhook_log(description=webhook_desc,
                     thumbnail=server.icon_url,
                     extra_fields=[])

@client.event
async def playing_msg_loop():
    while True:
        await client.change_presence(game=discord.Game(name="Say y!help", type=1, url='https://twitch.tv/stshrewsburyDev'))
        await asyncio.sleep(8)
        await client.change_presence(game=discord.Game(name="Made With discord.py", type=1, url='https://twitch.tv/stshrewsburyDev'))
        await asyncio.sleep(8)
        await client.change_presence(game=discord.Game(name="Made By stshrewsburyDev", type=1, url='https://twitch.tv/stshrewsburyDev'))
        await asyncio.sleep(8)
        await client.change_presence(game=discord.Game(name=("In " + str(len(list(client.servers))) + " Server(s)"), type=1, url='https://twitch.tv/stshrewsburyDev'))
        await asyncio.sleep(8)
        await client.change_presence(game=discord.Game(name=("With Pens (And Knives)"), type=1, url='https://twitch.tv/stshrewsburyDev'))
        await asyncio.sleep(8)

@client.event
async def on_command_error(error,
                           ctx
                           ):
    if isinstance(error, commands.CommandOnCooldown):
        cooldown = discord.Embed(title="",
                                 description="You Are On Cooldown To Use This Command",
                                 colour=bot_error_embed_colour)
        cooldown.set_author(name="COOLDOWN ERROR:",
                            icon_url=client.user.avatar_url)
        await client.send_message(ctx.message.channel,
                                  embed=cooldown)
        return

    elif isinstance(error, commands.CommandNotFound):
        no_command = discord.Embed(title="",
                                   description="Unkown Command. Use **y!help** To See All Commands",
                                   colour=bot_error_embed_colour)
        no_command.set_author(name="UNKNOWN COMMAND ERROR:",
                              icon_url=client.user.avatar_url)
        await client.send_message(ctx.message.channel,
                                  embed=no_command)
        return

    else:
        ERROR(error)

class help_commands:
    @commands.cooldown(1, 10, commands.BucketType.user)
    @client.command(pass_context = True)
    async def help():
        help_msg = discord.Embed(title=h_lists.notice,
                                 description=h_lists.main_help,
                                 colour=bot_embed_colour)
        help_msg.set_author(name="Main Help:",
                            icon_url=client.user.avatar_url)
        await client.say(embed=help_msg)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @client.command(pass_context = True)
    async def help_general():
        g_help_msg = discord.Embed(title=h_lists.notice,
                                   description=h_lists.general_help,
                                   colour=bot_embed_colour)
        g_help_msg.set_author(name="General Help:",
                              icon_url=client.user.avatar_url)
        await client.say(embed=g_help_msg)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @client.command(pass_context = True)
    async def help_bot():
        b_help_msg = discord.Embed(title=h_lists.notice,
                                   description=h_lists.bot_help,
                                   colour=bot_embed_colour)
        b_help_msg.set_author(name="Bot Help:",
                              icon_url=client.user.avatar_url)
        await client.say(embed=b_help_msg)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @client.command(pass_context = True)
    async def help_server():
        s_help_msg = discord.Embed(title=h_lists.notice,
                                   description=h_lists.server_help,
                                   colour=bot_embed_colour)
        s_help_msg.set_author(name="Server Help:",
                              icon_url=client.user.avatar_url)
        await client.say(embed=s_help_msg)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @client.command(pass_context = True)
    async def help_admin():
        a_help_msg = discord.Embed(title=h_lists.notice,
                                   description=h_lists.admin_help,
                                   colour=bot_embed_colour)
        a_help_msg.set_author(name="Admin Help:",
                              icon_url=client.user.avatar_url)
        await client.say(embed=a_help_msg)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @client.command(pass_context = True)
    async def help_fun():
        f_help_msg = discord.Embed(title=h_lists.notice,
                                   description=h_lists.fun_help,
                                   colour=bot_embed_colour)
        f_help_msg.set_author(name="Fun Help:",
                              icon_url=client.user.avatar_url)
        await client.say(embed=f_help_msg)

class general_commands:
    @client.command(pass_context = True)
    async def joke():
        joke_msg = discord.Embed(title="",
                                 description=random.choice(var_list.jokes_list),
                                 colour=bot_embed_colour)
        joke_msg.set_author(name="Joke:",
                            icon_url=client.user.avatar_url)
        await client.say(embed=joke_msg)

    @client.command(pass_context = True)
    async def rip(ctx, name: str=None, *, text: str=None):
        rip_msg = discord.Embed(title="",
                                description="",
                                colour=bot_embed_colour)
        if name is None:
            name = ctx.message.author.name
        if len(ctx.message.mentions) >= 1:
            name = str(ctx.message.mentions[0].name)
        if text is None:
            text = "No Message..."
        if len(text) >= 22:
            one = text[:22]
            two = text[22:]
            rip_msg.set_image(url=("http://www.tombstonebuilder.com/generate.php?top1=R.I.P&top2={0}&top3={1}&top4={2}".format(name, one, two).replace(" ", "%20")))
        else:
            rip_msg.set_image(url=("http://www.tombstonebuilder.com/generate.php?top1=R.I.P&top2={0}&top4={1}".format(name, text).replace(" ", "%20")))
        await client.say(embed=rip_msg)

    @client.command(pass_context = True)
    async def reverse(ctx, *, text: str=None):
        if text is None:
            reverse_msg = discord.Embed(title="",
                                        description="Please Enter Something To Be Reversed",
                                        colour=bot_embed_colour)
        else:
            reverse_msg = discord.Embed(title="",
                                        description=utils.reverse(str(text)),
                                        colour=bot_embed_colour)
        reverse_msg.set_author(name="Reversed Text:",
                               icon_url=client.user.avatar_url)
        await client.say(embed=reverse_msg)

    @client.command(pass_context = True)
    async def analyse(ctx, *, text: str=None):
        if text is None:
            analyse_msg = discord.Embed(title="",
                                        description="Please Enter Some Text To Be Analysed",
                                        colour=bot_embed_colour)
        else:
            analyse_msg = discord.Embed(title="",
                                        description="",
                                        colour=bot_embed_colour)
            analyse_results = utils.analyse(text)
            analyse_msg.add_field(name="Inputted Text:",
                                  value=text,
                                  inline=False)
            analyse_msg.add_field(name="Length:",
                                  value=analyse_results["length"],
                                  inline=False)
            analyse_msg.add_field(name="Word Count:",
                                  value=analyse_results["words"],
                                  inline=False)
            analyse_msg.add_field(name="Uppercase Letters:",
                                  value=analyse_results["uppercase"],
                                  inline=False)
            analyse_msg.add_field(name="Lowercase Letters:",
                                  value=analyse_results["lowercase"],
                                  inline=False)
            analyse_msg.add_field(name="Numbers:",
                                  value=analyse_results["numbers"],
                                  inline=False)
        analyse_msg.set_author(name="Analyse Text:",
                               icon_url=client.user.avatar_url)
        await client.say(embed=analyse_msg)

    @client.command(pass_context = True)
    async def num2binary(ctx, *, text: str=None):
        try:
            number_to_convert = int(text)
            binary_number = utils.num2binconv(number=number_to_convert)
            num2binary_msg = discord.Embed(title="",
                                           description=("Denary: " + str(number_to_convert) + "\nBinary: " + str(binary_number)),
                                           colour=bot_embed_colour)
            num2binary_msg.set_author(name="Denary To Binary Conversion:",
                                      icon_url=client.user.avatar_url)
            await client.say(embed=num2binary_msg)
        except:
            num2binary_error = discord.Embed(title="",
                                             description="Please Enter A Real Valid Number",
                                             colour=bot_error_embed_colour)
            num2binary_error.set_author(name="Number Error:",
                                        icon_url=client.user.avatar_url)
            await client.say(embed=num2binary_error)

    @client.command(pass_context = True)
    async def binary2num(ctx, *, text: str=None):
        if utils.checkbin(text) is True:
            denary_number = utils.bin2numconv(number=text)
            binary2num_msg = discord.Embed(title="",
                                           description=("Binary: " + str(text) + "\nDenary: " + str(denary_number)),
                                           colour=bot_error_embed_colour)
            binary2num_msg.set_author(name="Binary To Denary Conversion:",
                                      icon_url=client.user.avatar_url)
            await client.say(embed=binary2num_msg)
        else:
            binary2num_error = discord.Embed(title="",
                                             description="Please Enter A Real Valid Binary Number",
                                             colour=bot_error_embed_colour)
            binary2num_error.set_author(name="Binary Error:",
                                        icon_url=client.user.avatar_url)
            await client.say(embed=binary2num_error)

    @client.command(pass_context = True)
    async def urban(ctx, *, text: str=None):
        search_result = utils.search_urban(text)
        if search_result is not None:
            urban_msg = discord.Embed(title="",
                                      description="",
                                      colour=bot_embed_colour)
            urban_msg.set_author(name=("Urban Search For: " + str(text)),
                                 icon_url=client.user.avatar_url)
            urban_msg.add_field(name="Definition:",
                                value=str(search_result["definition"].replace("\n", " ")),
                                inline=False)
            urban_msg.add_field(name="Example:",
                                value=str(search_result["example"].replace("\n", " ")),
                                inline=False)
            try:
                await client.say(embed=urban_msg)
            except:
                urban_error = discord.Embed(title="",
                                            description="There Was A Error While Searching Your Request\nPlease Try A Different Search Term",
                                            colour=bot_error_embed_colour)
                urban_error.set_author(name="Urban Search Error:",
                                       icon_url=client.user.avatar_url)
                await client.say(embed=urban_error)
        else:
            urban_error = discord.Embed(title="",
                                        description="There Was A Error While Searching Your Request\nPlease Try A Different Search Term",
                                        colour=bot_error_embed_colour)
            urban_error.set_author(name="Urban Search Error:",
                                   icon_url=client.user.avatar_url)
            await client.say(embed=urban_error)

    @client.command(pass_context = True)
    async def slap(ctx, user: discord.Member = None):
        if user is None:
            slap_msg = discord.Embed(title="",
                                     description="",
                                     colour=bot_embed_colour)
            slap_msg.set_author(name=(str(ctx.message.author) + " Is Just Flailing Their Arms Around..."))
            slap_msg.set_image(url="https://stshrewsburydev.github.io/discord_bots_resources_site/yuri_pybot/images/slap_command_images/B1.gif")
            slap_msg.set_footer(text="Hint: Try And @Mentioning A User")

        elif user is ctx.message.author:
            slap_msg = discord.Embed(title="",
                                     description="",
                                     colour=bot_embed_colour)
            slap_msg.set_author(name=(str(ctx.message.author) + " Is... Slapping Themself..."))
            slap_msg.set_image(url="https://stshrewsburydev.github.io/discord_bots_resources_site/yuri_pybot/images/slap_command_images/C1.gif")
            slap_msg.set_footer(text="Why On Earth Would They Do That...")

        else:
            if str(user.id) == "431823873391198218":
                slap_msg = discord.Embed(title="",
                                         description="",
                                         colour=bot_embed_colour)
                slap_msg.set_author(name=(str(ctx.message.author) + " Is Trying To Slap Me..."))
                slap_msg.set_image(url="https://stshrewsburydev.github.io/discord_bots_resources_site/yuri_pybot/images/slap_command_images/A1.gif")
                slap_msg.set_footer(text="Please Dont Do That...")

            else:
                slap_msg = discord.Embed(title="",
                                         description="",
                                         colour=bot_embed_colour)
                slap_msg.set_author(name=(str(ctx.message.author) + " Just Slapped " + str(user) + " Right In The Face..."))
                slap_msg.set_image(url=random.choice(var_list.slap_command_normal_images))
                slap_msg.set_footer(text=("I Wonder What " + str(user) + " Did To Deserve This..."))

        await client.say(embed=slap_msg)

    @client.command(pass_context = True)
    async def avatar(ctx, user: discord.Member = None):
        if user is None:
            user = ctx.message.author
        avatar = user.avatar_url
        if avatar == "":
            avatar = random.choice(var_list.default_discord_logos)
        avatar_msg = discord.Embed(title="",
                                   description=("Here Is The Avatar Of **" + str(user.name) + "**:"),
                                   colour=bot_embed_colour)
        avatar_msg.set_image(url=avatar)
        await client.say(embed=avatar_msg)

class bot_commands:
    @commands.cooldown(1, 10, commands.BucketType.user)
    @client.command(pass_context = True)
    async def ping():
        time1 = time.perf_counter()
        ping_msg = await client.say(embed=discord.Embed(title="Ping!",
                                                        description="Waiting For A Responce From The Server...",
                                                        colour=bot_embed_colour))
        time2 = time.perf_counter()
        latency = time2 - time1

        latency_msg = discord.Embed(title="",
                                    description=("Pong! Latency Is " + str(round(latency * 1000)) + "ms"),
                                    colour=bot_embed_colour)
        latency_msg.set_author(name="Ping?!",
                               icon_url=client.user.avatar_url)
        await client.delete_message(ping_msg)
        await client.say(embed=latency_msg)

    @client.command(pass_context = True)
    async def invite():
        invite_msg = discord.Embed(title="",
                                   description="",
                                   colour=bot_embed_colour)
        invite_msg.set_author(name="Invite Links:",
                              icon_url=client.user.avatar_url)
        invite_msg.add_field(name="My Developers Server:",
                             value="https://discord.io/stshrewsburyDev\n\n**Use If Above Doesnt Work:**\nhttps://discord.gg/QGMaFMf",
                             inline=False)
        invite_msg.add_field(name="Add Me To Your Server:",
                             value="https://discordapp.com/oauth2/authorize?client_id=431823873391198218&permissions=8&scope=bot",
                             inline=False)
        await client.say(embed=invite_msg)

    @client.command(pass_context = True)
    async def bot_info():
        bot_current_time = time.time()
        bot_up_time = int(bot_current_time - bot_launch_time)
        bot_up_time_hours = bot_up_time // 3600
        bot_up_time -= (bot_up_time_hours * 3600)
        bot_up_time_mins = bot_up_time // 60
        bot_up_time -= (bot_up_time_mins * 60)
        bot_up_time_secs = bot_up_time

        bot_info_m = discord.Embed(title="",
                                   description="",
                                   colour=discord.colour.Colour.dark_purple())

        bot_info_m.set_author(name="BOT INFORMATION:",
                              icon_url=client.user.avatar_url)

        bot_info_m.add_field(name="Name:",
                             value=str(client.user.name),
                             inline=False)

        bot_info_m.add_field(name="Bot Version:",
                             value=var_list.bot_version,
                             inline=False)

        bot_info_m.add_field(name="Bot Creator",
                             value="Steven Shrewsbury AKA:**stshrewsburyDev#4846**",
                             inline=False)

        bot_info_m.add_field(name="Uptime:",
                             value=(str(bot_up_time_hours) + " Hour(s), " + str(bot_up_time_mins) + " Minute(s) And " + str(bot_up_time_secs) + " Second(s)"),
                             inline=False)

        bot_info_m.add_field(name="Total Servers:",
                             value=str(len(list(client.servers))),
                             inline=True)

        bot_info_m.add_field(name="Total Channels:",
                             value=str(len(list(client.get_all_channels()))),
                             inline=True)

        bot_info_m.add_field(name="Total Users:",
                             value=str(len(list(client.get_all_members()))),
                             inline=False)

        bot_info_m.add_field(name="Python Version:",
                             value=platform.python_version(),
                             inline=True)

        bot_info_m.add_field(name="discord.py Version:",
                             value=str(discord.__version__),
                             inline=True)

        bot_info_m.add_field(name="Host Operating System:",
                             value='{} {} | {}'.format(platform.system(), platform.release(), platform.version()),
                             inline=False)

        await client.say(embed=bot_info_m)

    @client.command(pass_context = True)
    async def about():
        about_msg = discord.Embed(title="",
                                  description=var_list.about_info,
                                  colour=discord.colour.Colour.dark_purple())

        about_msg.set_author(name="About:",
                             icon_url=client.user.avatar_url)

        await client.say(embed=about_msg)

class server_commands:
    @client.command(pass_context = True)
    async def server_info(ctx):
        server_custom_emojis = ""
        for custom_emoji in ctx.message.server.emojis:
            server_custom_emojis += str(custom_emoji) + " "
        if server_custom_emojis == "":
            server_custom_emojis = "Server Has No Custom Emojis"

        server_info_msg = discord.Embed(title="",
                                        description=("Server Info On " + str(ctx.message.server)),
                                        colour=bot_embed_colour)

        server_info_msg.set_author(name="SERVER INFORMATION:",
                                   icon_url=client.user.avatar_url)

        server_info_msg.set_thumbnail(url=ctx.message.server.icon_url)

        server_info_msg.add_field(name="Sever Name:",
                                  value=str(ctx.message.server),
                                  inline=False)

        server_info_msg.add_field(name="Member Count:",
                                  value=str(ctx.message.server.member_count),
                                  inline=False)

        server_info_msg.add_field(name="Server Region:",
                                  value=str(ctx.message.server.region),
                                  inline=False)

        server_info_msg.add_field(name="Server ID:",
                                  value=str(ctx.message.server.id),
                                  inline=False)

        server_info_msg.add_field(name="Server Owner:",
                                  value=str(ctx.message.server.owner),
                                  inline=False)

        server_info_msg.add_field(name="Server Verification Level:",
                                  value=str(ctx.message.server.verification_level),
                                  inline=False)

        server_info_msg.add_field(name="Server Custom Emojis:",
                                  value=server_custom_emojis,
                                  inline=False)

        server_info_msg.add_field(name="Server Splash:",
                                  value=str(ctx.message.server.splash),
                                  inline=False)

        server_info_msg.add_field(name="Icon URL:",
                                  value=str(ctx.message.server.icon_url),
                                  inline=False)


        await client.say(embed=server_info_msg)

    @client.command(pass_context = True)
    async def list_members(ctx):
        if len(ctx.message.server.members) <= 200:
            members_formatted = ""
            for _member_ in ctx.message.server.members:
                members_formatted += str(_member_) + "\n"

            list_members_msg = discord.Embed(name="",
                                             description=members_formatted,
                                             colour=bot_embed_colour)

            list_members_msg.set_author(name=("Members In Server: " + str(ctx.message.server)),
                                        icon_url=client.user.avatar_url)

            list_members_msg.set_thumbnail(url=ctx.message.server.icon_url)

            await client.send_message(ctx.message.author,
                                      embed=list_members_msg)

            list_members_success_msg = discord.Embed(name="",
                                                     description=("**" + ctx.message.author.name + "**, The Info Has Been DM'd To You."),
                                                     colour=discord.colour.Colour.dark_purple())

            list_members_success_msg.set_author(name="SUCCESS:",
                                                icon_url=client.user.avatar_url)

            await client.say(embed=list_members_success_msg)

        else:
            list_members_msg = discord.Embed(name="Oops...",
                                             description="Sorry But Due To Lag In The Bots Server Client This Command Only Works For Servers With 500 Or Less Members In It.",
                                             colour=bot_embed_colour)

            list_members_msg.set_author(name="LIST MEMBERS LIMITATIONS:",
                                        icon_url=client.user.avatar_url)

            await client.say(embed=list_members_msg)

    @client.command(pass_context = True)
    async def member_count(ctx):
        online_member_count = 0
        IDLE_member_count = 0
        DND_member_count = 0
        offline_member_count = 0
        bot_member_count = 0

        for _member_ in ctx.message.server.members:
            if str(_member_.status).lower() == "online":
                online_member_count += 1
            if str(_member_.status).lower() == "idle":
                IDLE_member_count += 1
            if str(_member_.status).lower() == "dnd":
                DND_member_count += 1
            if str(_member_.status).lower() == "offline":
                offline_member_count += 1
            if str(_member_.bot).lower() == "true":
                bot_member_count += 1

        member_count_msg = discord.Embed(title="",
                                         description=("Member Count For " + str(ctx.message.server) + ":"),
                                         colour=bot_embed_colour)

        member_count_msg.set_author(name="Member Count:",
                                    icon_url=client.user.avatar_url)

        member_count_msg.set_thumbnail(url=ctx.message.server.icon_url)

        member_count_msg.add_field(name="Total Members",
                                   value=(str(ctx.message.server.member_count) + " Members."),
                                   inline=False)

        member_count_msg.add_field(name="Details:",
                                   value=("ONLINE: " + str(online_member_count) + "\nIDLE: " + str(IDLE_member_count) + "\nDO NOT DISTURB: " + str(DND_member_count) + "\nOFFLINE: " + str(offline_member_count) + "\nBOTS: " + str(bot_member_count)),
                                   inline=False)

        await client.say(embed=member_count_msg)

    @client.command(pass_context = True)
    async def stats(ctx, user: discord.Member = None):
        if user is None:
            stats_msg = discord.Embed(title="Hmph!",
                                      description="Please State A User.\n\nEg: >>stats @Yuri PyBot#8191",
                                      colour=bot_embed_colour)

            stats_msg.set_author(name="STATS ERROR:",
                                 icon_url=client.user.avatar_url)

        else:
            user_avatar_URL = user.avatar_url
            if user_avatar_URL == "":
                user_avatar_URL = random.choice(var_list.default_discord_logos)

            formatted_roles = ""
            first_one = True
            for _role_ in user.roles:
                if _role_.name != "@everyone":
                    if first_one == True:
                        formatted_roles += str(_role_.mention)
                        first_one = False
                    else:
                        formatted_roles += ", " + str(_role_.mention)

            stats_msg = discord.Embed(title="",
                                      description="",
                                      colour=bot_embed_colour)

            stats_msg.set_author(name=("Stats On User **" + str(user) + "**:"),
                                 icon_url=client.user.avatar_url)

            stats_msg.set_thumbnail(url=user_avatar_URL)

            stats_msg.add_field(name="Name:",
                                value=str(user.name),
                                inline=False)

            stats_msg.add_field(name="Display Name:",
                                value=str(user.display_name),
                                inline=False)

            stats_msg.add_field(name="User ID:",
                                value=str(user.id),
                                inline=False)

            stats_msg.add_field(name="# Number:",
                                value=str(user.discriminator),
                                inline=False)

            stats_msg.add_field(name="Full Name:",
                                value=str(user),
                                inline=False)

            stats_msg.add_field(name="Nickname:",
                                value=str(user.nick),
                                inline=False)

            stats_msg.add_field(name="Status:",
                                value=str(user.status).upper(),
                                inline=False)

            stats_msg.add_field(name="Highest Role:",
                                value=str(user.top_role),
                                inline=False)

            stats_msg.add_field(name="Current Game:",
                                value=str(user.game),
                                inline=False)

            stats_msg.add_field(name="Colour:",
                                value=str(user.colour),
                                inline=False)

            stats_msg.add_field(name="Bot?:",
                                value=str(user.bot),
                                inline=False)

            stats_msg.add_field(name="Date Joined Server:",
                                value=str(user.joined_at),
                                inline=False)

            stats_msg.add_field(name="User Avatar URL:",
                                value=user_avatar_URL,
                                inline=False)

            stats_msg.add_field(name="Roles:",
                                value=formatted_roles,
                                inline=False)

        await client.say(embed=stats_msg)

class admin_commands:
    @client.command(pass_context = True)
    async def kick(ctx, user: discord.Member = None, *, text: str=None):
        if ctx.message.author.server_permissions.kick_members:
            if user is None:
                no_user_mentioned_msg = discord.Embed(title="",
                                                      description="Sorry You Havent Specified A User To Kick.",
                                                      colour=bot_embed_colour)
                no_user_mentioned_msg.set_author(name="No User Mentioned:",
                                                 icon_url=client.user.avatar_url)
                await client.say(embed=no_user_mentioned_msg)
                return

            else:
                if text is None:
                    no_reason_msg = discord.Embed(title="",
                                                  description="Sorry You Havent Entered A Reason To Kick The Specified User.",
                                                  colour=bot_embed_colour)
                    no_reason_msg.set_author(name="No Reason:",
                                             icon_url=client.user.avatar_url)
                    await client.say(embed=no_reason_msg)
                    return

                else:
                    if str(user.id) == "312984580745330688":
                        cannot_kick_creator_msg = discord.Embed(title="",
                                                                description="Sorry I Cannot Kick My Creator.",
                                                                colour=bot_embed_colour)
                        cannot_kick_creator_msg.set_author(name="I Cant Do That!",
                                                           icon_url=client.user.avatar_url)
                        await client.say(embed=cannot_kick_creator_msg)
                        return
                    try:
                        await client.kick(user)

                        kick_successfull_msg_contents = "Kicked: " + str(user.name) + "\nReason: " + str(text)
                        kick_successfull_msg = discord.Embed(title="",
                                                             description=kick_successfull_msg_contents,
                                                             colour=bot_embed_colour)
                        kick_successfull_msg.set_author(name="Kicked User:",
                                                        icon_url=client.user.avatar_url)
                        await client.say(embed=kick_successfull_msg)

                        youve_been_kicked_msg_contents = "Server: " + str(ctx.message.server.name) + "\nReason: " + str(text)
                        youve_been_kicked_msg = discord.Embed(title="",
                                                              description=youve_been_kicked_msg_contents,
                                                              colour=bot_embed_colour)
                        youve_been_kicked_msg.set_author(name="You Have Been Kicked From A Server:",
                                                         icon_url=client.user.avatar_url)
                        await client.send_message(user,
                                                  embed=youve_been_kicked_msg)

                    except discord.errors.Forbidden:
                        kick_failed_msg = discord.Embed(title="",
                                                        description="Sorry Either I Am In A Role Below The Specified User Or I Do Not Have The Correct Perms To Perform This Command",
                                                        colour=bot_embed_colour)
                        kick_failed_msg.set_author(name="Could Not Kick User:",
                                                   icon_url=client.user.avatar_url)
                        await client.say(embed=kick_failed_msg)
                        return
        else:
            no_perms_msg = discord.Embed(title="",
                                         description="Sorry You Dont Have The Right Perms To Perform this Action.\n\nYou Need Permission: Kick Members/Administrator",
                                         colour=bot_embed_colour)
            no_perms_msg.set_author(name="No Correct Perms:",
                                    icon_url=client.user.avatar_url)
            await client.say(embed=no_perms_msg)

    @client.command(pass_context = True)
    async def ban(ctx, user: discord.Member = None, *, text: str=None):
        if ctx.message.author.server_permissions.ban_members:
            if user is None:
                no_user_mentioned_msg = discord.Embed(title="",
                                                      description="Sorry You Havent Specified A User To Ban.",
                                                      colour=bot_embed_colour)
                no_user_mentioned_msg.set_author(name="No User Mentioned:",
                                                 icon_url=client.user.avatar_url)
                await client.say(embed=no_user_mentioned_msg)
                return

            else:
                if text is None:
                    no_reason_msg = discord.Embed(title="",
                                                  description="Sorry You Havent Entered A Reason To Ban The Specified User.",
                                                  colour=bot_embed_colour)
                    no_reason_msg.set_author(name="No Reason:",
                                             icon_url=client.user.avatar_url)
                    await client.say(embed=no_reason_msg)
                    return

                else:
                    if str(user.id) == "312984580745330688":
                        cannot_ban_creator_msg = discord.Embed(title="",
                                                               description="Sorry I Cannot Ban My Creator.",
                                                               colour=bot_embed_colour)
                        cannot_ban_creator_msg.set_author(name="I Cant Do That!",
                                                          icon_url=client.user.avatar_url)
                        await client.say(embed=cannot_ban_creator_msg)
                        return
                    try:
                        await client.ban(user, delete_message_days=0)

                        ban_successfull_msg_contents = "Banned: " + str(user.name) + "\nReason: " + str(text)
                        ban_successfull_msg = discord.Embed(title="",
                                                            description=ban_successfull_msg_contents,
                                                            colour=bot_embed_colour)
                        ban_successfull_msg.set_author(name="Banned User:",
                                                       icon_url=client.user.avatar_url)
                        await client.say(embed=ban_successfull_msg)

                        youve_been_banned_msg_contents = "Server: " + str(ctx.message.server.name) + "\nReason: " + str(text)
                        youve_been_banned_msg = discord.Embed(title="",
                                                              description=youve_been_banned_msg_contents,
                                                              colour=bot_embed_colour)
                        youve_been_banned_msg.set_author(name="You Have Been Banned From A Server:",
                                                         icon_url=client.user.avatar_url)
                        await client.send_message(user,
                                                  embed=youve_been_banned_msg)

                    except discord.errors.Forbidden:
                        ban_failed_msg = discord.Embed(title="",
                                                        description="Sorry Either I Am In A Role Below The Specified User Or I Do Not Have The Correct Perms To Perform This Command",
                                                        colour=bot_embed_colour)
                        ban_failed_msg.set_author(name="Could Not Ban User:",
                                                   icon_url=client.user.avatar_url)
                        await client.say(embed=ban_failed_msg)
                        return
        else:
            no_perms_msg = discord.Embed(title="",
                                         description="Sorry You Dont Have The Right Perms To Perform this Action.\n\nYou Need Permission: Ban Members/Administrator",
                                         colour=bot_embed_colour)
            no_perms_msg.set_author(name="No Correct Perms:",
                                    icon_url=client.user.avatar_url)
            await client.say(embed=no_perms_msg)

    @client.command(pass_context = True)
    async def warn(ctx, user: discord.Member = None, *, text: str=None):
        if ctx.message.author.server_permissions.manage_server:
            if user is None:
                no_user_mentioned_msg = discord.Embed(title="",
                                                      description="Sorry You Havent Specified A User To Warn.",
                                                      colour=bot_embed_colour)
                no_user_mentioned_msg.set_author(name="No User Mentioned:",
                                                 icon_url=client.user.avatar_url)
                await client.say(embed=no_user_mentioned_msg)
                return

            else:
                if text is None:
                    no_reason_msg = discord.Embed(title="",
                                                  description="Sorry You Havent Entered A Reason To Warn The Specified User.",
                                                  colour=bot_embed_colour)
                    no_reason_msg.set_author(name="No Reason:",
                                             icon_url=client.user.avatar_url)
                    await client.say(embed=no_reason_msg)
                    return

                else:
                    if str(user.id) == "312984580745330688":
                        cannot_warn_creator_msg = discord.Embed(title="",
                                                                description="Sorry I Cannot Warn My Creator.",
                                                                colour=bot_embed_colour)
                        cannot_warn_creator_msg.set_author(name="I Cant Do That!",
                                                           icon_url=client.user.avatar_url)
                        await client.say(embed=cannot_warn_creator_msg)
                        return


                    warn_successfull_msg_contents = "Warned: " + str(user.name) + "\nReason: " + str(text)
                    warn_successfull_msg = discord.Embed(title="",
                                                         description=warn_successfull_msg_contents,
                                                         colour=bot_embed_colour)
                    warn_successfull_msg.set_author(name="Warned User:",
                                                    icon_url=client.user.avatar_url)
                    await client.say(embed=warn_successfull_msg)

                    youve_been_warned_msg_contents = "Server: " + str(ctx.message.server.name) + "\nReason: " + str(text)
                    youve_been_warned_msg = discord.Embed(title="",
                                                          description=youve_been_warned_msg_contents,
                                                          colour=bot_embed_colour)
                    youve_been_warned_msg.set_author(name="You Have Been Warned From A Server:",
                                                     icon_url=client.user.avatar_url)
                    await client.send_message(user,
                                              embed=youve_been_warned_msg)

        else:
            no_perms_msg = discord.Embed(title="",
                                         description="Sorry You Dont Have The Right Perms To Perform this Action.\n\nYou Need Permission: Manage Server/Administrator",
                                         colour=bot_embed_colour)
            no_perms_msg.set_author(name="No Correct Perms:",
                                    icon_url=client.user.avatar_url)
            await client.say(embed=no_perms_msg)

class fun_commands:
    @client.command(pass_context = True)
    async def dance(ctx):
        dance_msg = discord.Embed(title="",
                                  description="",
                                  colour=bot_embed_colour)
        dance_msg.set_author(name="O-Ok...")
        dance_msg.set_image(url=random.choice(var_list.dance_command_images))
        await client.say(embed=dance_msg)

    @client.command(pass_context = True)
    async def middle_finger(ctx):
        middle_finger_msg = discord.Embed(title="",
                                          description="",
                                          colour=bot_embed_colour)
        middle_finger_msg.set_author(name="O-Ok...")
        middle_finger_msg.set_image(url=random.choice(var_list.middle_finger_command_images))
        await client.say(embed=middle_finger_msg)

    @client.command(pass_context = True)
    async def dice_roll(ctx):
        dice_roll_msg = discord.Embed(title="",
                                      description=("You Rolled A: " + str(random.randint(1, 6))),
                                      colour=bot_embed_colour)
        dice_roll_msg.set_author(name="Dice Roll:",
                                 icon_url=client.user.avatar_url)
        await client.say(embed=dice_roll_msg)

    @client.command(pass_context = True)
    async def fruit_machine(ctx):
        outcome = utils.fruit_machine_results_maker(possible_outcomes=var_list.fruit_machiene_outcones)

        if outcome["middle_line"][0] == outcome["middle_line"][1] == outcome["middle_line"][2]:
            fruit_machine_msg = discord.Embed(title="",
                                              description=(str(outcome["text"]) + "\n\nYou Win. GG " + str(ctx.message.author.name)),
                                              colour=bot_embed_colour)
            fruit_machine_msg.set_author(name="Fruit Machiene:",
                                         icon_url=client.user.avatar_url)
            await client.say (embed=fruit_machine_msg)
            return

        else:
            fruit_machine_msg = discord.Embed(title="",
                                              description=(str(outcome["text"]) + "\n\nYou Didnt Win This Time. GG " + str(ctx.message.author.name)),
                                              colour=bot_embed_colour)
            fruit_machine_msg.set_author(name="Fruit Machiene:",
                                         icon_url=client.user.avatar_url)
            await client.say (embed=fruit_machine_msg)
            return

    @commands.cooldown(1, 10, commands.BucketType.user)
    @client.command(pass_context = True, aliases=["day_at_the_races"])
    async def horse_race(ctx, *, text: str=None):
        if text is None:
            invalid_entry_msg = discord.Embed(title="",
                                              description="Please Input a Valid Arguement.\n\nExample: **y!horse_race 1**",
                                              colour=bot_embed_colour)
            invalid_entry_msg.set_author(name="Invalid Arguement:",
                                         icon_url=client.user.avatar_url)
            await client.say(embed=invalid_entry_msg)

        elif text != "1" and text != "2" and text != "3" and text != "4":
            invalid_entry_msg = discord.Embed(title="",
                                              description="Please Input a Valid Arguement.\n\nExample: **y!horse_race 1**",
                                              colour=bot_embed_colour)
            invalid_entry_msg.set_author(name="Invalid Arguement:",
                                         icon_url=client.user.avatar_url)
            await client.say(embed=invalid_entry_msg)

        else:
            player_no = int(text)

            horse_1_pos = 0
            horse_2_pos = 0
            horse_3_pos = 0
            horse_4_pos = 0

            game_not_finished = True

            horse_racing_msg = discord.Embed(title="",
                                             description=(str(utils.re_draw_horse_race(horse_1_pos, horse_2_pos, horse_3_pos, horse_4_pos))),
                                             colour=bot_embed_colour)
            horse_racing_msg.set_author(name="Horse Racing:",
                                        icon_url=client.user.avatar_url)
            horse_racing_msg_msg = await client.say(embed=horse_racing_msg)

            while game_not_finished:
                choices_horse_race = [0, 1]

                horse_1_pos += random.choice(choices_horse_race)
                horse_2_pos += random.choice(choices_horse_race)
                horse_3_pos += random.choice(choices_horse_race)
                horse_4_pos += random.choice(choices_horse_race)

                horse_racing_msg = discord.Embed(title="",
                                                 description=(str(utils.re_draw_horse_race(horse_1_pos, horse_2_pos, horse_3_pos, horse_4_pos))),
                                                 colour=bot_embed_colour)
                horse_racing_msg.set_author(name="Horse Racing:",
                                            icon_url=client.user.avatar_url)
                horse_racing_msg_edit = await client.edit_message(horse_racing_msg_msg, embed=horse_racing_msg)
                horse_racing_msg_msg = horse_racing_msg_edit

                await asyncio.sleep(2)

                winner = []

                if horse_1_pos == 10:
                    game_not_finished = False
                    winner.append(1)

                if horse_2_pos == 10:
                    game_not_finished = False
                    winner.append(2)

                if horse_3_pos == 10:
                    game_not_finished = False
                    winner.append(3)

                if horse_4_pos == 10:
                    game_not_finished = False
                    winner.append(4)

            if len(winner) != 1:
                winner = random.choice(winner)
            else:
                winner = winner[0]

            if winner == player_no:
                horse_racing_msg = discord.Embed(title="",
                                                 description=(str(utils.re_draw_horse_race(horse_1_pos, horse_2_pos, horse_3_pos, horse_4_pos)) + "\n\nWinner Horse: " + str(winner) + "\n\nYou Win. GG " + str(ctx.message.author.name)),
                                                 colour=bot_embed_colour)
                horse_racing_msg.set_author(name="Horse Racing:",
                                            icon_url=client.user.avatar_url)
                await client.edit_message(horse_racing_msg_msg, embed=horse_racing_msg)

            else:
                horse_racing_msg = discord.Embed(title="",
                                                 description=(str(utils.re_draw_horse_race(horse_1_pos, horse_2_pos, horse_3_pos, horse_4_pos)) + "\n\nWinner Horse: " + str(winner) + "\n\nYou Didnt Win This Time. GG " + str(ctx.message.author.name)),
                                                 colour=bot_embed_colour)
                horse_racing_msg.set_author(name="Horse Racing:",
                                            icon_url=client.user.avatar_url)
                await client.edit_message(horse_racing_msg_msg, embed=horse_racing_msg)

    @client.command(pass_context = True)
    async def rps(ctx, *, text: str=None):
        if text is None:
            invalid_entry_msg = discord.Embed(title="",
                                              description="Please Input a Valid Arguement.\n\nExample: **y!rps rock**",
                                              colour=bot_embed_colour)
            invalid_entry_msg.set_author(name="Invalid Arguement:",
                                         icon_url=client.user.avatar_url)
            await client.say(embed=invalid_entry_msg)

        elif text.lower() != "rock" and text.lower() != "paper" and text.lower() != "scissors":
            invalid_entry_msg = discord.Embed(title="",
                                              description="Please Input a Valid Arguement.\n\nExample: **y!rps rock**",
                                              colour=bot_embed_colour)
            invalid_entry_msg.set_author(name="Invalid Arguement:",
                                         icon_url=client.user.avatar_url)
            await client.say(embed=invalid_entry_msg)

        else:
            player_responce = text.lower()
            rps_responce = random.choice(var_list.rps_outcomes).lower()

            if player_responce == rps_responce:
                rps_output = discord.Embed(title="",
                                           description=("YOU = " + str(utils.rps_get_emoji(player_responce)) + " v " + str(utils.rps_get_emoji(rps_responce)) + " = ME\n\nIt Is A Draw. GG " + str(ctx.message.author.name)),
                                           colour=bot_embed_colour)
                rps_output.set_author(name="Rock Paper Scissors Outcome:",
                                      icon_url=client.user.avatar_url)

                await client.say(embed=rps_output)

            elif player_responce == "rock":
                if rps_responce == "paper":
                    rps_output = discord.Embed(title="",
                                               description=("YOU = " + str(utils.rps_get_emoji(player_responce)) + " v " + str(utils.rps_get_emoji(rps_responce)) + " = ME\n\nI Win. GG " + str(ctx.message.author.name)),
                                               colour=bot_embed_colour)
                    rps_output.set_author(name="Rock Paper Scissors Outcome:",
                                          icon_url=client.user.avatar_url)

                    await client.say(embed=rps_output)

                elif rps_responce == "scissors":
                    rps_output = discord.Embed(title="",
                                               description=("YOU = " + str(utils.rps_get_emoji(player_responce)) + " v " + str(utils.rps_get_emoji(rps_responce)) + " = ME\n\nYou Have Defeated Me. GG " + str(ctx.message.author.name)),
                                               colour=bot_embed_colour)
                    rps_output.set_author(name="Rock Paper Scissors Outcome:",
                                          icon_url=client.user.avatar_url)

                    await client.say(embed=rps_output)

            elif player_responce == "paper":
                if rps_responce == "rock":
                    rps_output = discord.Embed(title="",
                                               description=("YOU = " + str(utils.rps_get_emoji(player_responce)) + " v " + str(utils.rps_get_emoji(rps_responce)) + " = ME\n\nYou Have Defeated Me. GG " + str(ctx.message.author.name)),
                                               colour=bot_embed_colour)
                    rps_output.set_author(name="Rock Paper Scissors Outcome:",
                                          icon_url=client.user.avatar_url)

                    await client.say(embed=rps_output)

                elif rps_responce == "scissors":
                    rps_output = discord.Embed(title="",
                                               description=("YOU = " + str(utils.rps_get_emoji(player_responce)) + " v " + str(utils.rps_get_emoji(rps_responce)) + " = ME\n\nI Win. GG " + str(ctx.message.author.name)),
                                               colour=bot_embed_colour)
                    rps_output.set_author(name="Rock Paper Scissors Outcome:",
                                          icon_url=client.user.avatar_url)

                    await client.say(embed=rps_output)

            elif player_responce == "scissors":
                if rps_responce == "rock":
                    rps_output = discord.Embed(title="",
                                               description=("YOU = " + str(utils.rps_get_emoji(player_responce)) + " v " + str(utils.rps_get_emoji(rps_responce)) + " = ME\n\nI Win. GG " + str(ctx.message.author.name)),
                                               colour=bot_embed_colour)
                    rps_output.set_author(name="Rock Paper Scissors Outcome:",
                                          icon_url=client.user.avatar_url)

                    await client.say(embed=rps_output)

                elif rps_responce == "paper":
                    rps_output = discord.Embed(title="",
                                               description=("YOU = " + str(utils.rps_get_emoji(player_responce)) + " v " + str(utils.rps_get_emoji(rps_responce)) + " = ME\n\nYou Have Defeated Me. GG " + str(ctx.message.author.name)),
                                               colour=bot_embed_colour)
                    rps_output.set_author(name="Rock Paper Scissors Outcome:",
                                          icon_url=client.user.avatar_url)

                    await client.say(embed=rps_output)

    @client.command(pass_context = True)
    async def say(ctx, *, text: str=None):
        say_msg = discord.Embed(title="",
                                description=text,
                                colour=bot_embed_colour)
        say_msg.set_author(name="Say Response:")
        await client.say(embed=say_msg)

    @client.command(pass_context = True)
    async def say_emoji(ctx, *, text: str=None):
        arguements_split = list(text)
        converted_msg = ""
        for charactor in arguements_split:
            try:
                _index_ = var_list.say_emoji.allowed_keys.index(charactor.lower())
                converted_msg += var_list.say_emoji.key_outputs[_index_]
            except ValueError:
                pass
        say_emoji_msg = discord.Embed(title="",
                                      description=converted_msg,
                                      colour=bot_embed_colour)
        say_emoji_msg.set_author(name="Say Emoji Response:")
        await client.say(embed=say_emoji_msg)

client.run(BOT_TOKEN)