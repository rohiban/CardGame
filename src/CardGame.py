import random
from CardGameRules import GadhaLotanRules
from Cards import Card, SetOfCards, Hand

__author__ = 'rbansal'


class Game(object):
    def __init__(self, players):
        self.players = players
        self.no_of_players = len(players)

    def beginPlay(self):
        return NotImplemented

    # def setRules(self, rules):
    #     self.rules = rules
    #
    # def getRules(self):
    #     return self.rules


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
        for i in range(noOfCardsToDistribute / cardsInOneChunk):
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
        # self.dealCards(floor(self.card_deck.cardCount() / len(self.players)))

    def beginPlay(self):
        return NotImplemented

    # def nextPlayerIndex(self, currIndex, delta=1):
    #     currIndex += delta
    #     if currIndex > (self.no_of_players-1):
    #         currIndex -= self.no_of_players
    #     return currIndex

    # get the next player given a player
    def nextPlayer(self, p):
        for i, player in enumerate(self.players):
            if p.isSame(player):
                return self.players[(i + 1) % self.no_of_players]

        return None

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

    def getTheLoser(self):
        for p in self.players:
            if p.noOfCardsInHand() != 0:
                return p
        return None

    def beginPlay(self):
        no_of_cards = self.rules.maxCountAfterDealing()
        self.initialize(no_of_cards)

        # initialize the played hand variable
        playedHand = Hand()

        # print the hands of all players (for debugging)
        # for p in self.players:
        #     p.printIt()
        #     p.printYourHand()

        # which player has Ace of Spade [starting card]
        # card = self.rules.startingCard()
        # suite = card.getSuite()
        p = self.playerWithCard(self.rules.startingCard())

        hand = 0
        loading = False

        # continue as long as there is more than one player, holding cards in hand
        while self.playersWithCardsInHand() > 1:

            # iterate over all players
            for i in range(self.no_of_players):

                # for the very first hand, play the starting card
                if (hand == 0) & (i == 0):
                    card = p.playTHECard(self.rules.startingCard())
                    suite = card.getSuite()

                    # set variables
                    winningPlayer = p
                    winningCard = card
                else:
                    # declare the player as winner if no cards in hand
                    if p.noOfCardsInHand() == 0:
                        # select the next player and move on
                        p = self.nextPlayer(p)
                        continue

                    if suite is None:  # beginning of a hand
                        suite = p.selectASuite(self.rules)
                        card = p.playACard(suite)
                        winningCard = card
                        winningPlayer = p
                    else:
                        if p.hasCardOfSuite(suite):
                            card = p.playACard(suite)
                        else:
                            loading = True
                            suite = p.selectASuite(self.rules)
                            card = p.playACard(suite)

                # add the card to played hand
                playedHand.addACard(card)

                if loading:
                    break

                # for debugging
                # print "hand = %d, i = %d" %(hand, i)

                # determine the winning card, SO FAR
                if self.rules.rankFunction(card, winningCard):
                    winningCard = card
                    winningPlayer = p

                # determine the next player
                p = self.nextPlayer(p)

            # for debugging
            # playedHand.printIt()

            if loading:
                # loaded player needs to pick up the hand
                winningPlayer.getCardsInHand().mergeWith(playedHand)

                #print "Got Loaded ... ",
                #winningPlayer.printIt()
                #winningPlayer.printYourHand()

                # reset variables, though current player starts the next hand
                suite = None
                loading = False
            else:
                p = winningPlayer
                suite = None

            playedHand = Hand()
            hand += 1

        # for p in self.players:
        #     p.printIt()
        #     p.printYourHand()

        print "Gadhaaaaaaaa is ...",
        loser = self.getTheLoser()
        loser.printIt()
        loser.printYourHand()


class Rummy(CardGame):
    def __init__(self, players, deck, rules):
        super(Rummy, self).__init__(players, deck, rules)
        self.trumpSuite = None

        self.used_cards = SetOfCards()
        # self.unused_cards = None

    def getTrumpSuite(self):
        return self.trumpSuite

    def beginPlay(self):
        trumpDeclared = False

        no_of_cards = self.rules.maxCountAfterDealing()
        self.initialize(no_of_cards)

        # initialize the hand
        playedHand = Hand()

        # for debugging
        for p in self.players:
            p.printIt()
            p.printYourHand()

        # select randomly a player to start the game
        # startPos = self.rules.startingPlayerPos(self.players)
        # p = self.players[startPos]
        p = self.players[random.randint(0, len(self.players)-1)]

        # for debugging
        # print "starting player ... ",
        # p.printIt()

        # suite = self.rules.startingCard().getSuite()

        for hand in range(no_of_cards):
            # play a new hand
            print "# %d" %(hand+1)

            # loop as many times as number of players
            for i in range(self.no_of_players):

                if i == 0:  # first player in a hand

                    suite = p.selectASuite(self.rules)
                    card = p.playACard(suite)
                    # print "%s" % suite
                    # p.printIt()

                    # store these as winners
                    winners = (p, card)
                else:  # other players
                    if p.hasCardOfSuite(suite):
                        card = p.playACard(suite)

                        # check which is the winner
                        (winningPlayer, winningCard) = winners

                        if self.rules.rankFunction(card, winningCard):
                            winners = (p, card)
                    else:
                        if trumpDeclared:
                            if p.hasCardOfSuite(trumpSuite):
                                card = p.playACard(trumpSuite)

                                # check which is the winner
                                (winningPlayer, winningCard) = winners

                                if self.rules.rankFunction(card, winningCard):
                                    winners = (p, card)
                            else:
                                card = p.playARandomCard()
                        else:  # create trump
                            trumpSuite = self.rules.determineTrump(p.getCardsInHand())
                            self.rules.setTrump(trumpSuite)
                            trumpDeclared = True
                            card = p.playACard(trumpSuite)
                            winners = (p, card)

                            # for debugging
                            print "Trump is %s" % trumpSuite

                # add the card to played hand
                playedHand.addACard(card)

                # select next player
                p = self.nextPlayer(p)

            # for debugging
            playedHand.printIt()

            # determine the player starting the next hand
            (p, winningCard) = winners

            # merge the played hand with the used card deck
            self.used_cards.mergeWith(playedHand)


            #     if (hand == 0) & (i == 0):
            #         card = p.playTHECard(self.rules.startingCard())
            #     else:
            #         card = p.playACard(suite)
            #
            #     while card is None:
            #         if not trumpDeclared:
            #             trumpSuite = self.rules.determineTrump(p.getCardsInHand())
            #             self.rules.setTrump(trumpSuite)
            #             trumpDeclared = True
            #
            #             # for debugging
            #             print "Trump is %s" %trumpSuite
            #
            #         if p.hasCardOfSuite(trumpSuite):
            #             card = p.playACard(trumpSuite)
            #         else:
            #             card = p.playARandomCard()
            #
            #     # add the card to the played hand
            #     playedHand.addACard(card)
            #
            #     # select the next player
            #     startPos = self.nextPlayerIndex(startPos)
            #
            # # for debugging
            # playedHand.printIt()
            #
            # winPos = playedHand.winningCardPos(self.rules)
            # startPos = self.nextPlayerIndex(startPos, winPos)
            #
            # # suite = playedHand.getTopCard().getSuite()
            # self.used_cards.mergeWith(playedHand)
