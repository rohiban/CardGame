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
		pass
		
	def rankFunction(self, left, right):
		pass
	
	def bestSuiteCriteria(self):
		pass
		
	def isTrumpApplicable(self):
		pass
		
	def whoStartsNextHand(self):
		pass
		
	def whoDealsNextHand(self):
		pass
		
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
	def __init__(self, card):
		super(GadhaLotanRules, self).__init__()
		self.startCard = card
		
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

class RummyRules(CardGameRules):
	def __init__(self, card):
		super(RummyRules, self).__init__()
		self.startCard = card
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
	
	def printIt(self):
		if isAceMax():
			aceRule = "Max"
		else:
			aceRule = "Min"
				
		print "Starting card is %s" %self.startCard.toString()
		print "Best suite criteria is %s" %bestSuiteCriteria()
		print "Trump applicable = %r, and Ace is considered %s" %(isTrumpApplicable(), aceRule)
		print "Next hand start by : %s, Next hand dealer : %s" %(whoStartsNextHand(), whoDealsNextHand())

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