import random
import asyncio
import discord

class BlackjackCard():
    id = int()

    # returns a value between 1 and 13
    def getValue(self):
        return (self.id % 13) + 1

    def valueAsString(self):
        n = self.getValue()
        if n == 1:
            return "ACE"
        elif n == 11:
            return "JACK"
        elif n == 12:
            return "QUEEN"
        elif n == 13:
            return "KING"
        else:
            return str(n)

    def asFullString(self):
        return "A " + self.valueAsString() + " of " + self.suitAsString()

    def suitAsInt(self):
        return int(self.id / 13)

    def suitAsString(self):
        n = self.suitAsInt()
        if n == 3: return "Clubs"
        elif n == 2: return "Diamonds"
        elif n == 1: return "Hearts"
        elif n == 0: return "Spades"
        else: raise RuntimeError("Invalid suit for a card")

class BlackjackHand():
    cards           = None
    hasBlackjack    = False
    hasInsurance    = False
    bet             = 0

    def __init__(self):
        self.cards = []

    def AddCard(self, id):
        newCard = BlackjackCard()
        newCard.id = id
        self.cards.append(newCard)

    def cardValues(self):
        outl = []
        for c in self.cards:
            outl.append(c.getValue())
        return outl

    def cardsAsString(self):
        outl = ""
        for c in self.cards:
            outl += c.valueAsString() + ", "
        return outl.strip(' ').strip(',')

    def cardSum(self):
        numAces = 0
        s = 0
        for c in self.cards:
            value = c.getValue()
            if value == 1:
                numAces += 1
            elif value == 11:
                s += 10
            elif value == 12:
                s += 10
            elif value == 13:
                s += 10
            else:
                s += value

        i = 0
        while i < numAces:
            ps = s + 11
            if ps > 21:
                s += 1
                i += 1
            else:
                s += 11
                i += 1
        return s

    def canSplit(self):
        return (len(cards) < 3 and len(cards) > 1) and cards[0].getValue() == cards[1].getValue()

    def canDouble(self):
        return len(cards) < 3

    def hasBlackjack(self):
        return (len(cards) < 3) and (cardSum() == 21)

class BlackjackPlayer():
    author = 0
    name = ""
    money = 0
    roundBet = 0 # divided among hands (if multiple) equally
    hands = list()
            

    def __init__(self):
        self.hands = list()

    @staticmethod
    def CreatePlayer(name):
        p = BlackjackPlayer()
        p.money = 50
        p.name = name
        return p
        

# Card suits
# clubs (♣)
# diamonds (♦)
# hearts (♥)
# spades (♠)
class CardDealer():
    stack = list()
    cardsLeft = 0

    def DealCard(self):
        hasFound = False
        while not hasFound:
            rn = random.randint(1, 52)
            if self.stack[rn] > 0:
                self.stack[rn] -= 1
                hasFound = True
                self.cardsLeft -= 1
                return rn
        
    def ResetStacks(self, numStacks):
        self.cardsLeft = 52 * numStacks
        self.stack = [0]*53
        for i in range(0, 53):
            self.stack[i] = numStacks

            
def ValidateInput(cmdSplit, requiredArgs, fallbackMessage):
    if len(cmdSplit) - 1 < requiredArgs:
        cmdArg = input(fallbackMessage)
        return cmdArg
    else:
        return cmdSplit[1]
        

