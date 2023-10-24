class Gamestate:
    def __init__(self):
        self.gamestate = True

        '''
        will need to know what each player position is at
        player1 = 
        player2 = 
        
        AirZ&ZRental =
        DownTownStuidoApt =
        SkyRiseFlat = 
        SuburbanTownHouse =
        
    
        '''

'''

Def: create players
this should create a player and hold information on the players money(1500) and position(1-9), and game piece(cat.obj)





Def: new game
This method should create new game and creating 2 players and setting them at go position, and create new properitys

def: new_game(player1 choice x, player2 choice y)
        player1 = create player(x)
        player2 = create player(y)
        
        player1.position.set(0)
        player2.position.set(0)
        
        create_properitys()



Def: player position
get player position
set player position

Def: gameover
This method should check it ethier player 1 or 2 has less then 0 cash
This should check at the end of every turn.
If it is not true, change gamestate to false


Def: create_properitys
This method should inillaize each of the 4 properitys with who owns what, and wether a properity is morgatged


Def: properitys_values
This method holds the information for each property

'''