from core.Engine import Engine
from core.Interval import Frame, Tick
from core.Scene import Scene
from core.Object import Object
from core.Camera import Camera
from core.pggui import Frame
from core.shaderLoader import ShaderProgram
from game.PlayerTurn import PlayerTurn, GuiAction
from game.Gamestate import Gamestate
from game.Animation import *

import math
import pyrr
import pygame as pg
from pygame_gui.core import ObjectID

from core.gui import *

class Game(Engine):
    HELP_MESSAGE = """<font size=5> Where's My Money -- Help </font>
    <p> Where's my money is a simple version of the classic board game monopoly. </p>
    """
    positions = [
        [ 0.5,  0.13,  0.5], # 0
        [ 0.0,  0.13,  0.5], # 1
        [-0.5,  0.13,  0.5], # 2
        [-0.5,  0.13,  0.0], # 3
        [-0.5,  0.13, -0.5], # 4
        [ 0.0,  0.13, -0.5], # 5
        [ 0.5,  0.13, -0.5], # 6
        [ 0.5,  0.13,  0.0]  # 7
    ]
    @staticmethod
    def rotations(index):
        return [0, (((index + 1) % 4) * math.pi) / 2, 0]
    rotation_offsets = [
        [math.pi / 2,   0,  0], # Player 1
        [0,             0,  0]  # Player 2
    ]
    def __init__(self, width: int, height: int):
        # To be replaced with self.game_state, 
        # where player turn can be accessed from.
        #self.current_player : PlayerTurn = PlayerTurn()
        self.current_player = 1
        self.action = ""
        self.g = Gamestate()
        self.p = PlayerTurn(self)
        self.player_objects = []
        self.LightBlueHouse_objects = []
        self.OrangeHouse_objects = []
        self.YellowHouse_objects = []
        self.DarkBlueHouse_objects = []
        self.EventCard_objects = []

        self.animations: list[Animation] = []

        self.test_gui = SimpleGUI("Debug & Testing")
        self.cheat_slider = self.test_gui.add_checkbox("sv_cheats", False)
        self.dice_slider_1 = self.test_gui.add_slider("Dice Roll #1", 1, 6, 1, 1)
        self.dice_slider_2 = self.test_gui.add_slider("Dice Roll #2", 1, 6, 1, 1)
        self.tps_slider = self.test_gui.add_slider("TPS", 1, 120, 60, 1)
        self.dice_slider_1.get_value()
        self.dice_slider_2.get_value()

        super().__init__(width, height)

        self.guiSetup()

    def frame_update(self, frame: Frame):
        self.cheat_slider.get_value()
        self.dice_slider_1.get_value()
        self.dice_slider_2.get_value()

        new_tps = self.tps_slider.get_value()
        if new_tps != self.TPS and self.cheat_slider.get_value():
            self.set_tps(new_tps)
        
        # TODO: Temporarily show current player positions using a beam or cylinder
        
        current_player_list = self.g.current_player_list(self.current_player)
        #current_player_list[0] = self.money_slider.get_value()
        #current_player_list[1] = self.position_slider.get_value()
        
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

        self.money_label_1.set_text("P1: " + str(self.g.player1[0]))
        self.money_label_2.set_text("P2: " + str(self.g.player2[0]))
        self.stock_label_1.set_text("Stock: " + str(self.g.player1[2]))
        self.stock_label_2.set_text("Stock: " + str(self.g.player2[2]))
        if self.last_money[0] != self.g.player1[0] or self.last_money[1] != self.g.player2[0]:
            self.update_label_1.update_value(str(self.g.player1[0] - self.last_money[0]))
            self.update_label_2.update_value(str(self.g.player2[0] - self.last_money[1]))
            self.last_money[0] = self.g.player1[0]
            self.last_money[1] = self.g.player2[0]
        self.current_player_label.set_text("C: " + str(self.current_player))
        super().frame_update(frame)

    def run(self):
        super().run()

    def guiSetup(self):
        help_rect = pg.Rect(20, 20, self.ui_width, self.ui_height * self.height_fraction * 2)
        help = self.guiManager.create_text(self.HELP_MESSAGE, relative_rect=help_rect)
        help.hide()

        total_height = 0
        def add_box(height_fraction):
            nonlocal total_height
            rect = pg.Rect(self.width - self.ui_width, total_height, self.ui_width, self.ui_height * self.height_fraction * height_fraction)
            total_height += self.ui_height * self.height_fraction * height_fraction
            return rect
        
        total_width = 0
        def add_box_bottom():
            nonlocal total_width
            rect = pg.Rect(total_width, self.height - self.ui_height * self.height_fraction, self.ui_width, self.ui_height * self.height_fraction * 1/2)
            total_width += self.ui_width
            return rect
        
        total_width2 = 0
        def add_box_bottom2():
            nonlocal total_width2
            rect = pg.Rect(total_width2, self.height - self.ui_height * self.height_fraction * 1/2, self.ui_width, self.ui_height * self.height_fraction * 1/2)
            total_width2 += self.ui_width
            return rect
        
        total_width3 = 0
        def add_box_bottom3():
            nonlocal total_width3
            rect = pg.Rect(total_width3, self.height - self.ui_height * self.height_fraction * 5/4, self.ui_width, self.ui_height * self.height_fraction * 1/4)
            total_width3 += self.ui_width
            return rect

        money_rect = add_box_bottom()
        self.money_label_1 = self.guiManager.create_label(relative_rect=money_rect, text="P1: " + str(self.g.player1[0]))

        money_rect = add_box_bottom()
        self.money_label_2 = self.guiManager.create_label(relative_rect=money_rect, text="P2: " + str(self.g.player2[0]))

        stock_rect = add_box_bottom2()
        self.stock_label_1 = self.guiManager.create_label(relative_rect=stock_rect, text="Stock: " + str(self.g.player1[2]))

        stock_rect = add_box_bottom2()
        self.stock_label_2 = self.guiManager.create_label(relative_rect=stock_rect, text="Stock: " + str(self.g.player2[2]))

        self.last_money = [self.g.player1[0], self.g.player2[0]]

        update_rect = add_box_bottom3()
        self.update_label_1 = self.guiManager.create_update_label(relative_rect=update_rect, text="", object_id=ObjectID(class_id="@update_label", object_id=""))

        update_rect = add_box_bottom3()
        self.update_label_2 = self.guiManager.create_update_label(relative_rect=update_rect, text="", object_id=ObjectID(class_id="@update_label", object_id=""))

        current_player_rect = add_box(1/2)
        self.current_player_label = self.guiManager.create_label(relative_rect=current_player_rect, text="1")

        roll_button_rect = add_box(1/2)
        def roll_dice(ui):
            if self.guiManager.window_active and not self.animations == []: return
            self.p.roll_dice(self.g)
        self.roll_button = self.guiManager.create_button(relative_rect=roll_button_rect, text="Roll", callback=lambda ui: roll_dice(ui))

        end_turn_rect = add_box(1/2)
        def end_turn(ui):
            if self.guiManager.window_active and not self.animations == []: return
            self.p.end_turn()
        self.end_turn_button = self.guiManager.create_button(relative_rect=end_turn_rect, text="End Turn", callback=lambda ui: end_turn(ui))

        rules_height = self.ui_height * self.height_fraction * 1 / 4
        rules_rect = pg.Rect(self.width - self.ui_width, self.height - rules_height, self.ui_width, rules_height)
        self.guiManager.create_button(relative_rect=rules_rect, text="Rules", callback=lambda ui: help.toggle_visibility())

        #self.player_turn.buy(self.gamestate, 1, "OfferToBuyAirZandZRental")
        #self.player_turn.roll_dice(self.gamestate, 1)
        # self.g.player1[3] = 3
        # self.p.prompt_jail(self.g, 1)

    def tick_update(self, tick: Tick):
        self.logicRun()
        self.update_animations(tick)
        super().tick_update(tick)

    def update_animations(self, tick: Tick):
        i = 0
        animations_size = len(self.animations)
        while i < animations_size:
            if self.animations[i].is_empty():
                self.animations.pop(i)
                animations_size -= 1
                if animations_size == 0: self.p.should_update_logic = True
                continue
            i+=1
        if animations_size > 0:
            self.animations[0].tick_update(tick)

    def run(self):
        super().run()

    def playerturn(self):
        self.current_player = self.current_player % 2 + 1
        self.roll_button.show()
        self.p = PlayerTurn(self)

    # Logical Processing of actions returned from gamestate and calls to animations. 
    # Needs GUI calls to be completed
    def logicRun(self):
        if self.guiManager.window_active: return
        if not self.animations == []: return
        if self.p.should_end():
            endingAction = self.g.endturn()
            if(endingAction == "Next Players Turn"):
                self.playerturn()

            elif(endingAction == "Player 1 Won"):
                ... #gui display winner
            elif(endingAction == "Player 2 Won"):
                ... #gui display winner
        
        if not self.p.should_update_logic and self.p.dice_roll == -1: return

        if self.p.dice_roll != -1:
            self.action = self.g.gamelocation(self.p.dice_roll, self.current_player)
        elif self.p.player_action != GuiAction.BUY:
            self.p.buy(self.g, self.current_player, self.action)
        print("Player Action:", self.p.player_action)
        print(self.action)
        print(self.p.should_update_logic)

        if(self.action == "OfferToPayToLeaveJail"):
            if self.GUIpayjail():
                self.g.leavejail(self.current_player)
            else: 
                self.p.prompt_jail(self.g, self.current_player)

        if(self.action == "MoveToGo"):
            self.PlacePlayer("GO")

        elif (self.action == "OfferToBuyAirZandZRental"):
            self.PlacePlayer("AirZandZRental")
            if self.wantsToBuy():
                self.g.BuyAirZandZRental(self.current_player)       

        elif (self.action == "MoveToAirZandZRental"):
            self.PlacePlayer("AirZandZRental")

        elif (self.action == "MoveToJustVisiting"):
            self.PlacePlayer("JustVisiting")

        elif (self.action == "OfferToBuySuburbanTownHouse"):
            self.PlacePlayer("SuburbanTownHouse")
            if self.wantsToBuy():
                self.g.BuySuburbanTownHouse(self.current_player)


        elif (self.action == "MoveToSuburbanTownHouse"):
            self.PlacePlayer("SuburbanTownHouse")

        elif (self.action == "OfferToBuyDownTownStudioApt"):
            self.PlacePlayer("DownTownStudioApt")
            if self.wantsToBuy():
                self.g.BuyDownTownStudioApt(self.current_player)


        elif (self.action == "MoveToDownTownStudioApt"):
            self.PlacePlayer("DownTownStudioApt")

        elif (self.action == "MoveToCourtBattleThenJail" and self.p.dice_roll != -1):
            self.PlacePlayer("CourtBattle")
            self.p.dice_roll = 4
            self.PlacePlayer("Jail")

        elif (self.action == "OfferToBuySkyRiseFlat"):
            self.PlacePlayer("SkyRiseFlat")
            if self.wantsToBuy():
                self.g.BuySkyRiseFlat(self.current_player)

        elif (self.action == "MoveToSkyRiseFlat"):
            self.PlacePlayer("SkyRiseFlat")

        elif (self.action == "EventAdd100"):
            self.PlacePlayer("FreeParking")
            self.animationEvents(self.action)

        elif (self.action == "EventPlus2x"):
            self.PlacePlayer("FreeParking")
            self.animationEvents(self.action)

        elif (self.action == "EventMinus2x"):
            self.PlacePlayer("FreeParking")
            self.animationEvents(self.action)

        self.p.dice_roll = -1
        self.p.should_update_logic = False

    #event card animations
    def animationEvents(self, action: str):

        c1 = self.EventCard_objects[0]
        c2 = self.EventCard_objects[1]
        c3 = self.EventCard_objects[2]

        if (action == "EventAdd100"):

            self.displayCard(0)
            # returns card to deck
            c1.set_position([0, 0.025, 0])
            c1.set_rotation([0, math.pi / 2, math.pi / 2])

        elif (action == "EventPlus2x"):

            self.displayCard(1)
            # returns card to deck
            c2.set_position([0, 0.020, 0])
            c2.set_rotation([0, math.pi / 2, math.pi / 2])

        elif (action == "EventMinus2x"):

            self.displayCard(2)
            #returns card to deck
            c3.set_position([0, 0.015, 0])
            c3.set_rotation([0, math.pi / 2, math.pi / 2])

    #place card in front of camera for a time
    def displayCard(self, eventnumber: int):

        start = 0
        end = 60

        card = self.EventCard_objects[eventnumber]

        # Attach someObject to the animation
        anim = Animation(card)

        # Create Keyframes to raise card from deck
        start = Keyframe(pyrr.Vector3([0, 0.015, 0]), 30)
        middle = Keyframe(pyrr.Vector3([0, 0.6, 0]), 45)

        # Create Keyframes to make the card rotate to face the camera
        rotate = Keyframe(pyrr.Vector3([0, math.pi / 2, math.pi / 2]), 5)
        rotateEnd = Keyframe(pyrr.Vector3([math.pi, math.pi / 2, math.pi / 2]), 0)

        # Create Keyframes to hold the card in front of the camera for 120 ticks
        hold = Keyframe(pyrr.Vector3([0.3, 0.6, 0.3]), 120) #need to update with camera pos!!!
        end = Keyframe(pyrr.Vector3([0, 0.015, 0]), 0)
        # Must be pyrr.Vector3 or else it won't do arithmetic properly in Animation
        # Last keyframe *must* be zero ticks long

        # Append keyframes to animation
        anim.positions.append(start)  # Can also be animation.scales or animation.rotations
        anim.positions.append(middle)
        anim.rotations.append(rotate)
        anim.rotations.append(rotateEnd)
        anim.positions.append(hold)
        anim.positions.append(end)

        # Add to game animations queue
        self.animations.append(anim)  # Assumes we are located in the Game class


    #GUI Call for JAIL
    def GUIpayjail(self):
        #update with GUI call for paying JAIL
        return self.p.player_action == GuiAction.LEAVE_JAIL or self.g.current_player_list(self.current_player)[3] <= 0
    
    def wantsToBuy(self):
        return self.p.player_action == GuiAction.BUY

    #moves player to specified location on board.
    def PlacePlayer(self, Location: str):
        if self.p.dice_roll == -1: return

        oldlocation = 0
        newlocation = 0

        if(Location == "GO"):
            oldlocation = self.g.getoldlocation(self.p.dice_roll, self.current_player)
            newlocation = 0
            self.animationSeqeunce(newlocation, oldlocation)

        if (Location == "AirZandZRental"):
            oldlocation = self.g.getoldlocation(self.p.dice_roll, self.current_player)
            newlocation = 1
            self.animationSeqeunce(newlocation, oldlocation)

        if (Location == "Jail" or Location == "JustVisiting"):
            oldlocation = self.g.getoldlocation(self.p.dice_roll, self.current_player)
            newlocation = 2
            self.animationSeqeunce(newlocation, oldlocation)

        if (Location == "SuburbanTownHouse"):
            oldlocation = self.g.getoldlocation(self.p.dice_roll, self.current_player)
            newlocation = 3
            self.animationSeqeunce(newlocation, oldlocation)

        if (Location == "FreeParking"):
            oldlocation = self.g.getoldlocation(self.p.dice_roll, self.current_player)
            newlocation = 4
            self.animationSeqeunce(newlocation, oldlocation)

        if (Location == "DownTownStudioApt"):
            oldlocation = self.g.getoldlocation(self.p.dice_roll, self.current_player)
            newlocation = 5
            self.animationSeqeunce(newlocation, oldlocation)

        if (Location == "CourtBattle"):
            oldlocation = self.g.getoldlocation(self.p.dice_roll, self.current_player)
            newlocation = 6
            self.animationSeqeunce(newlocation, oldlocation)

        if (Location == "SkyRiseFlat"):
            oldlocation = self.g.getoldlocation(self.p.dice_roll, self.current_player)
            newlocation = 7
            self.animationSeqeunce(newlocation, oldlocation)
        
        self.g.old_location = newlocation

    def animationSeqeunce(self, end: int, begin: int):

        print(end, begin)
        if(begin > end):
            moves = self.p.dice_roll
            self.animationTree(begin, moves)
        elif(begin < end):
            moves = self.p.dice_roll
            self.animationTree(begin, moves)
        elif(end == begin):
            moves = 8
            self.animationTree(begin, moves)

    #animationTree covers the logic of calling animations X number of moves
    def animationTree(self, begin: int, moves: int):
        player = self.current_player - 1
        i = 0
        current = begin
        current = current % 8
        while (i < moves):
            anim = Animation(self.player_objects[player])
            anim.translation(self.positions[current], self.positions[(current + 1) % 8], 30)
            anim.rotation(pyrr.Vector3(self.rotations(current // 2)) + pyrr.Vector3(self.rotation_offsets[player]),
                           pyrr.Vector3(self.rotations((current + 1) // 2)) + pyrr.Vector3(self.rotation_offsets[player]), 30)
            self.animations.append(anim)

            i += 1
            current = (current + 1) % 8

    # GUI Call for house animation Processing for building a house, just moves the house above the board
    def ProcessBuildHouse(self, properity: str):

        action = self.g.buyHouse(properity, self.current_player)
        if((action == "Max number of houses have been built already") or (action == "Not Enough Houses to Sell")):
            # add some error message to end user?
            return

        HouseNumber = action[-1:-1]-1
        actionLoc = action[:-1]

        if (actionLoc == "BuildHouseOnAirZandZRental"):
            house = self.LightBlueHouse_objects[HouseNumber]
            house.set_position.y(0.06)

        if (actionLoc == "BuildHouseOnSuburbanTownHouse"):
            house = self.OrangeHouse_objects[HouseNumber]
            house.set_position.y(0.06)

        if (actionLoc == "BuildHouseOnDownTownStudioApt"):
            house = self.YellowHouse_objects[HouseNumber]
            house.set_position.y(0.06)

        if (actionLoc == "BuildHouseOnSkyRiseFlat"):
            house = self.DarkBlueHouse_objects[HouseNumber]
            house.set_position.y(0.06)


    # GUI Call for house animation Processing for selling a house, just moves the house bellow the board
    def ProcessSellHouse(self, properity: str):

        action = self.g.sellHouse(properity, self.current_player)
        if ((action == "Max number of houses have been built already") or (action == "Not Enough Houses to Sell")):
            #add some error message to end user?
            return

        HouseNumber = action[-1:-1]-1
        actionLoc = action[:-1]

        if (actionLoc == "RemoveHouseOnAirZandZRental"):
            house = self.LightBlueHouse_objects[HouseNumber]
            house.set_position.y(-0.1)
        if (actionLoc == "RemoveHouseOnSuburbanTownHouse"):
            house = self.OrangeHouse_objects[HouseNumber]
            house.set_position.y(-0.1)
        if (actionLoc == "RemoveHouseOnDownTownStudioApt"):
            house = self.YellowHouse_objects[HouseNumber]
            house.set_position.y(-0.1)
        if (actionLoc == "RemoveHouseOnSkyRiseFlat"):
            house = self.DarkBlueHouse_objects[HouseNumber]
            house.set_position.y(-0.1)
