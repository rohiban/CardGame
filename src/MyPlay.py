from CardGame import *
from Cards import *
from Player import *
from CardGameRules import *

# the MAIN body

# create four card-players		
players = []
players.append(CardPlayer("Shwetha"))
players.append(CardPlayer("Aman"))
players.append(CardPlayer("Shashank"))
players.append(CardPlayer("Laddoo"))

# start the game
#rummy = Rummy(players, FullDeck())
#rummy.setRules(RummyRules(Card(Suites.SPADE, 1)))
#rummy.beginPlay()

lotan = GadhaLotan(players, FullDeck())
lotan.setRules(GadhaLotanRules(Card(Suites.SPADE, 1)))
lotan.beginPlay()