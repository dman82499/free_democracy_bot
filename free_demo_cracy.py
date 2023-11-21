
import discord
from discord.ext import commands
import random
import asyncio
import knuckles_memelist
try:
    import key
except:
    print("You need to insert a custom key!")

description = "free democracy bot 2.0 : Starting up"
intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix='/', description=description, intents=intents)


past_kicked_users = {}
voted_users = []
is_voting = False
kicked_user = None
yes_votes = 0
no_votes = 0
use_vote_system = True
channel = bot.get_all_channels()

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

#@bot.event
#async def on_message(message):
#    print(message.content)

async def process_vote():
    await asyncio.sleep(2)

@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)

@bot.command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)


@bot.command(description='For when you wanna settle the score some other way')
async def choose(ctx, *choices: str):
    """Chooses between multiple choices."""
    await ctx.send(random.choice(choices))




@bot.command()
async def vote(ctx, msg:str):
    global is_voting
    bot_vote = is_voting
    global yes_votes
    global no_votes
    if is_voting:
        if msg == 'yes':
            await ctx.send(ctx.author.mention + "has voted yes!")
            yes_votes += 1
        if msg == 'no':
            await ctx.send(ctx.author.mention + " has voted no!")
            no_votes += 1
    else:
        await ctx.send("you can't vote right now!")


@bot.event
async def on_reaction_add(reaction, user):
    global voted_users
    if user.bot:
        return
    global is_voting
    global yes_votes
    global no_votes
    
    emoji = reaction.emoji
    #this will eventually be changed to a fixed channel

    if is_voting:
        if user in voted_users:
            await bot.get_channel(id=1).send(user.mention + ", you have already voted and cannot vote twice!")
        else:
            if emoji == "✅":
                await bot.get_channel(id=1).send(user.mention +" voted yes!")
                yes_votes += 1
            if emoji == "❌":
                no_votes += 1
                #await cxt.send(user.mention+ " voted no!")
            voted_users.append(user)



@bot.command()
async def votekick(ctx, user:discord.Member):
    global is_voting
    global past_kicked_users
    global kicked_user
    global yes_votes
    global no_votes
    global use_vote_system
    global voted_users
    if use_vote_system:
        if type(user) != discord.Member:
            await ctx.send("you need to select someone to vote kick first!")
        else:
            kicked_user = user

            is_voting = True
            vote_message = await  ctx.send("starting votekick for user:" + str(user))
            await vote_message.add_reaction("✅")
            await vote_message.add_reaction("❌")

            #await ctx.send("type \"vote yes\" or \"vote no\" to cast your vote!\n if the majority of votes are in favor, the defendent shall be kicked")
            await asyncio.sleep(15)
            await ctx.send("voting is finished!")
            voted_users = []
            is_voting = False

            await ctx.send("total yes votes: " + str(yes_votes) + "\ntotal no votes: " + str(no_votes))
            if yes_votes > no_votes:
                if yes_votes > 0:
                    await ctx.send("By law of the people of " + ctx.message.guild.name + ", the defendant "+ user.mention+ "is guilty! Prepare to be kicked. \n You have ten seconds left to say your last words.")

                    try:
                        invite = await ctx.channel.create_invite()
                    except Exception:
                        await ctx.send("rip, I don't have permissions, or the user trying to be kicked is admin or some shit")
                        yes_votes = 0
                        no_votes = 0
                        return

                    await user.send(invite)

                    await user.send("You have been kicked. You can get back in the server with the above invite link.")
                    past_kicked_users[user] = user.roles
                    #old_roles = user

                    await asyncio.sleep(10)
                    try:
                        await user.kick()
                    except Exception:
                        await ctx.send("rip, I don't have permissions, or the user trying to be kicked is admin or some shit")
                        yes_votes = 0
                        no_votes = 0
                else:
                    await ctx.send("there are not enough users to votkick this user! (required: 3)")
            yes_votes = 0
            no_votes = 0


@votekick.error
async def votekick_error(ctx, message):
    await ctx.send("you must pick a valid user to kick!")

@bot.command()
async def die(ctx):
    print("die command executed")
    await ctx.send("k bitch :(")

