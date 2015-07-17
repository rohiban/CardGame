#import random
from CardGameRules import GadhaLotanRules
from Cards import Card, SetOfCards, Hand

__author__ = 'rbansal'


class Game(object):
    def __init__(self, players):
        self.players = players
        self.no_of_players = len(players)

    def beginPlay(self):
        return NotImplemented

    def setRules(self, rules):
        self.rules = rules

    def getRules(self):
        return self.rules


class CardGame(Game):
    def __init__(self, players, cardDeck, rules):
        super(CardGame, self).__init__(players)
        self.card_deck = cardDeck
        self.rules = rules
        self.unused_cards = None

    # simple getter, do we need it ?
    def getRules(self):
        return self.rules

    # find player with a given card
    def playerWithCard(self, card):
        for p in self.players:
            if p.hasCard(card):
                return p
        return None

    def distributeHand(self, noOfCardsToDistribute):
        cardsInOneChunk = self.rules.noOfCardsToDealToAPlayer()
        for i in range(noOfCardsToDistribute):
            for p in self.players:
                if cardsInOneChunk == 1:
                    p.takeACard(self.card_deck.drawACard())
                else:
                    p.takeCards(self.card_deck.drawCards(cardsInOneChunk))
        return self.card_deck

    def dealCards(self, cardsPerPlayer):
        self.unused_cards = self.distributeHand(cardsPerPlayer)

    def startingPlayerPos(self):
        return 0

    def winningCard(self, rules):
        return NotImplemented

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
        return NotImplemented

    def nextPlayerIndex(self, currIndex, delta=1):
        currIndex += delta
        if currIndex > (self.no_of_players-1):
            currIndex -= self.no_of_players
        return currIndex

    def playAHand(self, startPos):
        return NotImplemented


class GadhaLotan(CardGame):
    def __init__(self, players, deck, rules):
        super(GadhaLotan, self).__init__(players, deck, rules)
        self.used_cards = SetOfCards()

    def playersWithCardsInHand(self):
        count = 0
        for p in self.players:
            if p.noOfCardsInHand() != 0:
                count += 1
        return count

    def beginPlay(self):
        no_of_cards = self.rules.maxCountAfterDealing()
        self.initialize(no_of_cards)

        # initialize the played hand variable
        playedHand = Hand()

        # print the hands of all players (for debugging)
        for p in self.players:
            p.printIt()
            p.printYourHand()

        # person with the leading card starts
        startPos = self.rules.startingPlayerPos(self.players)

        # which player has Ace of Spade [starting card]
        # p = self.playerWithCard(self.rules.startingCard())

        suite = None
        hand = 0
        loading = False

        # continue as long as there is more than one player, holding cards in hand
        while self.playersWithCardsInHand() > 1:

            # iterate over all players
            for i in range(self.no_of_players):

                # get the player
                p = self.players[startPos]

                # if a player has finished the cards, declare it
                if p.noOfCardsInHand() == 0:
                    # for debugging
                    print "Winner is ... ",
                    p.printIt()

                    # shift to next player
                    startPos = self.nextPlayerIndex(startPos)

                    continue

                if hand == 0:  # first hand, suite can't change
                    if suite is None:  # first player plays the starting card
                        card = p.playTHECard(self.rules.startingCard())
                        suite = card.getSuite()
                    else:  # second player onwards
                        if p.hasCardOfSuite(suite):
                            card = p.playACard(suite)
                        else:  # no loading can happen on first hand
                            card = p.playARandomCard()
                else:  # suite can be decided
                    if suite is None:  # suite is not decided for the hand
                        suite = p.selectASuite(self.rules)
                        card = p.playACard(suite)
                    else:  # suite is already decided for the hand
                        if p.hasCardOfSuite(suite):
                            card = p.playACard(suite)
                        else:  # loading happens
                            loading = True
                            winPos = playedHand.winningCardPos(self.rules)

                            # let the player select a new suite
                            card = p.playACard(p.selectASuite(self.rules))
                            suite = card.getSuite()

                # if (hand == 0) & (i == 0):  # first hand and first player
                #     card = p.playTHECard(self.rules.startingCard())
                #     suite = card.getSuite()
                # else:
                #     # check if the player has this suite's card
                #     if p.hasCardOfSuite(suite):
                #         card = p.playACard(suite)
                #     else:
                #         # if this is first hand, then player can throw a random card
                #         if hand == 0:
                #             card = p.playARandomCard()
                #         else:
                #             # loading happens
                #             loading = True
                #             winPos = playedHand.winningCardPos(self.rules)
                #
                #             # ask the player to select a suite
                #             suite = p.selectASuite(self.rules)
                #             card = p.playACard(suite)

                # if card is None:  # when player doesn't have a card of the suite
                #     card = p.playARandomCard()
                #     if i != 0:  # more than one player has played
                #         # if this is first hand then no loading can happen
                #         if hand != 0:
                #             loading = True
                #             winPos = playedHand.winningCardPos(self.rules)
                #     else:
                #         suite = card.getSuite()

                # add the played card to the deck
                playedHand.addACard(card)

                # determine the starting position of next player
                if loading:
                    loadedPlayerPos = self.nextPlayerIndex(self.nextPlayerIndex(startPos) + (self.no_of_players-1 - i), winPos)
                    print "startpos = %d, winPos = %d, loadedPlayerPos = %d" %(startPos, winPos, loadedPlayerPos)
                    break
                else:
                    startPos = self.nextPlayerIndex(startPos)

            # for debugging
            playedHand.printIt()

            # prepare to start the next hand
            if loading:
                # loaded player has to pick the hand up
                self.players[loadedPlayerPos].getCardsInHand().mergeWith(playedHand)

                # the player who did the loading should start the next hand =>
                # so no need to change the startPos variable

                # for debugging
                print "Got LOADED ... ",
                self.players[loadedPlayerPos].printIt()
                self.players[loadedPlayerPos].printYourHand()

                # reset the variable
                loading = False
            else :
                winPos = playedHand.winningCardPos(self.rules)
                self.used_cards.mergeWith(playedHand)
                startPos = self.nextPlayerIndex(startPos, winPos)

            # move to the subsequent hand
            suite = None
            hand += 1

            # if (hand > 25):
            #	break


class Rummy(CardGame):
    def __init__(self, players, deck):
        super(Rummy, self).__init__(players, deck)
        self.trumpSuite = None

        self.used_cards = SetOfCards()
        # self.unused_cards = None

    def getTrumpSuite(self):
        return self.trumpSuite

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
