
import discord
from discord.ext import commands
import random
import asyncio

description = "free democracy bot 2.0 : Starting up"
intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='@', description=description, intents=intents)

past_kicked_users = [] 


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
async def votekick(ctx, user:discord.user):
    if type(user) != discord.user:
        await ctx.send("you need to select someone to vote kick first!")
    else:
        past_kicked_users.append(user)
        await  ctx.send("starting votekick for user:", user)
        await ctx.send("type \"voteyes\" or \"voteno\" to cast your vote!\n if the majority of votes are in favor, the defendent shall be kicked")
        await asyncio.sleep(10)
        await ctx.send("voting is finished!")

@bot.command()
async def repeat(ctx, times: int, content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(times):
        await ctx.send(content)



bot.run('token')
