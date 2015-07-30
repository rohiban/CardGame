from Cards import Card, Suites

__author__ = 'rbansal'


class BestCriteria(object):
    VALUE = "Sum of Value"
    COUNT = "Card Count"


class WhoPlaysNext(object):
    SEQUENCE = "Sequence of Players"
    WINNER = "Previous hand's Winner"


class WhoDealsNext(WhoPlaysNext):
    LOSER = "Previous hand's Loser"


class CardDistribution(object):
    ONEATATIME = "One card at a time"
    MULTIATATIME = "Multiple cards at a time"


class GameRules(object):
    def __init__(self):
        pass

    # def printIt(self):
    #     pass


class CardGameRules(GameRules):
    def __init__(self):
        super(CardGameRules, self).__init__()
        self.criterion = None

    def startingSuite(self):
        pass

    def startingCard(self):
        pass

    def isAceMax(self):
        return True

    def rankFunction(self, left, right):
        pass

    def setBestSuiteCriteria(self, c):
        self.criterion = c

    def bestSuite(self, cards):
        pass

    def isTrumpApplicable(self):
        return False

    def whoStartsNextHand(self):
        pass

    def whoDealsNextHand(self):
        pass

    def noOfCardsToDealToAPlayer(self):
        return 1

    def maxCountAfterDealing(self):
        return 0

    def determineWinningCard(self, hand):
        pass

    def startingPlayerPos(self, allPlayers):
        startPos = 0
        for p in allPlayers:
            if p.hasCard(self.startingCard()):
                return startPos
            else:
                startPos += 1
        return -1

    # def printIt(self):
    #     pass


class GadhaLotanRules(CardGameRules):
    def __init__(self):
        super(GadhaLotanRules, self).__init__()
        self.startCard = Card(Suites.SPADE, 1)

    def startingCard(self):
        return self.startCard

    def isAceMax(self):
        return True

    def isTrumpApplicable(self):
        return False

    def whoStartsNextHand(self):
        return WhoPlaysNext.WINNER

    def rankFunction(self, left, right):
        if left.isSame(right):
            return False

        if left.isOfSameSuite(right):
            if self.isAceMax():
                if left.isAce():
                    return True
                if right.isAce():
                    return False

            return left.isHigher(right)
        else:
            return False

    def maxCountAfterDealing(self):
        return 13

    def bestSuite(self, cards):
        if self.criterion == BestCriteria.COUNT:
            suiteList = [(cards.noOfCards(suite), suite)
                          for suite in [Suites.SPADE, Suites.CLUB,
                                        Suites.DIAMOND, Suites.HEART]]
        elif self.criterion == BestCriteria.VALUE:
            suiteList = [(cards.sumOfValue(suite), suite)
                          for suite in [Suites.SPADE, Suites.CLUB,
                                        Suites.DIAMOND, Suites.HEART]]
        else:
            return None

        for x, suite in sorted(suiteList, reverse=True):
            return suite

        # winSuite = Suites.SPADE
        # winCount = cards.noOfCards(winSuite)
        # for s in [Suites.CLUB, Suites.DIAMOND, Suites.HEART]:
        #     count = cards.noOfCards(s)
        #     if winCount < count:
        #         winCount = count
        #         winSuite = s
        # return winSuite


class RummyRules(CardGameRules):
    def __init__(self):
        super(RummyRules, self).__init__()
        # self.startCard = None
        self.trumpSuite = None

    def setTrump(self, suite):
        self.trumpSuite = suite

    def getTrumpSuite(self):
        return self.trumpSuite

    def startingCard(self):
        return None

    def isAceMax(self):
        return True

    def determineTrump(self, cardSet):
        return self.bestSuite(cardSet)

    def rankFunction(self, left, right):
        if left.isOfSameSuite(right):
            if self.isAceMax():
                if left.isAce():
                    return True
                if right.isAce():
                    return False

            return left.isHigher(right)
        else:
            if self.isTrumpApplicable():
                if left.getSuite() == self.trumpSuite:
                    return True
                if right.getSuite() == self.trumpSuite:
                    return False
            return left.isHigherValue(right)

    def bestSuite(self, cards):
        if self.criterion == BestCriteria.COUNT:
            suiteList = [(cards.noOfCards(suite), suite)
                         for suite in [Suites.SPADE, Suites.CLUB,
                                       Suites.DIAMOND, Suites.HEART] if suite != self.trumpSuite]
        elif self.criterion == BestCriteria.VALUE:
            suiteList = [(cards.sumOfValue(suite), suite)
                         for suite in [Suites.SPADE, Suites.CLUB,
                                       Suites.DIAMOND, Suites.HEART] if suite != self.trumpSuite]
        else:
            return None

        for x, suite in sorted(suiteList, reverse=True):
            return suite if x else self.trumpSuite
            # if x == 0:  # if only trump cards are left in hand
            #     return self.trumpSuite
            # else:
            #     return suite

            # maxVal = 0
        # winSuite = ""
        # valOfSuites = []
        #
        # for suite in [Suites.SPADE, Suites.CLUB, Suites.DIAMOND, Suites.HEART]:
        #     if self.criterion == BestCriteria.COUNT:
        #         val = cards.noOfCards(suite)
        #     if self.criterion == BestCriteria.VALUE:
        #         val = cards.sumOfValue(suite)
        #
        #     valOfSuites.append([suite, val])
        #
        #     if suite != self.trumpSuite:
        #         if val > maxVal:
        #             winSuite, maxVal = suite, val
        #
        # return winSuite

#	def startingPlayerPos(self, allPlayers):
#		startPos = 0
#		for p in allPlayers:
#			if p.hasCard(self.startCard):
#				return startPos
#			else:
#				startPos += 1
#		return startPos

    def isTrumpApplicable(self):
        return True

    def whoStartsNextHand(self):
        return WhoPlaysNext.WINNER

    def whoDealsNextHand(self):
        return WhoDealsNext.WINNER

    def noOfCardsToDealToAPlayer(self):
        return 4

    def maxCountAfterDealing(self):
        return 12

    # def printIt(self):
    #     if self.isAceMax():
    #         aceRule = "Max"
    #     else:
    #         aceRule = "Min"
    #
    #     print "Best suite criteria is %s" % self.criterion
    #     print "Trump applicable = %r, and Ace is considered %s" %(self.isTrumpApplicable(), aceRule)
    #     print "Next hand start by : %s, Next hand dealer : %s" %(self.whoStartsNextHand(), self.whoDealsNextHand())
