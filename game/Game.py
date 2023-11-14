from core.Engine import Engine
from core.Interval import Frame, Tick
from core.Scene import Scene
from core.Object import Object
from core.Camera import Camera
from core.pggui import Frame
from core.shaderLoader import ShaderProgram
from game.PlayerTurn import PlayerTurn
import Gamestate

from core.gui import *

class Game(Engine):
    HELP_MESSAGE = """<font size=5> Where's My Money -- Help </font>
    <p> Where's my money is a simple version of the classic board game monopoly. </p>
    """
    def __init__(self, width: int, height: int):
        # To be replaced with self.game_state, 
        # where player turn can be accessed from.
        #self.current_player : PlayerTurn = PlayerTurn()
        self.current_player = 1
        self.diceroled = False
        self.endturn = False
        self.g = Gamestate.Gamestate()

        self.test_gui = SimpleGUI("Debug & Testing")
        self.money_slider = self.test_gui.add_slider("Money", 0, 1500, 0, 10)

        super().__init__(width, height)

        self.guiSetup()

    def frame_update(self, frame: Frame):
        self.current_player.money = self.money_slider.get_value()
        self.money_label.id.set_text("Money: " + str(self.current_player.money))
        super().frame_update(frame)

    def guiSetup(self):
        help = self.guiManager.create_text(0, 0, self.ui_width, self.ui_height * self.height_fraction * 2, self.HELP_MESSAGE)
        help.hide()
        money_height = self.ui_height * self.height_fraction * 1 / 2
        self.money_label = self.guiManager.create_label(self.width - self.ui_width, 0, self.ui_width, money_height, text=
                                                        "Money: " + str(self.current_player.money))
        rules_height = self.ui_height * self.height_fraction * 1 / 4
        self.guiManager.create_button(self.width - self.ui_width, self.height - rules_height, self.ui_width, rules_height, text="Rules",
                                callback=help.toggle_visibility)

    def tick_update(self, tick: Tick):


        super().tick_update(tick)

    def run(self):
        super().run()

    def playerturn(self):
        if(self.current_player == 1):
            self.current_player = 2
        else:
            self.current_player = 1


    #Logical Processing of actions returned from gamestate and calls to animations. Needs GUI calls to be completed
    def logicRun(self):

        #placeholder replace 0 with dice value


        if(self.diceroled == True):
            dicevalue = 0 #add gui dice rolled method here

        self.diceroled == False

        action = self.g.gamelocation(dicevalue, self.current_player)

        if(action == "OfferToPayToLeaveJail"):
            if(self.GUIpayjail() == True):
                self.g.leavejail(self.current_player)
                action = self.g.gamelocation(dicevalue, self.current_player)

        if(action == "MoveToGo"):
            self.PlacePlayer("GO")

        elif (action == "OfferToBuyAirZandZRental"):
            self.PlacePlayer("AirZandZRental")
            if (self.GUIpayjail() == True):
                self.g.BuyAirZandZRental(self.current_player)


        elif (action == "MoveToAirZandZRental"):
            self.PlacePlayer("AirZandZRental")

        elif (action == "MoveToJustVisiting"):
            self.PlacePlayer("JustVisiting")

        elif (action == "OfferToBuySuburbanTownHouse"):
            self.PlacePlayer("SuburbanTownHouse")
            if (self.GUIpayjail() == True):
                self.g.BuySuburbanTownHouse(self.current_player)


        elif (action == "MoveToSuburbanTownHouse"):
            self.PlacePlayer("SuburbanTownHouse")

        elif (action == "OfferToBuyDownTownStudioApt"):
            self.PlacePlayer("DownTownStudioApt")
            if (self.GUIpayjail() == True):
                self.g.BuyDownTownStudioApt(self.current_player)


        elif (action == "MoveToDownTownStudioApt"):
            self.PlacePlayer("DownTownStudioApt")

        elif (action == "MoveToCourtBattleThenJail"):
            self.PlacePlayer("CourtBattle")
            self.PlacePlayer("Jail")

        elif (action == "OfferToBuySkyRiseFlat"):
            if (self.GUIpayjail() == True):
                self.g.BuySkyRiseFlat(self.current_player)
            self.PlacePlayer("SkyRiseFlat")

        elif (action == "MoveToSkyRiseFlat"):
            self.PlacePlayer("SkyRiseFlat")

        elif (action == "EventAdd100"):
            self.PlacePlayer("FreeParking")

        elif (action == "EventPlus2x"):
            self.PlacePlayer("FreeParking")

        elif (action == "EventMinus2x"):
            self.PlacePlayer("FreeParking")



        if(self.endturn == True):
            endingAction = self.g.endturn()
            if(endingAction == "Next Players Turn"):
                self.playerturn()

            elif(endingAction == "Player 1 Won"):
                ... #gui display winner
            elif(endingAction == "Player 2 Won"):
                ... #gui display winner
        self.endturn == False

    #GUI Call for JAIL
    def GUIpayjail(self):

        #update with GUI call for paying JAIL
        return True

    #moves player to specified location on board.
    def PlacePlayer(self, Location: str):

        if(Location == "GO"):
            x = 1
        if (Location == "AirZandZRental"):
            x = 1
        if (Location == "Jail"):
            x = 1
        if (Location == "JustVisiting"):
            x = 1
        if (Location == "SuburbanTownHouse"):
            x = 1
        if (Location == "DownTownStudioApt"):
            x = 1
        if (Location == "CourtBattle"):
            x = 1
        if (Location == "SkyRiseFlat"):
            x = 1
        if (Location == "FreeParking"):
            x = 1