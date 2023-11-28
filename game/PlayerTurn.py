from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import game.Game as Game
    import core.Engine as Engine

import random

import game.Gamestate as gs
Gamestate = gs.Gamestate

class GuiAction:
    NONE        = 0
    ROLL        = 1
    BUY         = 2
    MORTGAGE    = 3
    BANKRUPT    = 4
    LEAVE_JAIL  = 5
    END         = 6

class PlayerTurn:
    def __init__(self, engine: Game):
        self.engine: Game = engine
        self.player_action = GuiAction.NONE
        self.should_update_logic = False
        self.dice_roll = -1
        self.dice = (-1, -1)

        self.inJail = False
    
    def rent(self, gamestate: Gamestate, player_index: int):
        if gamestate.players[player_index][0] < 0:
            self.bankrupt(gamestate, player_index)

    def buy(self, gamestate: Gamestate, player_index: int, prop: str):
        if not prop.startswith("OfferToBuy"): return
        prop = prop.replace("OfferToBuy", "")

        player_list = gamestate.current_player_list(player_index)

        prop_price = gamestate.get_property_price(prop)
        location_string_fixed = Gamestate.location_spaced_string(prop)
        if player_list[0] < prop_price:
            self.engine.guiManager.query_message(f"You have insufficient funds to buy {location_string_fixed}", 300, 300)
            return

        def wantsToBuy(confirmed: bool):
            # if confirmed: gamestate.buy_property(player_index, prop)
            self.player_action = GuiAction.BUY

        self.engine.guiManager.query_confirmation(f"Would you like to buy {location_string_fixed} for {prop_price}?", 
                                                        300, 300, callback=wantsToBuy)
        
    def prompt_jail(self, gamestate: Gamestate, player_index: int):
        player_list = gamestate.current_player_list(player_index)
        if player_list[3] <= 0:
            return
        
        def wantsToRoll(roll: True):
            if roll:
                self.player_action = GuiAction.LEAVE_JAIL 

        self.engine.guiManager.query_confirmation(f"How would you like to leave jail?", 300, 300, 
                                                  "Pay $50", "No", callback=wantsToRoll)

    def roll_dice(self, gamestate: Gamestate):
        def simulation():
            # TODO: Some simulation
            self.dice = (random.randint(1, 6), random.randint(1, 6))
            if self.engine.cheat_slider.get_value():
                self.dice = (self.engine.dice_slider_1.get_value(), self.engine.dice_slider_2.get_value())
            self.dice_roll = self.dice[0] + self.dice[1]
            print("LastLoc:", gamestate.current_player_list(self.engine.current_player)[1])
            current_loc = (gamestate.current_player_list(self.engine.current_player)[1] + self.dice_roll) % 8
            if self.dice[0] != self.dice[1] or current_loc == 6:
                self.engine.roll_button.hide()

        self.engine.guiManager.query_message(f"Would you like to roll the dice?", 300, 300, callback=simulation)

    def tick(self, gamestate: Gamestate, player_index: int):
        ...

    def should_end(self):
        return self.player_action == GuiAction.END
    
    def end_turn(self):
        self.player_action = GuiAction.END

    def bankrupt(self, gamestate: Gamestate):
        # TODO
        ...