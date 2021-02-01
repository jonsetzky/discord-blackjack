

from .card import Card

class Hand():
    

    # the bet
    bet = 0

    def __init__(self):
        self.cards = list()

        # <0 not resolved
        #  0 blackjack
        #  1 win
        #  2 draw
        #>=3 lose
        self.state = -1

    def pay(self):
        s = self.state
        if s == 0:
            return self.bet * 3/2 + self.bet
        elif s == 1:
            return self.bet + self.bet
        elif s == 2:
            return self.bet
        else: 
            return 0

    def asString(self):
        outstr = ""
        
        if self.state >= 0:
            s = self.state
            if s == 0:
                return '**Blackjack**'
            elif s == 1:
                return 'Win'
            elif s == 2:
                return 'Draw'
            else: 
                return 'Lose'

        for card in self.cards:
            outstr += card.valueAsString() + ' '
        outstr = outstr.strip(' ') + f', which is total **{self.cardsSum()}**'
        if self.cardsSum() > 21:
            outstr += " that is a BUST"
        if outstr == "":
            outstr = "HAND EMPTY"
        return outstr

    def cardsSum(self):
        numAces = 0
        s = 0
        for c in self.cards:
            value = c.value()
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

    def hasBust(self):
        return self.cardsSum() > 21

    def hasBlackjack(self):
        return self.cardsSum == 21 and len(self.cards) < 3
