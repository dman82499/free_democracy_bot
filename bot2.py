
import discord
from discord.ext import commands
import random
import asyncio

description = "free democracy bot 2.0 : Starting up"
intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='-', description=description, intents=intents)

past_kicked_users = {}
voted_users = []
is_voting = False
kicked_user = None
yes_votes = 0
no_votes = 0
use_vote_system = True
channel = None

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


async def process_vote():
    await asyncio.sleep()

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
    global channel
    emoji = reaction.emoji
    #this will eventually be changed to a fixed channel
    cxt = channel
    if is_voting:
        if user in voted_users:
            await cxt.send(user.mention + ", you have already voted and cannot vote twice!")
        else:
            if emoji == "✅":
                await cxt.send(user.mention +" voted yes!")
                yes_votes += 1
            if emoji == "❌":
                no_votes += 1
                await cxt.send(user.mention+ " voted no!")
            voted_users.append(user)



@bot.command()
async def votekick(ctx, user:discord.Member):
    global is_voting
    global past_kicked_users
    global kicked_user
    global yes_votes
    global no_votes
    global use_vote_system
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
            is_voting = False
            await ctx.send("total yes votes: " + str(yes_votes) + "\ntotal no votes: " + str(no_votes))
            if yes_votes > no_votes:
                await ctx.send("By law of the people of " + ctx.message.guild.name + ", the defendant "+ user.mention+ "is guilty! Prepare to be kicked. \n You have ten seconds left to say your last words.")
            yes_votes = 0
            no_votes = 0

            invite = await ctx.channel.create_invite()
            await user.send(invite)

            await user.send("You have been kicked. You can get back in the server with the above invite link.")
            past_kicked_users[user] = user.roles
            #old_roles = user
            await asyncio.sleep(10)
            await user.kick()



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


bot.run('')
