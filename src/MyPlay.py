from CardGame import *
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
#rummy.setRules(RummyRules())
#rummy.beginPlay()

lotan = GadhaLotan(players, FullDeck(), GadhaLotanRules())
#lotan.setRules(GadhaLotanRules())
lotan.beginPlay()