import re

class Gamestate:
    """
    Tracks the current state of the game.
    """

    # Helper dictionary for getting property costs.
    property_prices = {
            "AirZandZRental":       300,
            "SuburbanTownHouse":    450,
            "DownTownStudioApt":    600,
            "SkyRiseFlat":          800
        }
    
    def __init__(self):
        self.gamestatecon = True

        #which event we are on, may add randomizing start later
        self.event = 0

        #money, player position, stock value, jail turns remaining
        self.player1 = [1500, 0, 200, 0]
        self.player2 = [1500, 0, 200, 0]
        self.current_player = 1

        #owner, number of houses, mortgaged 0 for false
        self.AirZandZRental = [0, 0, 0]
        self.DownTownStudioApt = [0, 0, 0]
        self.SkyRiseFlat = [0, 0, 0]
        self.SuburbanTownHouse = [0, 0, 0]

    def location_spaced_string(location: str):
        """
        Helper function to get the spaced version of the property string,
        with some regex and string magic.
        """
        return re.sub(r"(([A-Z](?!(and))[a-z]*)|[A-Z]|and)", r"\1 ", location)[:-1]
    
    def swap_current_player(self):
        self.current_player = self.current_player % 2 + 1
    
    def current_player_list(self, current_player: int) -> list:
        """
        Helper function to get the list of the current player
        """
        if current_player > 2: 
            return []
        return self.player1 if current_player == 1 else self.player2

    def getgamestatecon(self):
        return self.gamestatecon

    #this method finds where the piece should move based on the dice value rolled and then call the current game state method to preform the action
    #it then returns a string for game actions
    def gamelocation(self, dicevalue: int, currentplayer: int):

        #check jail before updating
        if (currentplayer == 1):
            if(self.player1[3] > 0):
                self.player1[3] = self.player1[3]-1
                if(self.player1[3] == 0):
                    self.player1[0] = self.player1[0] - 50
                else:
                    return "OfferToPayToLeaveJail"
        elif (currentplayer == 2):
            if (self.player2[3] > 0):
                self.player2[3] = self.player2[3] - 1
                if (self.player2[3] == 0):
                    self.player2[0] = self.player2[0] - 50
                else:
                    return "OfferToPayToLeaveJail"

        #updates player location
        if(currentplayer == 1):
            self.player1[1] = self.player1[1] + dicevalue
            playermove = self.player1[1]
        elif(currentplayer == 2):
            self.player2[1] = self.player2[1] + dicevalue
            playermove = self.player2[1]


        if((playermove-dicevalue)%8+dicevalue > 8):
            #if player passes GO give them money
            self.passgo(currentplayer)

        if(playermove % 8 == 0):
            #do GO
            self.passgo(currentplayer)
            return "MoveToGo"

        if (playermove % 8 == 1):
            # do LightBlue
            if(self.AirZandZRental[0] == 0):
                return "OfferToBuyAirZandZRental"

            rentvalue = self.get_rent("AirZandZRental", currentplayer)
            if (currentplayer == 1):
                self.player1[0] = self.player1[0] - rentvalue
                self.player2[0] = self.player2[0] + rentvalue
            elif (currentplayer == 2):
                self.player1[0] = self.player1[0] + rentvalue
                self.player2[0] = self.player2[0] - rentvalue
            return "MoveToAirZandZRental"

        if (playermove % 8 == 2):
            # do Just Visiting
            return "MoveToJustVisiting"

        if (playermove % 8 == 3):
            # do Orange
            if (self.SuburbanTownHouse[0] == 0):
                return "OfferToBuySuburbanTownHouse"

            rentvalue = (self.get_rent("SuburbanTownHouse", currentplayer))
            if (currentplayer == 1):
                self.player1[0] = self.player1[0] - rentvalue
                self.player2[0] = self.player2[0] + rentvalue
            elif (currentplayer == 2):
                self.player1[0] = self.player1[0] + rentvalue
                self.player2[0] = self.player2[0] - rentvalue
            return "MoveToSuburbanTownHouse"

        if (playermove % 8 == 4):
            # do event/freeparking
            return self.getevent(currentplayer)

        if (playermove % 8 == 5):
            # do Yellow
            if (self.DownTownStudioApt[0] == 0):
                return "OfferToBuyDownTownStudioApt"

            rentvalue = self.get_rent("DownTownStudioApt", currentplayer)
            if (currentplayer == 1):
                self.player1[0] = self.player1[0] - rentvalue
                self.player2[0] = self.player2[0] + rentvalue
            elif (currentplayer == 2):
                self.player1[0] = self.player1[0] + rentvalue
                self.player2[0] = self.player2[0] - rentvalue
            return "MoveToDownTownStudioApt"

        if (playermove % 8 == 6):
            # do CourtBattle
            if(currentplayer == 1):
                self.player1[1] = playermove - 4
                self.player1[3] = 3
            elif(currentplayer == 2):
                self.player2[1] = playermove - 4
                self.player2[3] = 3
            return "MoveToCourtBattleThenJail"

        if (playermove % 8 == 7):
            # do Dark Blue
            if (self.SkyRiseFlat[0] == 0):
                return "OfferToBuySkyRiseFlat"

            rentvalue = self.get_rent("SkyRiseFlat", currentplayer)
            if (currentplayer == 1):
                self.player1[0] = self.player1[0] - rentvalue
                self.player2[0] = self.player2[0] + rentvalue
            elif (currentplayer == 2):
                self.player1[0] = self.player1[0] + rentvalue
                self.player2[0] = self.player2[0] - rentvalue
            return "MoveToSkyRiseFlat"

    #this method add money to the player that passed or landed on go based on their go value
    def passgo(self, currentplayer: int):
        if (self.event == 0):
            if (currentplayer == 1):
                self.player1[0] = self.player1[0] + self.player1[2]
            elif (currentplayer == 2):
                self.player2[0] = self.player1[0] + self.player2[2]

    #call this when a player chooses to leave jail by paying 50
    def leavejail(self, currentplayer: int):

        if (currentplayer == 1):
            self.player1[3] = 0
            if(self.player1[3] == 0):
                self.player1[0] = self.player1[0] - 50
        elif (currentplayer == 2):
            self.player2[3] = 0
            if (self.player2[3] == 0):
                self.player2[0] = self.player2[0] - 50


    #this method returns the name of the event and proccess the event
    def getevent(self, currentplayer: int):
        if(self.event == 0):
            if (currentplayer == 1):
                self.player1[0] = self.player1[0] + 100
            elif (currentplayer == 2):
                self.player2[0] = self.player2[0] + 100
            self.event = self.event + 1
            return "EventAdd100"

        if (self.event == 1):
            if (currentplayer == 1):
                self.player1[0] = self.player1[2]*2
            elif (currentplayer == 2):
                self.player2[0] = self.player2[2]*2
            self.event = self.event + 1
            return "EventPlus2x"

        if (self.event == 2):
            if (currentplayer == 1):
                self.player1[0] = self.player1[2]*0.5
            elif (currentplayer == 2):
                self.player2[0] = self.player2[2]*0.5
            self.event = self.event + 1
            return "EventMinus2x"

    #Methods for updating gamestate
    def endturn(self):

        return self.checkgamestate()

    def forfit(self):
        self.gamestatecon = False

    def checkgamestate(self):

        if(self.player1[0] < 0):
            self.gamestatecon = False
            return "Player 2 Won"

        if(self.player2[0] < 0):
            self.gamestatecon = False
            return "Player 1 Won"

        return "Next Players Turn"

    #this method returns the cost of rent on a properity and 0 is the properity is morgatged
    def get_rent(self, properity: str, currentplayer: int):

        if(properity == 'AirZandZRental'):
            return self.AirZandZRentalRent(currentplayer)
        elif(properity == 'DownTownStudioApt'):
            return self.DownTownStudioAptRent(currentplayer)
        elif(properity == 'SkyRiseFlat'):
            return self.SkyRiseFlatRent(currentplayer)
        elif (properity == 'SuburbanTownHouse'):
            return self.SuburbanTownHouseRent(currentplayer)
        
    def buy_property(self, currentplayer: int, prop: str):
        """
        Buy's a property by calling a given Buy...() function.
        """
        func = getattr(self, "Buy" + prop)
        func(currentplayer)

    def get_property_price(self, prop: str):
        return self.property_prices[prop]

    def BuyAirZandZRental(self, currentplayer: int):
        if (currentplayer == 1):
            self.player1[0] = self.player1[0] - 300
            self.AirZandZRental[0] = 1
        elif (currentplayer == 2):
            self.player2[0] = self.player2[0] - 300
            self.AirZandZRental[0] = 2

    def AirZandZRentalRent(self, currentplayer: int):
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

    def BuySuburbanTownHouse(self, currentplayer: int):
        if (currentplayer == 1):
            self.player1[0] = self.player1[0] - 450
            self.SuburbanTownHouse[0] = 1
        elif (currentplayer == 2):
            self.player2[0] = self.player2[0] - 450
            self.SuburbanTownHouse[0] = 2

    def SuburbanTownHouseRent(self, currentplayer: int):
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

    def BuyDownTownStudioApt(self, currentplayer: int):
        if (currentplayer == 1):
            self.player1[0] = self.player1[0] - 600
            self.DownTownStudioApt[0] = 1
        elif (currentplayer == 2):
            self.player2[0] = self.player2[0] - 600
            self.DownTownStudioApt[0] = 2

    def DownTownStudioAptRent(self, currentplayer: int):
        if (currentplayer == self.AirZandZRental[0]):
            return 0

        if(self.DownTownStudioApt[2] == 1):
            return 0
        elif(self.DownTownStudioApt[1] == 0):
            return 45
        elif(self.DownTownStudioApt[1] == 1):
            return 150
        elif(self.DownTownStudioApt[1] == 2):
            return 350
        elif(self.DownTownStudioApt[1] == 3):
            return 750
        elif(self.DownTownStudioApt[1] == 4):
            return 1000
        elif(self.DownTownStudioApt[1] == 5):
            return 1200
        else:
            return 0

    def BuySkyRiseFlat(self, currentplayer: int):
        if (currentplayer == 1):
            self.player1[0] = self.player1[0] - 800
            self.SkyRiseFlat[0] = 1
        elif (currentplayer == 2):
            self.player2[0] = self.player2[0] - 800
            self.SkyRiseFlat[0] = 2

    def SkyRiseFlatRent(self, currentplayer: int):
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