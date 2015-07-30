import random
from Cards import Card, SetOfCards, Hand

__author__ = 'rbansal'


class Game(object):
    def __init__(self, players):
        self.players = players
        self.no_of_players = len(players)

    def beginPlay(self):
        return NotImplemented


class PlayerPoint(object):
    def __init__(self, p, pts=0):
        self.player = p
        self.points = pts

    def __str__(self):
        return "%s [%d points]" % (self.player, self.points)

    def __unicode__(self):
        return self.__str__()

    def __cmp__(self, other):
        return int.__cmp__(self.points, other.points)

    def addPoints(self, pts):
        self.points += pts

    def isForPlayer(self, p):
        return self.player == p


class CardGame(Game):
    def __init__(self, players, cardDeck, rules):
        super(CardGame, self).__init__(players)
        self.card_deck = cardDeck
        self.rules = rules
        self.unused_cards = None
        self.pointsTable = None

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

    def beginPlay(self):
        # initialize the points table
        self.pointsTable = []
        for p in self.players:
            self.pointsTable.append(PlayerPoint(p, 0))

    def updatePoints(self, player, pts=1):
        for p_pt in self.pointsTable:
            if p_pt.isForPlayer(player):
                p_pt.addPoints(pts)
                break

    # get the next player given a player
    def nextPlayer(self, p):
        for i, player in enumerate(self.players):
            if player == p:
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
        # call the base class' method first
        super(GadhaLotan, self).beginPlay()

        no_of_cards = self.rules.maxCountAfterDealing()
        self.initialize(no_of_cards)

        # initialize the played hand variable
        playedHand = Hand()

        # print the hands of all players (for debugging)
        # for p in self.players:
        #     print "%s" % p
        #     print "%s" % p.getCardsInHand()

        # which player has Ace of Spade [starting card]
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
            # print "%s" % playedHand

            if loading:
                # loaded player needs to pick up the hand
                winningPlayer.getCardsInHand().mergeWith(playedHand)

                # print "Got Loaded ... ",
                # print "%s" % winningPlayer
                # print "%s" % winningPlayer.getCardsInHand()

                # reset variables, though current player starts the next hand
                suite = None
                loading = False
            else:
                p = winningPlayer
                suite = None

            playedHand = Hand()
            hand += 1

        # for p in self.players:
        #     print "%s" % p
        #     print "%s" % p.getCardsInHand()

        loser = self.getTheLoser()
        print "Gadhaaaaaaaa is ...",
        print "%s" % loser
        print "%s" % loser.getCardsInHand()


class Rummy(CardGame):
    def __init__(self, players, deck, rules):
        super(Rummy, self).__init__(players, deck, rules)
        self.trumpSuite = None

        self.used_cards = SetOfCards()
        # self.unused_cards = None

    def getTrumpSuite(self):
        return self.trumpSuite

    def theWinner(self):
        sorted_list = sorted(self.pointsTable, reverse=True)
        return sorted_list[0]

    def beginPlay(self):
        # call the base class' method first
        super(Rummy, self).beginPlay()

        trumpDeclared = False

        no_of_cards = self.rules.maxCountAfterDealing()
        self.initialize(no_of_cards)

        # initialize the hand
        playedHand = Hand()

        # for debugging
        for p in self.players:
            print "%s" % p
            print "%s" % p.getCardsInHand()

        # select randomly a player to start the game
        p = self.players[random.randint(0, len(self.players)-1)]

        # for debugging
        # print "starting player ... %s" % p

        for hand in range(no_of_cards):
            # play a new hand
            print "# %d" %(hand+1)

            # loop as many times as number of players
            for i in range(self.no_of_players):

                if i == 0:  # first player in a hand
                    suite = p.selectASuite(self.rules)
                    card = p.playACard(suite)
                    # print "%s" % suite
                    # print "%s" % p

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
            print "%s" % playedHand

            # determine the player starting the next hand
            (p, winningCard) = winners

            # update the point tally for the player
            self.updatePoints(p)

            # merge the played hand with the used card deck
            self.used_cards.mergeWith(playedHand)

        # declare the winner
        print "The Winner is ... %s" % self.theWinner()

        # for debugging
        # for p_pt in self.pointsTable:
        #    print "%s" % p_pt