@bot.command()
async def rate_meme(ctx, message:discord.Attachment=None):
    #print(message)
    #if message is None:
   #     await ctx.send("You need to send a valid meme!")
    #else:
    embed_msg = discord.Embed(description="rating meme for:")
    embed_msg.set_image(url=message.url)
    rand_number = random.randint(0, len(knuckles_memelist.memes)-1)
    await ctx.send(f"rating meme for:", embed=embed_msg)
    await asyncio.sleep(2)
    await ctx.send(knuckles_memelist.memes[rand_number])
@rate_meme.error
async def rate_meme_error(ctx, error):
    await ctx.send("You need to send a valid meme!")


    #file_name = r"c:\location\of\the_file_to\send" + str(rand_number)+ ".mp4"
    #area = ctx.message.channel
    #await ctx.send(file=discord.File(file_name))



@bot.command()
async def fortnite(ctx, msg:int):
    lmao = '''AMONGUS Among Us[c] is an online multiplayer social deduction game developed and published by American game studio Innersloth. It was released on iOS and Android devices in June 2018 and on Windows in November 2018, 
    featuring cross-platform play between these platforms.[4] The game was also ported for the Nintendo Switch in December 2020, and 
    has planned releases for the Xbox One and Xbox Series X and Series S in 2021. The game was inspired by the party game Mafia and the science fiction horror film The Thing, and since the release of its first map, The Skeld, other maps were added into the game. A fourth map, "The Airship", is set to be released in March 2021.

The game takes place in a space-themed setting, in which players each take on one of two roles, most being Crewmates, and a predetermined number being Impostors.[d] The goal of the Crewmates is to identify the Impostors, 
eliminate them, and complete tasks around the map; the Impostors' goal is to covertly sabotage and kill the Crewmates before they complete all of their tasks. Players suspected to 
be Impostors may be eliminated via a plurality vote, which any player may initiate by calling an emergency meeting (except during a crisis) or reporting a dead body. Crewmates win if all Impostors are eliminated or all tasks are completed whereas Impostors win if there is an equal number of Impostors and Crewmates, or if a critical sabotage goes unresolved.'''

    if msg:
        for x in range(0, msg):
            await ctx.send(lmao)
    else:
        await ctx.send(lmao)

@fortnite.error
async def fortnite_error(ctx, error):
    lmao = '''AMONGUS Among Us[c] is an online multiplayer social deduction game developed and published by American game studio Innersloth. It was released on iOS and Android devices in June 2018 and on Windows in November 2018, 
        featuring cross-platform play between these platforms.[4] The game was also ported for the Nintendo Switch in December 2020, and 
        has planned releases for the Xbox One and Xbox Series X and Series S in 2021. The game was inspired by the party game Mafia and the science fiction horror film The Thing, and since the release of its first map, The Skeld, other maps were added into the game. A fourth map, "The Airship", is set to be released in March 2021.

    The game takes place in a space-themed setting, in which players each take on one of two roles, most being Crewmates, and a predetermined number being Impostors.[d] The goal of the Crewmates is to identify the Impostors, 
    eliminate them, and complete tasks around the map; the Impostors' goal is to covertly sabotage and kill the Crewmates before they complete all of their tasks. Players suspected to 
    be Impostors may be eliminated via a plurality vote, which any player may initiate by calling an emergency meeting (except during a crisis) or reporting a dead body. Crewmates win if all Impostors are eliminated or all tasks are completed whereas Impostors win if there is an equal number of Impostors and Crewmates, or if a critical sabotage goes unresolved.'''
    await ctx.send(lmao)
@bot.command()
async def repeat(ctx, times: int, content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(times):
        await ctx.send(content)

@bot.event
async def on_member_join(member):
  global past_kicked_users
  if member in past_kicked_users.keys():
      roles = past_kicked_users[member]
      member.add_roles(roles)


@bot.command()
async def set_channel(ctx, a:str):
    global channel
    await ctx.send("set the channel to this one!")
    channel = ctx.message.channel
    print("lol")

# You will need to insert a custom key here if you would like to host
bot.run(key.token)
