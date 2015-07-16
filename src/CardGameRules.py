from Cards import Card


class Suites(object):
    SPADE="Spade"
    CLUB="Club"
    DIAMOND="Diamond"
    HEART="Heart"


class BestCriteria(object):
    VALUE="Sum of Value"
    COUNT="Card Count"


class WhoPlaysNext(object):
    SEQUENCE="Sequence of Players"
    WINNER="Previous hand's Winner"


class WhoDealsNext(WhoPlaysNext):
    LOSER="Previous hand's Loser"


class CardDistribution(object):
    ONEATATIME="One card at a time"
    MULTIATATIME="Multiple cards at a time"


class GameRules(object):
    def printIt(self):
        pass


class CardGameRules(GameRules):
    def __init__(self):
        super(CardGameRules, self).__init__()

    def startingSuite(self):
        pass

    def startingCard(self):
        pass

    def isAceMax(self):
        return True

    def rankFunction(self, left, right):
        pass

    def bestSuiteCriteria(self):
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
        return startPos

    def printIt(self):
        pass


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

class RummyRules(CardGameRules):
    def __init__(self, card):
        super(RummyRules, self).__init__()
        self.startCard = None
        self.trumpSuite = ""

    def setTrump(self, suite):
        self.trumpSuite = suite

    def getTrumpSuite(self):
        return self.trumpSuite

    def startingCard(self):
        return self.startCard

    def isAceMax(self):
        return True

    def determineTrump(self, cardSet):
        return self.getTheBestSuite(cardSet)

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

    def bestSuiteCriteria(self):
        return BestCriteria.COUNT

    def getTheBestSuite(self, cards):
        maxVal = 0
        winSuite = ""
        valOfSuites = []

        for suite in [Suites.SPADE, Suites.CLUB, Suites.DIAMOND, Suites.HEART]:
            if self.bestSuiteCriteria() == BestCriteria.COUNT:
                val = cards.noOfCards(suite)
            if self.bestSuiteCriteria() == BestCriteria.VALUE:
                val = cards.sumOfValue(suite)

            valOfSuites.append([suite, val])

            if suite != self.trumpSuite:
                if val > maxVal:
                    winSuite, maxVal = suite, val

        return winSuite

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
        return 13

    def printIt(self):
        if self.isAceMax():
            aceRule = "Max"
        else:
            aceRule = "Min"

        print "Starting card is %s" %self.startCard.toString()
        print "Best suite criteria is %s" %self.bestSuiteCriteria()
        print "Trump applicable = %r, and Ace is considered %s" %(self.isTrumpApplicable(), aceRule)
        print "Next hand start by : %s, Next hand dealer : %s" %(self.whoStartsNextHand(), self.whoDealsNextHand())

#class RuleUser(object):
#	def __init__(self, someRules):
#		self.rules = someRules
#	def doWork(self):
#		print self.rules.startingSuite()

# Main Body

#myRules = RummyRules()
#print myRules.isAceMax()
#print myRules.startingSuite()
#print myRules.isTrumpApplicable()

#user = RuleUser(myRules)
#user.doWork()