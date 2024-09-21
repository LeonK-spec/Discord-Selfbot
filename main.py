import selfcord
import json, base64
import string, re
import  random
import aiohttp
t = "TOKEN_HERE" #token

bot = selfcord.Bot(prefixes=["!", "+"])
prefix = "+"

nitrosniper = True
stop_flag = False

@bot.on("ready")
async def ready(time):
    print(f"Connected To {bot.user.name}\nStartup took {time:0.2f} seconds")


@bot.on("member_chunk")
async def membershit(members, other, join, leave):
    member_data = []
    
    if members is None:
        return
    for member in members:
        member_data.append({
            "name": member.name,
            "discriminator": member.discriminator,
            "id": member.id,
            "created_at:": str(member.created_at)
        })

    with open('guild_members.json', 'w') as json_file:
        json_file.write("[\n")
        for i, item in enumerate(member_data):
            if i > 0:
                json_file.write(",\n")
            json_file.write(json.dumps(item))
        json_file.write("\n]")

@bot.on("message")
async def reader(message):
        with open(f"logs.txt", "a", encoding="utf-8") as f:
                f.write(f"{message.author} ["+str(message)+f"] in ({message.guild})\n")

        print(message)
        if "discord.gift/" in str(message):
                    nitro_code = re.search(r'discord\.gift\/([\w\d]+)', message.content).group(1)
                    print(f"Got nitro {message}")
                    await bot.redeem_nitro(nitro_code)


@bot.cmd(description="Purges the channel", aliases=["wipe", "clear"])
async def purge(ctx, amount: int=None):
    await ctx.purge(amount)

@bot.cmd(description="DISCORDR RPC")
async def changerpc(ctx, status: str, message:str, emoji:str=None):
    await bot.change_status(status=status,message=message, emoji=emoji)


@bot.cmd(description="[Usage: !selfcmd 'subcommand' content message emoji]\n       join, changestatus, changepass,\n       addfriend, redeemnitro, changepfp\n       block, hypesquad, editprofile \n\n")
async def selfcmd(ctx, sub_command:str, content:str=None, message:str=None, emoji:str=None):
    if sub_command == "join":
        await bot.join_invite(content)
    elif sub_command == "changestatus":
        await bot.change_status(status=content, message=message, emoji=emoji)
    elif sub_command == "changepass":
        await ctx.edit("nothing to see here u cock uwu")
        await bot.change_pass(content, message)
        print("Changed password UwU46")
    elif sub_command == "addfriend":
        await bot.add_friend(content)
    elif sub_command == "redeemnitro":
        await bot.redeem_nitro(content)
    elif sub_command == "changepfp":
        await bot.change_pfp(avatar_url=content)
    elif sub_command == "block":
        await bot.block(content)
    elif sub_command == "hypesquad":
        await bot.change_hypesquad(content)
    elif sub_command == "editprofile":
        await bot.edit_profile(content, message)
    elif sub_command == "createserver":
        await bot.create_guild(content, None, "2TffvPucqHkN")

@bot.cmd(description="[Usage : !dmcmd")
async def dmcmd(ctx, sub_command: str, amount:int):
    if sub_command =="purge":
        await ctx.purge(amount=amount)



@bot.cmd(description="[Usage: !user 'subcommand' User]\n       username, avatar, token, dm\n\n")
async def user(ctx, sub_command: str, user: selfcord.User=None, message:str=None, timemsg:str=None):
    if sub_command == "username":
        await ctx.edit(f"Username: {user.name}")
    elif sub_command == "avatar":
        await ctx.edit(f"{user.avatar_url}")
    elif sub_command == "token":
        mid = user.id
        id_ascii = mid.encode("ascii")
        id_base64 = base64.b64encode(id_ascii)
        id_idk = id_base64.decode("ascii")
        timest = "".join(random.choices(string.ascii_letters + string.digits + "-" + "_", k=6))
        last = "".join(random.choices(string.ascii_letters + string.digits + "-" + "_", k=27))
        await ctx.edit(f'{id_idk}.{timest}.{last}')
    elif sub_command == "dm":
        await user.create_dm()
    elif sub_command == "spam":
        amt = int(input("how many times nga >> "))
        msg = input("how many text nga >> ")
        for _ in range(amt):
            await ctx.send(str(msg))




