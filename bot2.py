
import discord
from discord.ext import commands
import random
import asyncio

description = "free democracy bot 2.0 : Starting up"
intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='-', description=description, intents=intents)

past_kicked_users = [] 
is_voting = False
yes_votes = 0
no_votes = 0

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
            await ctx.send(ctx.author.id + "has voted yes!")
            yes_votes += 1
        if msg == 'no':
            await ctx.send(ctx.author.id + " has voted no!")
            no_votes += 1
    else:
        await ctx.send("you can't vote right now!")


@bot.command()
async def votekick(ctx, user:discord.User):
    global is_voting
    global past_kicked_users
    global yes_votes
    global no_votes
    if type(user) != discord.User:
        await ctx.send("you need to select someone to vote kick first!")
    else:
        past_kicked_users.append(user)
        is_voting = True
        await  ctx.send("starting votekick for user:" + str(user))
        await ctx.send("type \"vote yes\" or \"vote no\" to cast your vote!\n if the majority of votes are in favor, the defendent shall be kicked")
        await asyncio.sleep(15)
        await ctx.send("voting is finished!")
        is_voting = False
        await ctx.send("total yes votes: " + str(yes_votes) + "\ntotal no votes: " + str(no_votes))
        if yes_votes > no_votes:
            await ctx.send("by law of the people of" + ctx.message.guild.name + ", the defendant is guilty! Prepare to be kicked. \n You have ten seconds left to say your last words.")
        yes_votes = 0
        no_votes = 0

@bot.command()
async def repeat(ctx, times: int, content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(times):
        await ctx.send(content)



bot.run('Njk4NDY3MDE4MjE0NzM1OTEy.XpGQGg.eMAh_bYPd10SNU4zFaAFYfwDHfA')
