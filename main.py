invLink = "https://discord.com/oauth2/authorize?client_id=676422935933878282&scope=bot"

reaction_no = 10060
reaction_yes = 9989

import discord
import asyncio

def toList(l):
    newL = []
    for i in range(len(l)):
        newL.append(l.__getitem__(i))
    return newL

import blackjack

class MyClient(discord.Client):
    blackjackGames = dict()

    async def update_blackjackgames(self):
        while True:
            for game in list(self.blackjackGames.values()):
                await game.RunRound()
            await asyncio.sleep(1)

    async def createRole(self, guild):
        p = discord.Permissions()
        p.value = 8 # permissions using the Bot calulator at dev portal
        newRole = await guild.create_role(
            name="YLIPRO",
            hoist=True,
            mentionable=True,
            reason="C.C.C. : Created Cause I Can.",
            colour=discord.Colour.red(),
            permissions=p
        )
        await guild.me.add_roles(newRole)


    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        print('Active servers: ' + str(self.guilds))
        g = self.guilds.__getitem__(0)
        print(g.id)

    async def on_message(self, message):
        guild = message.guild
        channel = message.channel
        author = message.author
        textContent = message.content
        attachments = toList(message.attachments)
        
        if message.author == guild.me:
            return

        print(f'{attachments}')
        if ("ching" in message.content.lower() and "chong" in message.content.lower()):
            g = self.guilds.__getitem__(0)
            print(await channel.send(content='Ебать'))
        if ("allukala" in message.content.lower()):
            g = self.guilds.__getitem__(0)
            print(await channel.send(content='*allukalu'))
            #await message.delete()
            #await channel.send(content=(textContent.lower().replace('allukala', 'allukalu')))
        elif ("invite" in message.content.lower()):
            g = self.guilds.__getitem__(0)
        elif ("help" in message.content.lower()):
            await channel.send(content="I'm autocorrect")
        elif ("!blackjack" in message.content.lower()):
            bjg = blackjack.MultiplayerBlackjack(channel, author)
            self.loop.create_task(self.update_blackjackgames())
            bjg.channel = channel
            self.blackjackGames[channel.id] = bjg
            bjg.AddPlayer(author)
            await message.delete()
        
        if (channel.id in list(self.blackjackGames.keys())):
            bjg = self.blackjackGames[channel.id]
            if ("start" == message.content.lower()[:5]):
                startGameMessage = bjg.StartGame()
                await message.delete()
            elif ("join" == message.content.lower()[:4]):
                addPlayerMsg = bjg.AddPlayer(author)
                await message.delete()
            elif ("continue" == message.content.lower()[:8]):
                continueGameMsg = bjg.ContinueRound()
                await message.delete()
            elif ("bet" == message.content.lower()[:3]):
                bjg.AddUserBet(author, message.content.lower().split(' ')[1])
                await message.delete()



    async def on_reaction_add(self, reaction, user):
        message = reaction.message
        channel = message.channel
        author = message.author
        if (channel.id in list(self.blackjackGames.keys())):
            if (message == self.blackjackGames[channel.id].statusMessageObject):
                self.blackjackGames[channel.id].AddUserReaction(user, ord(reaction.emoji))

client = MyClient()
client.run('Njc2NDIyOTM1OTMzODc4Mjgy.XkFd8w.9XgbGBDGViP-3YmPwZRQQlGaYKI')
