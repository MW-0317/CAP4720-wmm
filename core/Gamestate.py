class Gamestate:

    def __init__(self):
        self.gamestate = True

        self.player1 = [1500, 0, 200]
        self.player2 = [1500, 0, 200]

        self.AirZandZRental = [0, 0, 0]
        self.DownTownStuidoApt = [0, 0, 0]
        self.SkyRiseFlat = [0, 0, 0]
        self.SuburbanTownHouse = [0, 0, 0]

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
    #this method finds where the peice should move based on the dice value roled and then call the corrent game state method to preform the action
    def gamelocation(self, dicevalue: int, currentplayer: int):

        if(currentplayer == 1):
            self.player1[1] = self.player1[1] + dicevalue
            playermove = self.player1[1]
            player = self.player1
        elif(currentplayer == 2):
            self.player2[1] = self.player2[1] + dicevalue
            playermove = self.player2[1]
            player = self.player2

        if(playermove % 8 == 0):
            #do GO
            return
        if (playermove % 8 == 1):
            # do LightBlue
            return self.get_rent("AirZandZRental", currentplayer)
        if (playermove % 8 == 2):
            # do Just Visiting
            return 0
        if (playermove % 8 == 3):
            # do Orange
            return self.get_rent("SuburbanTownHouse", currentplayer)
        if (playermove % 8 == 4):
            # do event/freeparking
            return 1
        if (playermove % 8 == 5):
            # do Yellow
            return self.get_rent("DownTownStuidoApt", currentplayer)
        if (playermove % 8 == 6):
            # do CourtBattle
            if(currentplayer == 1):
                self.player1[1] = playermove - 4
            elif(currentplayer == 2):
                self.player2[1] = playermove - 4
            return self.gamelocation(0, currentplayer)

        if (playermove % 8 == 7):
            # do Dark Blue
            return self.get_rent("SkyRiseFlat", currentplayer)



    def gamestate(self):

        if(self.player1[0] < 0):
            setgamestate = False
        if(self.player2[0] < 0):
            setgamestate = False

    #this method returns the cost of rent on a properity and 0 is the properity is morgatged
    def get_rent(self, properity: str, currentplayer: int):

        if(properity == 'AirZandZRental'):
            return self.AirZandZRental(currentplayer)
        elif(properity == 'DownTownStuidoApt'):
            return self.DownTownStuidoApt(currentplayer)
        elif(properity == 'SkyRiseFlat'):
            return self.SkyRiseFlat(currentplayer)
        elif (properity == 'SuburbanTownHouse'):
            return self.SuburbanTownHouse(currentplayer)

    def AirZandZRental(self, currentplayer: int):
        if(currentplayer == self.AirZandZRental[0]):
            return 0

        if(self.AirZandZRental[2] == 1):
            return 0
        elif(self.AirZandZRental[1] == 0):
            return 15
        elif(self.AirZandZRental[1] == 1):
            return 50
        elif(self.AirZandZRental[1] == 2):
            return 100
        elif(self.AirZandZRental[1] == 3):
            return 250
        elif(self.AirZandZRental[1] == 4):
            return 400
        elif(self.AirZandZRental[1] == 5):
            return 550
        else:
            return 0

    def SuburbanTownHouse(self, currentplayer: int):
        if (currentplayer == self.AirZandZRental[0]):
            return 0

        if(self.SuburbanTownHouse[2] == 1):
            return 0
        elif(self.SuburbanTownHouse[1] == 0):
            return 30
        elif(self.SuburbanTownHouse[1] == 1):
            return 100
        elif(self.SuburbanTownHouse[1] == 2):
            return 250
        elif(self.SuburbanTownHouse[1] == 3):
            return 600
        elif(self.SuburbanTownHouse[1] == 4):
            return 800
        elif(self.SuburbanTownHouse[1] == 5):
            return 1000
        else:
            return 0

    def DownTownStuidoApt(self, currentplayer: int):
        if (currentplayer == self.AirZandZRental[0]):
            return 0

        if(self.DownTownStuidoApt[2] == 1):
            return 0
        elif(self.DownTownStuidoApt[1] == 0):
            return 45
        elif(self.DownTownStuidoApt[1] == 1):
            return 150
        elif(self.DownTownStuidoApt[1] == 2):
            return 350
        elif(self.DownTownStuidoApt[1] == 3):
            return 750
        elif(self.DownTownStuidoApt[1] == 4):
            return 1000
        elif(self.DownTownStuidoApt[1] == 5):
            return 1200
        else:
            return 0

    def SkyRiseFlat(self, currentplayer: int):
        if (currentplayer == self.AirZandZRental[0]):
            return 0

        if(self.SkyRiseFlat[2] == 1):
            return 0
        elif(self.SkyRiseFlat[1] == 0):
            return 50
        elif(self.SkyRiseFlat[1] == 1):
            return 200
        elif(self.SkyRiseFlat[1] == 2):
            return 600
        elif(self.SkyRiseFlat[1] == 3):
            return 1300
        elif(self.SkyRiseFlat[1] == 4):
            return 1600
        elif(self.SkyRiseFlat[1] == 5):
            return 2000
        else:
            return 0