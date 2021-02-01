
# Card suits
# clubs (♣)
# diamonds (♦)
# hearts (♥)
# spades (♠)
class Card():
    # card id that contains all information required
    # to get the suit and the value of the card
    id = int()

    # returns a value between 1 and 13
    def value(self):
        return (self.id % 13) + 1

    def blackjackValue(self):
        return min(self.value(), 10)

    def suit(self):
        return int(self.id / 13)

    def suitAsString(self):
        suit = self.suit()
        if suit == 0:
            return "Clubs"
        elif suit == 1:
            return "Diamonds"
        elif suit == 2:
            return "Hearts"
        elif suit == 3:
            return "Spades"

    def valueAsString(self):
        n = self.value()
        if n == 1:
            return "Ace"
        elif n == 11:
            return "Jack"
        elif n == 12:
            return "Queen"
        elif n == 13:
            return "King"
        else:
            return str(n)