balanceCommands = ['balance', 'money']
unbetCommands = ['unbet', 'remove']
betCommands = ['setbet', 'bet']
continueCommands = ['continue', 'run', 'next', 'nextround']
class BlackJack():
    def __init__(self):
        self.cardDealer = CardDealer()
        self.cardDealer.ResetStacks(4)

    def CanInsurance(self, player):
        s = self.dealer.cardSum()
        if s < 21 and s > 19:
            return True
        else:
            return False

    def CanSplit(self, player):
        l = len(player.cardValues())
        v1 = CardDealer.GetCardNumberFromID(player.cardValues()[0])
        v1 = max(min(v1, 10), 1)
        v2 = CardDealer.GetCardNumberFromID(player.cardValues()[1])
        v2 = max(min(v2, 10), 1)
        if l < 3:
            if v1 == v2:
                if player.money >= player.bet:
                    return True
        return False

    def CanDouble(self, player):
        if len(player.cardValues()) < 3:
            return True
        return False

    def HasBlackJack(self, player):
        l = len(player.cardValues())
        s = player.cardSum()
        if l < 3 and s > 20:
            return True
        else:
            return False

    def HasBusted(self, player):
        if player.cardSum() > 21:
            return True

    def DealerSum(self):
        return self.dealer.cardSum()

    def IsPlayerWinner(self, player):
        playerBust = self.HasBusted(player)
        dealerBust = self.HasBusted(self.dealer)
        playerSum = player.cardSum()
        dealerSum = self.DealerSum()
        if playerBust:
            return False
        if dealerBust:
            return True
        if playerSum < dealerSum:
            return False
        if playerSum > dealerSum:
            return True
        if playerSum == dealerSum:
            return False
        raise ValueError("Find out the reason IsPlayerWinner() wen to the end of the if-tree")

    def IsPlayerDraw(self, player):
        playerBust = self.HasBusted(player)
        if playerBust:
            return False
        if player.cardSum() == self.DealerSum():
            return True

    gameStarted = False
    def StartGame(self):
        self.cardDealer.ResetStacks(4)
        self.gameStarted = True

    def RunRound(self):
        self.dealer.cards = []
        
        for i in range(0, 2):
            self.dealer.cards.append(self.cardDealer.DealCard())

        if not self.gameStarted:
            raise RuntimeError("Game has not been started")
            return
        for player in self.players:
            hasInsurance = False
            player.cards = []
            for i in range(0, 2):
                self.HitForPlayer(player)
                
            roundReady = False
            while not roundReady:
                print(f"Your cards are {player.cardStrings()}, sum is {player.cardSum()}")
                print("h for Hit"           * (not self.HasBlackJack(player)) +
                      ", st for Stand"      * (not self.HasBlackJack(player)) +
                      ", sp for Split"      * (not self.HasBlackJack(player)) * self.CanSplit(player)   +
                      ", d for Double"      * (not self.HasBlackJack(player)) * self.CanDouble(player)  +
                      ", i for Insurance"   * (not self.HasBlackJack(player)) * self.CanInsurance(player))
                if not self.HasBlackJack(player):
                    inp = input("")
                    if inp == 'h':# ['h', 's', 'd', 'i']:
                        self.HitForPlayer(player)
                        if self.HasBusted(player):
                            roundReady = True
                    elif inp == 'st':
                        roundReady = True
                    elif inp == 'sp':
                        print('This feature is yet to be added')
                    elif inp == 'd':
                        self.DoubleForPlayer(player)
                        roundReady = True
                    elif inp == 'i':
                        self.InsuranceForPlayer(player)
                else: # if player has blackjack
                    player.hasBlackjack = True
                    roundReady = True
            input("Press ENTER to continue")

        dealerReady = False
        while not dealerReady:
            dealerSum = self.DealerSum()
            if dealerSum > 17:
                dealerReady = True
            dealtCard =self.cardDealer.DealCard()
            dealtCardString = CardDealer.GetCardNumberStringFromID(dealtCard)
            dealtCardSuitString = CardDealer.GetCardSuitStringFromID(dealtCard)
            self.dealer.cards.append(self.cardDealer.DealCard())
            dealerSum = self.DealerSum()
            print(f"Dealer got a {dealtCardString} of {dealtCardSuitString}, which is total of {dealerSum}")


        # compare the hands
        for player in self.players:
            isPlayerWinner = self.IsPlayerWinner(player)
            isPlayerDraw = self.IsPlayerDraw(player)
            isPlayerBlackjack = self.HasBlackJack(player)
            if isPlayerBlackjack:
                self.WinForPlayer(player)
            elif isPlayerWinner:
                self.WinForPlayer(player)
            elif isPlayerDraw:
                self.DrawForPlayer(player)
            else:
                self.LoseForPlayer(player)
                
    def AddPlayer(self, player):
        self.players.append(player)

    def HitForPlayer(self, player):
        cardID = self.cardDealer.DealCard()
        player.cards.append(cardID)
        cardNumberString = CardDealer.GetCardNumberStringFromID(cardID)
        cardSuitString = CardDealer.GetCardSuitStringFromID(cardID)
        print(f"You got dealt a {cardNumberString} of {cardSuitString}, which makes it a total of {player.cardSum()}!")

    def SplitForPlayer(self, player):
        canSplit = self.CanSplit(player)
        if canSplit:
            player.money -= player.bet
            player.bet *= 2
        return

    def DoubleForPlayer(self, player):
        canDouble = self.CanDouble(player)
        if canDouble:
            player.money -= player.bet
            player.bet *= 2
            self.HitForPlayer(player)
        return

    def SetInsuranceForPlayer(self, player):
        return

    def LoseForPlayer(self, player):
        print("You lost the bet")
        bet = player.bet
        player.bet = 0
        if player.hasInsurance:
            player.money += bet / 2
            player.hasInsurance = False
        return

    def DrawForPlayer(self, player):
        return

    def WinForPlayer(self, player):
        print("You won the bet!")
        bet = player.bet
        if player.hasBlackjack:
            bet = bet * 5/4
            player.hasBlackjack = False
        player.money = player.money + (2 * bet)
        player.bet = 0
        

    def SetBetForPlayer(self, player, amount):   
        if int(amount) == player.money:
            print("Betting all-in")
        elif int(amount) > player.money:
            print("Cannot bet more than your balance")
            return False
        print("Setting a bet of " + str(amount))
        player.bet = int(amount)
        player.money -= int(amount)
        return True

    def UnbetForPlayer(self, player):
        if player.bet <= 0:
            return 0
        amountUnbet = player.bet
        player.money += player.bet
        player.bet = 0
        return amountUnbet


