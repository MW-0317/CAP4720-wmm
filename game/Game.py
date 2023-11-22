from core.Engine import Engine
from core.Interval import Frame, Tick
from core.Scene import Scene
from core.Object import Object
from core.Camera import Camera
from core.pggui import Frame
from core.shaderLoader import ShaderProgram
from game.PlayerTurn import PlayerTurn
from game.Gamestate import Gamestate

import pygame as pg

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
        self.g = Gamestate()
        self.p = PlayerTurn(self)

        self.test_gui = SimpleGUI("Debug & Testing")
        self.money_slider = self.test_gui.add_slider("Money", 0, 1500, 1500, 10)
        self.position_slider = self.test_gui.add_slider("Position", 0, 7, 0, 1)
        self.g.player1[0] = self.money_slider.get_value()
        self.g.player1[1] = self.position_slider.get_value()

        super().__init__(width, height)

        self.guiSetup()

    def frame_update(self, frame: Frame):
        # TODO: Temporarily show current player positions using a beam or cylinder
        
        current_player_list = self.g.current_player_list(self.g.current_player)
        #current_player_list[0] = self.money_slider.get_value()
        current_player_list[1] = self.position_slider.get_value()
        
        # TODO: Set camera to side of board given position,
        # need to now get this into a function like getCurrentCameraPosition.
        # Would love to introduce camera animations if given time to provide
        # smooth transitions.
        # Rotate camera based on player's position.
        if self.scenes[0].current_camera != None:
            camera = self.scenes[0].current_camera
            camera_pos = [0, 2]
            def rotate(pos):
                return (-pos[1], pos[0])
            n = current_player_list[1] // 2
            for i in range(0, n):
                camera_pos = rotate(camera_pos)
            camera.set_position((camera_pos[0], 1, camera_pos[1]))
            camera.pan = 90 * n

        self.money_label.set_text("Money: " + str(current_player_list[0]))
        super().frame_update(frame)

    def run(self):
        super().run()

    def guiSetup(self):
        help_rect = pg.Rect(20, 20, self.ui_width, self.ui_height * self.height_fraction * 2)
        help = self.guiManager.create_text(self.HELP_MESSAGE, relative_rect=help_rect)
        help.hide()

        money_height = self.ui_height * self.height_fraction * 1 / 2
        money_rect = pg.Rect(self.width - self.ui_width, 0, self.ui_width, money_height)
        self.money_label = self.guiManager.create_label(relative_rect=money_rect, text="Money: " + str(self.g.player1[0]))

        rules_height = self.ui_height * self.height_fraction * 1 / 4
        rules_rect = pg.Rect(self.width - self.ui_width, self.height - rules_height, self.ui_width, rules_height)
        self.guiManager.create_button(relative_rect=rules_rect, text="Rules", callback=lambda ui: help.toggle_visibility())

        #self.player_turn.buy(self.gamestate, 1, "OfferToBuyAirZandZRental")
        #self.player_turn.roll_dice(self.gamestate, 1)
        self.g.player1[3] = 3
        self.p.prompt_jail(self.g, 1)

    def tick_update(self, tick: Tick):
        self.logicRun()
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

        # I will need to introduce many of these checkpoints
        # that come from PlayerTurn / self.p
        if self.p.dice_roll == -1: return
        self.p.prompt_jail(self.g, self.current_player)

        action = self.g.gamelocation(self.p.dice_roll, self.current_player)

        if(action == "OfferToPayToLeaveJail"):
            if(self.GUIpayjail() == True):
                self.g.leavejail(self.current_player)
                action = self.g.gamelocation(self.p.dice_roll, self.current_player)

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
