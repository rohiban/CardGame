from Cards import *

class Player(object):
	def __init__(self, name):
		self.name = name

	def printIt(self):
		print "%s" %self.name

class CardPlayer(Player):
	def __init__(self, name):
		super(CardPlayer, self).__init__(name)
		self.cards = SetOfCards()
		
	def getCardsInHand(self):
		return self.cards
	
	def takeACard(self, card):
		self.cards.addACard(card)
		
	def playTHECard (self, card):
		return self.cards.throwTHECard(card)
		
	def getBestSuite(self, rules):
		return self.cards.bestSuite(rules)

	def playACard(self, ofSuite):
		return self.cards.throwACard(ofSuite)
		
	def playARandomCard(self):
		return self.cards.throwARandomCard()
	
	def hasCard(self, card):
		return self.cards.hasCard(card)
		
	def printYourHand(self):
		print self.cards.toString()
		
	def noOfCardsInHand(self):
		return self.cards.cardCount()
