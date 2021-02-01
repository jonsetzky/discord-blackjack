
from .hand import Hand
from .card import Card

import random

class Dealer():

    def __init__(self):
        self.stack = list()
        self.hand = Hand()

        self.embedShouldUpdate = True

        self.showAllCards = False

    def cardsAsString(self):
        outstr = ""
        for card in self.hand.cards:
            outstr += card.valueAsString() + ' '
            if not self.showAllCards:
                break
        if outstr == "":
            outstr = "HAND EMPTY"
        return outstr.strip(' ')

    def canInsurance(self):
        return

    def cardsLeft(self):
        return sum(self.stack)

    def DealCard(self):
        hasFound = False
        card = Card()
        while not hasFound:
            rn = random.randint(1, 52)
            if self.stack[rn] > 0:
                self.stack[rn] -= 1
                hasFound = True
                self.cardsLeft -= 1
                card.id = rn
        return card

    def DealCardToSelf(self):
        self.hand.cards.append(self.DealCard())
        
    def Shuffle(self, numStacks):
        self.cardsLeft = 52 * numStacks
        self.stack = [0]*53
        for i in range(0, 53):
            self.stack[i] = numStacks