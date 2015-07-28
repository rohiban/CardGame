from CardGame import GadhaLotan, Rummy
from CardPlayer import CardPlayer
from CardGameRules import GadhaLotanRules, RummyRules, BestCriteria
from Cards import FullDeck

__author__ = 'rbansal'


# the MAIN body

# create four card-players		
players = [CardPlayer("Jinesh"), CardPlayer("Laddoo"), CardPlayer("Shashank"), CardPlayer("Sunder")]

# start the game
#rummy = Rummy(players, FullDeck(), RummyRules())
#rummy.beginPlay()

# set the rule
rule = GadhaLotanRules()
rule.setBestSuiteCriteria(BestCriteria.VALUE)

lotan = GadhaLotan(players, FullDeck(), rule)
lotan.beginPlay()