import random
from CardGameRules import *
from Cards import *

class Game(object):
	def __init__(self, players):
		self.players = players
		self.no_of_players = len(players)
		
	def beginPlay(self):
		pass

class CardGame(Game):
	def __init__(self, players, cardDeck):
		super(CardGame, self).__init__(players)
		self.card_deck = cardDeck
		self.rules = None
		self.unused_cards = None

	def setRules(self, rules):
		self.rules = rules
		
	def getRules(self):
		return self.rules

	def distributeHand(self, noOfCardsToDistribute):
		for i in range(noOfCardsToDistribute):
			for p in self.players:
				p.takeACard(self.card_deck.drawACard())
		return self.card_deck

	def dealCards(self, cardsPerPlayer):
		self.unused_cards = self.distributeHand(cardsPerPlayer)

	def startingPlayerPos(self):
		return 0

	def winningCard(self, rules):
		pass

	def shuffleTheDeck(self):
		self.card_deck.shuffle()

	def initialize(self, cardsPerPlayer):
		self.shuffleTheDeck()
		self.dealCards(cardsPerPlayer)
		#self.dealCards(floor(self.card_deck.cardCount() / len(self.players)))

	def beginPlay(self):
		#initialize(floor(self.card_deck.cardCount() / len(self.players)))
		# decide player's position, who starts the first hand
		# repeat playing hands until all cards are exhausted
		#	each player plays a card
		#	when hand is completed, determine
		#		the winning card, and from it the winning player
		#	the winner player starts the next hand
		#determine points for each player
		#declare the winner of the game
		#
		pass

	def nextPlayerIndex(self, currIndex, delta=1):
		currIndex += delta
		if currIndex > (self.no_of_players-1):
			currIndex -= self.no_of_players
			
		return currIndex

	def playAHand(self, startPos):
		pass

class GadhaLotan(CardGame):
	def __init__(self, players, deck):
		super(GadhaLotan, self).__init__(players, deck)
		self.used_cards = SetOfCards()

	def playersWithCardsInHand(self):
		count = 0
		for p in self.players:
			if p.noOfCardsInHand() != 0:
				count += 1
		return count

	def beginPlay(self):
		rules = self.getRules()
		
		no_of_cards = 13
		self.initialize(no_of_cards)
		
		playedHand = Hand()
		for p in self.players:
			p.printIt()
			p.printYourHand()				

		# person with the Leading card starts
		startPos = self.rules.startingPlayerPos(self.players)

		suite = self.rules.startingCard().getSuite()
		hand = 0
		loading = False
		
		while self.playersWithCardsInHand() != 1:

			for i in range(self.no_of_players):

				p = self.players[startPos]
				if p.noOfCardsInHand() == 0:
					p.printIt(), 
					print " is the winner"
					continue

				if (hand == 0) & (i == 0):
					card = p.playTHECard(self.rules.startingCard())
				else:
					card = p.playACard(suite)

				if card is None:
					card = p.playARandomCard()
					if i != 0: # more than one player has played
						loading = True
						winPos = playedHand.winningCardPos(rules)
					else:
						suite = card.getSuite()

				playedHand.addACard(card)

				if loading:
					loadedPlayerPos = self.nextPlayerIndex(self.nextPlayerIndex(startPos) + (self.no_of_players-1 - i), winPos)
					#print "startpos = %d, winPos = %d, loadedPlayerPos = %d" %(startPos, winPos, loadedPlayerPos)
					break
				else:
					startPos = self.nextPlayerIndex(startPos)

			playedHand.printIt()
			suite = playedHand.getTopCard().getSuite()
			
			if loading:
				self.players[loadedPlayerPos].getCardsInHand().mergeWith(playedHand)
				self.players[loadedPlayerPos].printIt()
				self.players[loadedPlayerPos].printYourHand()
				loading = False
			else :
				winPos = playedHand.winningCardPos(rules)
				self.used_cards.mergeWith(playedHand)
				startPos = self.nextPlayerIndex(startPos, winPos)

			hand += 1
			#if (hand > 25):
			#	break

class Rummy(CardGame):
	def __init__(self, players, deck):
		super(Rummy, self).__init__(players, deck)
		
		self.used_cards = SetOfCards()
		#self.unused_cards = None

	def getTrumpSuite(self):
		return trumpSuite
	
	def beginPlay(self):
		trumpDeclared = False
		rules = self.getRules()

		no_of_cards = 13
		self.initialize(no_of_cards)

		# initialize the hand
		playedHand = Hand()

		for p in self.players:
			p.printIt()
			p.printYourHand()				

		# person with the Leading card starts
		startPos = self.rules.startingPlayerPos(self.players)

		suite = self.rules.startingCard().getSuite()
		for hand in range(no_of_cards):
			# play a new hand
			print "# %d" %(hand+1)

			for i in range(self.no_of_players):
				p = self.players[startPos]

				if (hand == 0) & (i == 0):
					card = p.playTHECard(self.rules.startingCard())
				else:
					card = p.playACard(suite)

				while card is None:
					if not trumpDeclared:
						trumpSuite = self.rules.determineTrump(p.getCardsInHand())
						trumpDeclared = True
						print "Trump is %s" %trumpSuite
						rules.setTrump(trumpSuite)
					card = p.playACard(trumpSuite)
					if card is None:
						card = p.playARandomCard()
				
				playedHand.addACard(card)
				
				startPos = self.nextPlayerIndex(startPos)

			playedHand.printIt()
			
			winPos = playedHand.winningCardPos(rules)
			startPos = self.nextPlayerIndex(startPos, winPos)
			
			suite = playedHand.getTopCard().getSuite()
			self.used_cards.mergeWith(playedHand)