class CLIBlackJack(BlackJack):

    def __init__(self):
        pl = BlackjackPlayer.CreateDefaultPlayer()
        self.AddPlayer(pl)

    def ValidateInput(self, cmdSplit, requiredArgs, fallbackMessage):
        if len(cmdSplit) - 1 < requiredArgs:
            cmdArg = input(fallbackMessage)
            return cmdArg
        else:
            return cmdSplit[1]



    def RunCommand(self, playerID, cmd):
        global betCommands, unbetCommands, balanceCommands, continueCommands
        cmdSplit = cmd.split(' ')
        player = self.players[playerID]
        if cmdSplit[0] in betCommands:
            betAmount = self.ValidateInput(cmdSplit, 1, "Amount to bet >>> ")
            try:
                betAmount = int(betAmount)
            except ValueError:
                allinPrompts = ['all', 'allin', 'all-in']
                if betAmount in allinPrompts:
                    betAmont = player.money
                else:
                    print("Please input a valid amount")
                    return True
            self.SetBetForPlayer(player, betAmount)
            return True
        elif cmdSplit[0] == 'quit':
            return -1
        elif cmdSplit[0] in balanceCommands:
            print(f"Your balance is: {self.players[playerID].money}")
            return True
        elif cmdSplit[0] in unbetCommands:
            unbetAmount = self.UnbetForPlayer(player)
            if unbetAmount <= 0:
                print(f"You haven't put a bet")
                return True
            print(f"Your bet of {unbetAmount} has been removed")
        elif cmdSplit[0] in continueCommands:
            print(f"Continuing game")
            self.RunRound()
        else:
            return False

    def GetInput(self):
        cmdIsValid = False
        while not cmdIsValid:
            cmd = input("CLI Blackjack >>> ")
            cmdIsValid = self.RunCommand(0, cmd)
            if cmdIsValid == -1:
                return True
        return False
    

