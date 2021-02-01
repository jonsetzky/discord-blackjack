

reaction_hit = 128994
reaction_stand = 128308
reaction_double = 128309
reaction_split = 128993

import time

import discord

import asyncio

from .card import Card
from .dealer import Dealer
from .hand import Hand
from .player import Player

updateQueue = {
            'add_reaction': [],
            'send_embed': [],
            'edit_embed': []
        }

# a thread that updates discrod
async def UpdateDiscordThread():
    global updateQueue
    while True:
        for (key, value) in list(updateQueue.items()):
            if key == 'add_reaction' and len(value) > 0:
                for react in value:
                    await discord.Message.add_reaction(react[0], react[1])
            if key == 'send_embed' and len(value) > 0:
                await discord.TextChannel.send(value[0], embed=value[1])
            if key == 'edit_embed' and len(value) > 0:
                for edit in value:
                    await discord.Message.edit(edit[0], embed=edit[1])
        await asyncio.sleep(1)

class Blackjack():

    global updateQueue

    def __init__(self, channel, host, loop):
        self.host = host

        self.players = dict()
        self.dealer = Dealer()

        self.addedReactions = dict()
        self.addedBets = dict()

        self.resultsShowTime = 0
        self.resultsShowTimeSet = False

        self.dealerEmbedObject = None

        self.mainEmbed = {
            'title': 'Set your bets using the command "bet <amount>". Use command "ready" when you are ready.',
            'description': 'Loading...',
            'color': 16711680,
            'footer': {'text': 'Note that all messages sent during the game will be deleted immediately'}
        }
        self.mainEmbedObject = None
        self.mainEmbedReactions = list()
        self.mainEmbedShouldUpdate = True

        self.channel = channel
        
        # the state defines what is happening in the game
        # 0 - get bets from players
        # 1 - deal cards
        # 2 - get player actions
        # 3 - get dealer actions
        # 4 - show results
        # 5 - commit results
        # repeat
        self.state = 0
        self.lastState = 0

        self.dealer.Shuffle(4)

        #asyncio.create_task(UpdateDiscordThread())

    def allPlayersReady(self):
        for player in list(self.players.values()):
            if player.isReady == False:
                return False
        return True

    def AddPlayer(self, author):
        newPlayer = Player()
        newPlayer.money = 50
        newPlayer.author = author
        self.players[author.id] = newPlayer

    async def OnBet(self, author, amount):
        self.addedBets[author] = amount
        await self.UpdatePlayerEmbed(self.players[author.id])

    def OnReaction(self, author, reactionOrd):
        self.addedReactions[author] = reactionOrd
        return

    async def SetBet(self, player, bet):
        h = Hand()
        h.bet = int(bet)
        player.hands.append(h)
        player.money = player.money - int(bet)


    def NextState(self):
        self.lastState = self.state
        for player in list(self.players.values()):
            player.isReady = False
        self.state += 1

    async def CreateEmbeds(self):
        self.dealerEmbedObject = await self.channel.send(embed=discord.Embed.from_dict({
            'title': 'Dealer',
            'color': 16711680
        }))

        self.playerEmbeds = list()
        for player in list(self.players.values()):
            self.playerEmbedsObjects[player.author.id] = await self.channel.send(embed=discord.Embed.from_dict({
                'title': f'{player.author.name}',
                'color': 16711680
            }))

        self.mainEmbedObject = await self.channel.send(embed=discord.Embed.from_dict({
            'title': 'Loading..',
            'color': 16711680,
            'fields': list()
        }))

    async def UpdateDealerEmbed(self):
        dealerEmbedDict = {
            'title': 'Dealer Vladimir',
            'color': 16711680,
            'fields': list()
        }
        dealerEmbedDict['fields'].append({
                'name': 'Hand',
                'inline': False,
                'value': self.dealer.cardsAsString()
        })
        dealerEmbed = discord.Embed.from_dict(dealerEmbedDict)
        if self.dealerEmbedObject == None:
            self.dealerEmbedObject = await self.channel.send(embed=dealerEmbed)
        else:
            if self.dealer.embedShouldUpdate:
                #updateQueue['edit_embed'].append((self.dealerEmbedObject, dealerEmbed))
                await self.dealerEmbedObject.edit(embed=dealerEmbed)
                self.dealer.embedShouldUpdate = False

    async def UpdatePlayerEmbed(self, player):
        playerEmbed = Player.PlayerEmbed(player)
        if player.embedObject == None:
            player.embedObject = await self.channel.send(embed=playerEmbed)
        else:
            if player.embedShouldUpdate:
                #updateQueue['edit_embed'].append((player.embedObject, playerEmbed))
                await player.embedObject.edit(embed=playerEmbed)
                player.embedShouldUpdate = False

    async def UpdateMainEmbed(self):
        mainEmbed = discord.Embed.from_dict(self.mainEmbed)
        if self.mainEmbedObject == None:
            self.mainEmbedObject = await self.channel.send(embed=mainEmbed)
        else:
            if self.mainEmbedShouldUpdate:
                #updateQueue['edit_embed'].append((self.mainEmbedObject, mainEmbed))
                await self.mainEmbedObject.edit(embed=mainEmbed)
                self.mainEmbedShouldUpdate = False

    async def UpdateEmbeds(self):
        await self.UpdateDealerEmbed()

        for player in list(self.players.values()):
            await self.UpdatePlayerEmbed(player)

        # no need to update, since it's done manually
        await self.UpdateMainEmbed()
        return

    async def Update(self):
        global updateQueue
        # when no players have joined
        if self.state > 5:
            self.state = 0

        if self.state == 0:
            self.dealer.showAllCards = False
            if self.lastState != self.state:
                self.resultsShowTimeSet = False
                self.mainEmbedShouldUpdate = True
                self.mainEmbed['title'] = 'Set your bets using the command "bet <amount>". Use command "ready" when you are ready.'
                await discord.Message.clear_reactions(self.mainEmbedObject)
            await self.GetBets()
            if self.allPlayersReady():
                self.NextState()

        if self.state == 1:
            if self.lastState != self.state:
                self.mainEmbedShouldUpdate = True
                self.mainEmbed['title'] = 'Dealing cards...'
                await discord.Message.clear_reactions(self.mainEmbedObject)
            await self.DealCards()
            self.state += 1
            self.lastState += 1

        if self.state == 2:
            if self.lastState != self.state:
                self.mainEmbedShouldUpdate = True
                self.mainEmbed['title'] = 'Use the reactions to do an action'
                self.mainEmbed['description'] = '🟢 to HIT\n🔴 to STAND\n🟡 to SPLIT (Not implemented yet)\n🔵 to DOUBLE (Not implemented yet)'
                
                await discord.Message.add_reaction(self.mainEmbedObject, chr(reaction_hit))
                await discord.Message.add_reaction(self.mainEmbedObject, chr(reaction_stand))
            #updateQueue['add_reaction'].append((self.mainEmbedObject, chr(reaction_hit)))
            #updateQueue['add_reaction'].append((self.mainEmbedObject, chr(reaction_stand)))
            #updateQueue['add_reaction'].append((self.mainEmbedObject, chr(reaction_split)))
            #updateQueue['add_reaction'].append((self.mainEmbedObject, chr(reaction_double)))
            await self.UpdateEmbeds()
            await self.GetActions()
            if self.allPlayersReady():
                self.NextState()

        if self.state == 3:
            if self.lastState != self.state:
                self.mainEmbedShouldUpdate = True
                self.mainEmbed['title'] = 'Dealing cards to the dealer...'
                if 'description' in list(self.mainEmbed.keys()):
                    del self.mainEmbed['description']
                await discord.Message.clear_reactions(self.mainEmbedObject)
            self.dealer.showAllCards = True
            await self.DoDealerActions()
            await self.UpdateDealerEmbed()
            await asyncio.sleep(2)
            self.state += 1

        if self.state == 4:
            if self.lastState != self.state:
                self.mainEmbedShouldUpdate = True
                self.mainEmbed['title'] = 'Preparing results...'
                await discord.Message.clear_reactions(self.mainEmbedObject)
            await self.ShowResults()

            for player in list(self.players.values()):
                player.embedShouldUpdate = True
                await self.UpdatePlayerEmbed(player)
            self.NextState()

        
        if self.state == 5:
            if self.lastState != self.state:
                self.mainEmbedShouldUpdate = True
                self.mainEmbed['title'] = 'Committing results...'
                await discord.Message.clear_reactions(self.mainEmbedObject)
            await self.CommitResults()
            for player in list(self.players.values()):
                player.embedShouldUpdate = True
                await self.UpdatePlayerEmbed(player)
            self.state += 1

        await self.UpdateMainEmbed()
        await self.UpdateEmbeds()
        self.lastState = self.state

    async def GetBets(self):
        for (author, bet) in list(self.addedBets.items()):
            betInt = int(bet)
            player = self.players[author.id]
            print(player)

            del self.addedBets[author]
            if betInt > player.money:
                return False
            else:
                await self.SetBet(player, betInt)
                player.embedShouldUpdate = True
                await self.UpdatePlayerEmbed(player)
                return True

    async def SetPlayerReady(self, author):
        self.players[author.id].isReady = True

    async def DealCards(self):
        self.dealer.embedShouldUpdate = True
        self.dealer.DealCardToSelf()
        self.dealer.DealCardToSelf()
        await self.UpdateDealerEmbed()

        for player in list(self.players.values()):
            player.embedShouldUpdate = True
            player.hands[0].cards.append(self.dealer.DealCard())
            player.hands[0].cards.append(self.dealer.DealCard())
            await self.UpdatePlayerEmbed(player)

    async def GetActions(self):
        for (author, reaction) in list(self.addedReactions.items()):
            r = reaction
            print(author)
            player = self.players[author.id]

            del self.addedReactions[author]
            if r == reaction_hit:
                player.hands[0].cards.append(self.dealer.DealCard())
                if player.hands[0].hasBust():
                    player.isReady = True
                player.embedShouldUpdate = True
                await self.UpdatePlayerEmbed(player)
            elif r == reaction_stand:
                player.isReady = True

        return

    async def DoDealerActions(self):
        dealerCardSum = self.dealer.hand.cardsSum()
        print(dealerCardSum)
        while dealerCardSum < 17:
            print(dealerCardSum)
            self.dealer.hand.cards.append(self.dealer.DealCard())
            dealerCardSum = self.dealer.hand.cardsSum()
        self.dealer.embedShouldUpdate = True
        return

    def GetHandState(self, hand):
        s = hand.cardsSum()
        if hand.hasBlackjack():
            return 0
        elif hand.hasBust():
            return 3
        elif self.dealer.hand.hasBust():
            return 1
        elif self.dealer.hand.cardsSum() == hand.cardsSum():
            return 2
        elif self.dealer.hand.cardsSum() < hand.cardsSum():
            return 1
        else:
            return 3


    async def ShowResults(self):
        for player in list(self.players.values()):
            for hand in player.hands:
                hand.state = self.GetHandState(hand)
            player.embedShouldUpdate = True
        print("game ended, now time for results which are not implemented")
        if not self.resultsShowTimeSet:
            self.resultsShowTime = time.time()
            self.resultsShowTimeSet = True
        self.dealer.embedShouldUpdate = True
        self.mainEmbedShouldUpdate = True

    async def CommitResults(self):
        # delete previous hands
        for player in list(self.players.values()):
            for hand in player.hands:
                player.money += hand.pay()
            player.ClearHands()
        self.dealer.hand = Hand()
