from CardGame import GadhaLotan, Rummy
from CardPlayer import CardPlayer
from CardGameRules import GadhaLotanRules, RummyRules, BestCriteria
from Cards import FullDeck

__author__ = 'rbansal'


# the MAIN body

# create four card-players		
players = [CardPlayer("Jinesh"), CardPlayer("Laddoo"), CardPlayer("Shashank"), CardPlayer("Sunder")]

# set the rule
# rule = GadhaLotanRules()
rule = RummyRules()

rule.setBestSuiteCriteria(BestCriteria.VALUE)

# set the game
# game = GadhaLotan(players, FullDeck(), rule)
game = Rummy(players, FullDeck(), rule)

# start the game
game.beginPlay()