class MultiplayerBlackjack():
    channel = None
    hostAuthor = None

    statusEmbed = None
    statusMessageObject = None

    addedBets = dict()

    cardDealer = CardDealer()

    players = list()
    dealerHand = BlackjackHand()

    numStacks = 1

    gamePlaying = False

    def __init__(self, channel, hostAuthor):
        self.channel = channel
        self.hostAuthor = hostAuthor

        self.cardDealer = CardDealer()
        self.cardDealer.ResetStacks(self.numStacks)
        self.addedReactions = dict()
        
        self.statusEmbed = {
            'title': f' Welcame to the blackest of Jacks! Write "join" to join the game and "start" to start the game!',
            'color': 16711680
        }

    async def PrintMessage(self, msg, removeAfterSeconds):
        await self.channel.send(content=msg, delete_after=removeAfterSeconds)

    async def UpdateStatusMessage(self):
        if self.statusMessageObject == None:
            self.statusMessageObject = await self.channel.send(embed=self.statusEmbed)
        else:
            await self.statusMessageObject.edit(embed=self.statusEmbed)

    def AddPlayer(self, author):
        hasJoinedAlready = False
        for player in self.players:
            hasJoinedAlready = player.author == author
            if hasJoinedAlready:
                return f"You {author} have already joined"
        player = BlackjackPlayer.CreatePlayer(author)
        player.author = author
        self.players.append(player)
        return f"Player {author} joined the blackjack game."

    def StartGame(self):
        numPlayers = len(self.players)
        if numPlayers < 1:
            return f"Cannot start a game with no players"

        self.cardDealer.ResetStacks(self.numStacks)
        
        self.gamePlaying = True

        self.statusEmbed = {
            'title': f'Starting game with {numPlayers} players! Write "continue" to start the round',
            'color': 16711680
        }

    def StartRound(self):
        if not self.gamePlaying:
            raise RuntimeError("Game is not running, cannot start a round")

        # deal starting cards to everyone

        # calculate the required amount of cards for the round
        maxCardsPerHand = 7 # 7 cards win instantly
        maxHandsPerPlayer = 4
        numPlayers = len(self.players)
        maxNumHands = numPlayers * 4 + 1 # 1 is for the dealer
        maxNumCards = maxCardsPerHand * maxNumHands

        dealerCardsLeft = self.cardDealer.cardsLeft

        # ask bets

        # to dealer
        dealerHand = BlackjackHand()
        for i in range(0, 2):
            self.DealCardToHand(dealerHand)

        # to players
        for player in self.players:
            player.hands = list()
            hand = BlackjackHand()
            hand.bet = 10
            player.hands.append(hand)
            for hand in player.hands:
                self.DealCardToHand(hand)


    reaction_no = 10060
    reaction_yes = 9989
    reaction_hit = 128994
    reaction_stand = 128308
    reaction_double = 0
    reaction_split = 128993
    reaction_insurance = 0
    def AddUserReaction(self, author, reaction):
        self.addedReactions[str(author.id)] = int(reaction)

    def AddUserBet(self, author, amount):
        self.addedBets[author] = amount

    # GAME STATES
    # 0 - asking bets
    # 1 - dealing cards
    # 2 - going through everyones actions
    # 3 - results
    gameState = 0 
    async def RunRound(self):
        
        if self.gameState == 0:
            await self.AskBets()

            #self.statusEmbed.title = 'Write "bet <amount>" to set your bet. "continue" to continue.\n'

            fields = list()
            for player in self.players:
                field = {
                    'name': player.author.name,
                    'inline': True,
                    'value': '$0'
                }
                for hand in player.hands:
                    field['value'] = f"${hand.bet}"
                fields.append(field)

            self.statusEmbed = {
                'title': 'Write "bet <amount>" to set your bet. "continue" to continue.\n',
                'color': 16711680,
                'fields': fields
            }
            self.statusEmbed = discord.Embed.from_dict(self.statusEmbed)

        elif self.gameState == 1:
            await self.DealStartingCards()
            self.gameState += 1

            fields = list()
            for player in self.players:
                playerMessage = f"{player.author.name}: "
                field = {
                    'name': player.author.name + " was dealt:",
                    'inline': True,
                    'value': 'None'
                }
                for hand in player.hands:
                    field['value'] = f"{hand.cardsAsString()}, which makes a total of **{hand.cardSum()}**."
                fields.append(field)

            self.statusEmbed = {
                'title': 'Cards dealt:',
                'description': '🟢 – HIT\n🔴 – STAND',
                'color': 16711680,
                'fields': fields
            }
            self.statusEmbed = discord.Embed.from_dict(self.statusEmbed)

        elif self.gameState == 2:
            await self.GetUserActions()
            await self.statusMessageObject.add_reaction(chr(self.reaction_hit))
            await self.statusMessageObject.add_reaction(chr(self.reaction_stand))

            
        await self.UpdateStatusMessage()

    def ContinueRound(self):
        self.gameState += 1
        return 1


    async def AskBets(self):
        for player in self.players:
            setBet = 0
            hasAdded = False
            #for author in list(self.addedBets.keys()):
            #    hasAdded = player.author.id == author.id
            if player.author in list(self.addedBets.keys()):
                betAmount = float(self.addedBets[player.author])
                del self.addedBets[player.author]
                playerBalance = player.money
                if playerBalance >= betAmount:
                    player.roundBet = betAmount
                    player.money -= betAmount
                    startingHand = BlackjackHand()
                    # maybe later add support for multiple hands per round
                    startingHand.bet = player.roundBet
                    player.hands = list()
                    player.hands.append(startingHand)
                    player.roundBet = 0
                    #await self.PrintMessage(f"@{player.author.name}, bet of {startingHand.bet} has been set", 1)
                #else:
                    #self.PrintMessage(f"@{player.author.name}, insufficient balance", 1)

    async def DealStartingCards(self):
        for player in self.players:
            for hand in player.hands:
                dealtCard = self.cardDealer.DealCard()
                dealtCardTwo = self.cardDealer.DealCard()
                hand.AddCard(dealtCard)
                hand.AddCard(dealtCardTwo)
        dealtDealerCard = self.cardDealer.DealCard()
        dealtDealerCardTwo = self.cardDealer.DealCard()
        self.dealerHand = BlackjackHand()
        self.dealerHand.AddCard(dealtDealerCard)
        self.dealerHand.AddCard(dealtDealerCardTwo)

    async def GetUserActions(self):
        for player in self.players:
            if str(player.author.id) in list(self.addedReactions.keys()):
                reaction = int(self.addedReactions[str(player.author.id)])
                del self.addedReactions[str(player.author.id)]
                if (reaction == self.reaction_hit):
                    await self.PrintMessage("You want to hit", 3)
                    return
                elif (reaction == self.reaction_stand):
                    await self.PrintMessage("You want to stand", 3)
                    return

    def DealCardToHand(self, hand):
        dealtCard = self.cardDealer.DealCard()
        c = self.cardDealer.DealCard()
        hand.AddCard(c)

if __name__ == "__main__":
    clbj = CLIBlackJack()
    clbj.StartGame()
    shouldQuit = False
    while not shouldQuit:
        shouldQuit = clbj.GetInput()
    
