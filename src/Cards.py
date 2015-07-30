import random
from __builtin__ import int

__author__ = 'rbansal'


class Suites(object):
    SPADE="Spade"
    CLUB="Club"
    DIAMOND="Diamond"
    HEART="Heart"


class Card(object):
    def __init__(self, suite, value):
        self.value = value
        self.suite = suite

        if value == 1:
            self.label="A"
        elif value == 11:
            self.label="J"
        elif value == 12:
            self.label="Q"
        elif value == 13:
            self.label="K"
        else:
            self.label=str(value)

    def getSuite(self):
        return self.suite

    def getValue(self):
        return self.value

    def isOfSameSuite(self, card):
        return self.suite == card.suite

    def isSame(self, card):
        return (self.value == card.value) & (self.suite == card.suite)

    def isHigher(self, card):
        return (self.suite == card.suite) & (self.value > card.value)

    def isHigherValue(self, card):
        return self.value > card.value

    def isAce(self):
        return self.value == 1

    # def printIt(self):
    #     print "(%s,%s)" %(self.suite, self.label)

    # def toString(self):
    #     return "(" + self.suite + "," + self.label + ")"

    def __cmp__(self, other):
        return int.__cmp__(self.value, other.value)

    def __str__(self):
        return "(" + self.suite + ", " + self.label + ")"

    def __unicode__(self):
        return self.__str__()


class SetOfCards(object):
    def __init__(self, c=None):
        self.cards = c if c else []

    def cardCount(self):
        return len(self.cards)

    def addACard(self, card):
        self.cards.append(card)

    def drawACard(self):
        return self.cards.pop(self.cardCount()-1)

    def drawCards(self, count):
        if count == 1:
            return self.drawACard()
        else:
            return SetOfCards([self.drawACard() for i in range(count)])
            # myCards = []
            # for i in range(count):
            #     myCards.append(self.drawACard())
            # return myCards

    def throwARandomCard(self):
        return self.cards.pop(random.randint(0, self.cardCount()-1))

    def throwACard(self, ofSuite):
        i = 0
        for card in self.cards:
            if card.getSuite() == ofSuite:
                return self.cards.pop(i)
            else:
                i += 1

        return None

    def throwTHECard(self, card):
        # i = 0
        for i, c in enumerate(self.cards):
            if c.isSame(card):
                return self.cards.pop(i)
            # else:
            #     i += 1

    def getMaxCard(self, ofSuite):
        # get all the cards of the suite
        suiteCards = [card for card in self.cards if card.getSuite() == ofSuite]

        # sort them in descending order

        # return the first one
        pass

    def getMinCard(self, ofSuite):
        # get all the cards of the suite
        suiteCards = [card for card in self.cards if card.getSuite() == ofSuite]

        # sort them in ascending order

        # return the first one
        pass

    def shuffle(self):
        no_of_cards = self.cardCount()
        for i in range(no_of_cards):
            card = self.cards.pop(random.randint(0, no_of_cards-1))
            self.cards.insert(random.randint(0,(no_of_cards-1) - 1), card)

    def mergeWith(self, additionalSetOfCards):
        for i in range(additionalSetOfCards.cardCount()):
            self.addACard(additionalSetOfCards.drawACard())

    def hasCard(self, card):
        return any(filter(lambda c: c.isSame(card), self.cards))
        # if len(self.cards) > 0:
        #     for c in self.cards:
        #         if c.isSame(card):
        #             return True
        # return False

    def noOfCards(self, ofSuite):
        return len([card for card in self.cards if card.getSuite() == ofSuite])
        # count = 0
        # for card in self.cards:
        #     if card.getSuite() == ofSuite:
        #         count += 1
        # return count

    def sumOfValue(self, ofSuite):
        return sum([card.getValue() for card in self.cards if card.getSuite() == ofSuite])
        # val = 0
        # for card in self.cards:
        #     if card.getSuite() == ofSuite:
        #         val += card.getValue()
        # return val

    def bestSuite(self, rules):
        pass

    # def toString(self):
    #     s = ""
    #     for card in self.cards:
    #         s += card.toString()
    #     return s

    # def printIt(self):
    #     print self.toString()

    def __str__(self):
        s = ""
        for card in self.cards:
            s += "%s" %card
        return s

    def __unicode__(self):
        return self.__str__()


class Hand(SetOfCards):
    def __init__(self, c=None):
        super(Hand, self).__init__(c)

    # def leadingSuite(self):
    #     return self.cards[0].getSuite()

#	def winningCard(self, rules):
#		winner = self.cards[0]
#		
#		i = 0
#		for card in self.cards:
#			if i > 0:
#				if rules.isHigher(card, winner):
#					winner = card
#			i += 1
#		return winner

    # def winningCardPos(self, rules):
    #     i = 0
    #     winPos = 0
    #     for card in self.cards:
    #         if i == 0:
    #             winner, winPos = card, i
    #         else:
    #             if rules.rankFunction(card, winner):
    #                 winner, winPos = card, i
    #         i += 1
    #     return winPos

    # def getBottomCard(self):
    #     return self.cards[0]
    #
    # def getTopCard(self):
    #     return self.cards[self.cardCount()-1]


class FullDeck(SetOfCards):
    def __init__(self):
        # self.no_of_cards = 52
        # super(FullDeck, self).__init__()
        # for suite in [Suites.SPADE, Suites.CLUB, Suites.DIAMOND, Suites.HEART]:
        #     for value in range(13):
        #         super(FullDeck, self).addACard(Card(suite, value+1))
        deck = [Card(suite, value)
                      for suite in [Suites.SPADE, Suites.CLUB,
                                    Suites.DIAMOND, Suites.HEART]
                      for value in range(1,14)]
        super(FullDeck, self).__init__(deck)
