from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import game.Game as Game
    import core.Engine as Engine

import random

import game.Gamestate as gs
Gamestate = gs.Gamestate

class PlayerTurn:
    wantsToBuy = False
    dice_roll = -1
    def __init__(self, engine: Engine):
        self.engine: Engine = engine
    
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
            self.wantsToBuy = confirmed

        self.engine.guiManager.query_confirmation(f"Would you like to buy {location_string_fixed} for {prop_price}?", 
                                                        300, 300, callback=wantsToBuy)
        
    def prompt_jail(self, gamestate: Gamestate, player_index: int):
        player_list = gamestate.current_player_list(player_index)
        if player_list[3] <= 0:
            return
        
        def wantsToRoll(roll: True):
            if roll:
                self.roll_dice(gamestate, player_index)

        self.engine.guiManager.query_confirmation(f"How would you like to leave jail?", 300, 300, 
                                                  "Roll!", "Pay $50", callback=wantsToRoll)

    def roll_dice(self, gamestate: Gamestate, player_index: int):
        """
        Provides GUI given a Game class.
        """
        def simulation():
            # TODO: Some simulation
            self.dice_roll = random.randint(1, 6) + random.randint(1, 6)
            # prop = gamestate.gamelocation(dice_val, player_index)
            # self.buy(gamestate, player_index, prop)

        self.engine.guiManager.query_message(f"Would you like to roll the dice?", 300, 300, callback=simulation)
    
    def start_turn(self, gamestate: Gamestate):
        # TODO: Prompt button to roll dice
        PlayerTurn.roll_dice()
        self.wantsToBuy = False
        self.dice_roll = -1
    
    def end_turn(self):
        # TODO
        ...

    def bankrupt(self, gamestate: Gamestate):
        # TODO
        ...