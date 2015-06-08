no_of_players = 4
players = []
i = 0
for s in ["A", "B", "C", "D"]:
	players.append([s, i+1])
	i += 1
	#players.append(100+i)
	#print players[i]

print players,
print ""

#np = [2,3,0,1]
for i in range(no_of_players):
	players[i][1] = (i+1)*(i+1)
	#pass
	
print "I am ...",
print players


	