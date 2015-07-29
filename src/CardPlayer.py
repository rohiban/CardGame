from Cards import SetOfCards

__author__ = 'rbansal'


class Player(object):
    def __init__(self, name):
        self.name = name

    def printIt(self):
        print "%s" % self.name

    def isSame(self, p):
        return self.name == p.name


class CardPlayer(Player):
    def __init__(self, name):
        super(CardPlayer, self).__init__(name)
        self.cards = SetOfCards()

    def getCardsInHand(self):
        return self.cards

    def takeACard(self, card):
        self.cards.addACard(card)

    def takeCards(self, cards):
        self.cards.mergeWith(cards)

    def playTHECard (self, card):
        return self.cards.throwTHECard(card)

    def selectASuite(self, rules):
        return rules.bestSuite(self.cards)

    def playACard(self, ofSuite):
        return self.cards.throwACard(ofSuite)

    def playARandomCard(self):
        return self.cards.throwARandomCard()

    def hasCard(self, card):
        return self.cards.hasCard(card)

    def hasCardOfSuite(self, ofSuite):
        return self.cards.noOfCards(ofSuite) > 0

    def printYourHand(self):
        print self.cards.toString()

    def noOfCardsInHand(self):
        return self.cards.cardCount()