from CardGame import GadhaLotan, Rummy
from CardPlayer import CardPlayer
from CardGameRules import GadhaLotanRules, RummyRules
from Cards import FullDeck

# the MAIN body

# create four card-players		
players = [CardPlayer("Shwetha"), CardPlayer("Aman"), CardPlayer("Shashank"), CardPlayer("Laddoo")]

# start the game
#rummy = Rummy(players, FullDeck())
#rummy.setRules(RummyRules())
#rummy.beginPlay()

lotan = GadhaLotan(players, FullDeck(), GadhaLotanRules())
#lotan.setRules(GadhaLotanRules())
lotan.beginPlay()