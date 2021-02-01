invLink = "https://discord.com/oauth2/authorize?client_id=676422935933878282&scope=bot"

reaction_no = 10060
reaction_yes = 9989

import discord
import asyncio

from discord.activity import Game

from blackjack import game

def toList(l):
    newL = []
    for i in range(len(l)):
        newL.append(l.__getitem__(i))
    return newL

class MyClient(discord.Client):
    blackjackGames = dict()

    def is_me(self, m):
        return m.author == self.user

    isUpdatingGames = False
    async def update_blackjackgames(self):
        while True:
            for game in list(self.blackjackGames.values()):
                await game.Update()
            await asyncio.sleep(1)

    async def end_blackjackgames(self):
        for game in list(self.blackjackGames.values()):
            await game.statusMessageObject.delete()

    async def CreateBlackjackGame(self, channel, host):
        bjg = game.Blackjack(channel, host, self.loop)
        self.blackjackGames[channel.id] = bjg
        bjg.AddPlayer(host)
        #bjg = blackjack.MultiplayerBlackjack(channel, host)
        if not self.isUpdatingGames:
            self.loop.create_task(self.update_blackjackgames())
            self.isUpdatingGames = True

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
        g = self.guilds.__getitem__(0)
        print('RUNNING...')

        with open('blackjackhelp.txt', 'r') as f:
            self.blackjackHelp = f.read()

    async def on_message(self, message):
        guild = message.guild
        channel = message.channel
        author = message.author
        textContent = message.content
        attachments = toList(message.attachments)
        
        if message.author == guild.me:
            return

        if ("ching" in message.content.lower() and "chong" in message.content.lower()):
            g = self.guilds.__getitem__(0)
            await channel.send(content='Ебать')
        if ("allukala" in message.content.lower()):
            g = self.guilds.__getitem__(0)
            await channel.send(content='*allukalu')
            #await message.delete()
            #await channel.send(content=(textContent.lower().replace('allukala', 'allukalu')))
        elif ("invite" in message.content.lower()):
            g = self.guilds.__getitem__(0)
        #elif ("help" in message.content.lower()):
        #    await channel.send(content="I'm autocorrect")
        elif ("!blackjack" in message.content.lower()):
            await self.CreateBlackjackGame(channel, author)
            
            await message.delete()
        elif "shutdown" in message.content.lower():
            await self.end_blackjackgames()
            exit()
        elif "purgekomrade" in message.content.lower():
            await channel.purge(limit=500, check=self.is_me)
        elif "purgewholechannelatonce123123" in message.content.lower():
            await channel.purge(limit=500)
        elif "purge" == message.content.lower()[:5]:
            await channel.send(content="if you send message containing string \"purgewholechannelatonce123123\" will purge 500 last messages", delete_after=7)
                    
        
        if (channel.id in list(self.blackjackGames.keys())):
            bjg = self.blackjackGames[channel.id]
            #if ("start" == message.content.lower()[:5]):
            #    bjg.gameState += 1
            if ("join" == message.content.lower()[:4]):
                bjg.AddPlayer(author)
                await channel.send(content=f"Welcome to the game {author.name}!", delete_after=3)
                await message.delete()
            #elif ("continue" == message.content.lower()[:8]):
            #    self.blackjackGames[channel.id].RunRound()
            elif ("bet" == message.content.lower()[:3]):
                await bjg.OnBet(author, message.content.lower().split(' ')[1])
                await message.delete()
            elif "ready" in message.content.lower():
                await game.Blackjack.SetPlayerReady(bjg, author)
                await message.delete()
            elif "autobet" == message.content.lower()[:7]:
                if message.content.lower().split(' ')[1] == "off":
                    await game.Blackjack.SetAutoBet(bjg, author, 0)
                else:    
                    await game.Blackjack.SetAutoBet(bjg, author, message.content.lower().split(' ')[1])
            elif "help" in message.content.lower():
                await channel.send(content=self.blackjackHelp)
            await message.delete()
            



    async def on_reaction_add(self, reaction, user):
        #print(ord(reaction.emoji))
        message = reaction.message
        channel = message.channel
        if user.id == message.guild.me.id:
            return
        if (channel.id in list(self.blackjackGames.keys())):
            game = self.blackjackGames[channel.id]
            
            if (message == game.mainEmbedObject):
                game.OnReaction(user, ord(reaction.emoji))
                await game.Update()
                
                # clear reactions
                await message.clear_reaction(reaction)
                await message.add_reaction(reaction)

client = MyClient()
token = str()
with open('token.tkn', 'r') as f:
    token = f.read()
    f.close()

client.run(token)