@bot.cmd(description="[Usage: !server 'subcommand' amount content both optional]\n       showchannels, showroles, kickall,\n       sendall, deletechannels, deleteroles,\n       createchannels, createroles \n\n")
async def server(ctx, sub_command:str, amount:int=None, content:str=None):

    if sub_command == "dmserver":
        with open('guild_members.json', 'r') as json_file:
            member_data = json.load(json_file)


        for member_info in member_data:
            member_id = member_info["id"]
            await ctx.guild.create_dm(member_id)

    if sub_command == "showchannels":
        await ctx.send(", ".join([str(r.name) for r in ctx.guild.channels]))
    if sub_command == "showroles":
        await ctx.send(" ".join([str(r.name) for r in ctx.guild.roles]))

    if sub_command == "kickall":
        for i in ctx.guild.members:
            await ctx.guild.kick(i.id)
    if sub_command == "banall":
        for u in ctx.guild.members:
            await ctx.guild.ban(str(u.id))
            print(u.id)

    if sub_command == "fetchmembers":
            await ctx.guild.get_members(ctx.channel.id)

    if sub_command == "sendall":
        for channel in ctx.guild.channels:
            for _ in range(amount):
                await channel.send(content)

    if sub_command == "createchannels":
        for _ in range(amount):
            await ctx.guild.txt_channel_create(content)

    if sub_command == "createroles":
        for _ in range(int(amount)):
            await ctx.guild.role_create(content)

    if sub_command == "createadminrole":

        roletoedit = await ctx.guild.role_create("Member69420")
        await roletoedit.admin()

    if sub_command == "createeveryonerole":

        role = await ctx.guild.role_create("YARRAMMMM")
        for member in ctx.guild.members:
            await member.add_roles(role)

    if sub_command == "createwebhook":
        webhook = await ctx.channel.create_webhook("Guard-Hook")
        await webhook.send(content)
    if sub_command == "deletewebhooks":
        for webhook in ctx.channel.webhooks:
            await webhook.delete()
    if sub_command == "deletechannels":
        for channels in ctx.guild.channels:
            await channels.delete()
    if sub_command == "deleteroles":
        try:
            for roles in ctx.guild.roles:
                await roles.delete()
        except aiohttp.ClientConnectionError as e:
                print(f"Trying to delete the @everyone role?\n{e}")


@bot.cmd(description="[Usage : !token sub token]\n       info")
async def token(ctx,sub , token:str):



        if sub == "info":
                msg = ctx.message
                async with aiohttp.ClientSession() as http:
                    r_user = await http.get(
                        "https://discord.com/api/v9/users/@me",
                        headers={
                           "authorization": token,
                            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9011 Chrome/91.0.4472.164 Electron/13.6.6 Safari/537.36"
                        })

                    nitro_types = {
                            "1": "Classic",
                            "2": "Monthly"
                        }

                    try:
                            js = await r_user.json()
                            try:
                                n = nitro_types[str(js["premium_type"])]

                            except Exception as e:
                                n = "None"

                            invalid_chars = "#%&{}\<>*?/ $!'\":@+`|="
                            username = f"{js['username']}#{str(js['discriminator'])}"
                            for char in invalid_chars:
                                if char in username:
                                    username = username.replace(char, "_")

                            info = f"""- Token: {token}
                            - Username: {js["username"]}#{js["discriminator"]}
                            - ID: {js["id"]}
                            - Email: {js["email"]}
                            - Phone: {js["phone"]}
                            - Avatar URL: https://cdn.discordapp.com/avatars/{js["id"]}/{js["avatar"]}.png?size=2048
                            - Banner URL: https://cdn.discordapp.com/banners/{js["id"]}/{js["banner"]}.png?size=2048
                            - Bio: {None if js["bio"] == "" else js["bio"]}
                            - Locale: {js["locale"]}
                            - 2FA Enabled: {js["mfa_enabled"]}
                            - Verified: {js["verified"]}
                            - Nitro Subscription: {n}"""

                            with open(f"./info/tokens/TOKEN_INFO {username}.txt", "w", encoding="utf-8") as f:
                                f.write(info)

                            with open(f"./info/tokens/TOKEN_INFO {username}.txt", "rb") as f:
                                await ctx.send(content=f"```yaml\n{info}```")

                    except Exception as e:
                        await ctx.send(f"""```yaml\n- Error: {e}```""", delete_after=5)

                        await msg.delete()




bot.run(t)
