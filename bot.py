import discord


class MyClient(discord.Client):

    vote_mode = True
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')


    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return

        if message.content.startswith('!hello'):
            await message.reply('Hello!', mention_author=True)

        if message.content.startswith("!votekick"):
            await message.reply("starting votekick for user:", 
            try:
                guess = await self.wait_for('message', check=is_correct, timeout=5.0)
            except asyncio.TimeoutError:
                return await message.channel.send('Sorry, you took too long it was {}.'.format(answer))

            if int(guess.content) == answer:
                await message.channel.send('You are right!')


        if message.content.startswith("!help"):
            await message.reply('Welcome to the freedemocracybot!\nCommands\n!votekick: votes to kick a user")

client = MyClient()
client.run('token')
