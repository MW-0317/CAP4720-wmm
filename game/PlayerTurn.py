from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import game.Game as Game
    import core.Engine as Engine

import random

import game.Gamestate as Gamestate

class PlayerTurn:
    def __init__(self, engine: Engine):
        self.engine: Engine = engine

    def rent(self, gamestate: Gamestate, player_index):
        if gamestate.players[player_index][0] < 0:
            self.bankrupt(gamestate, player_index)

    def buy(self, gamestate: Gamestate, player_index, property_index):
        if gamestate.players[player_index][0] < 0:
            self.bankrupt(gamestate, player_index)

        wantsToBuy = True
        if wantsToBuy and gamestate.players[player_index][0] > gamestate.properties[property_index][0]:
            ...

        player_list = gamestate.current_player_list(player_index)

        def wantsToBuy(confirmed: bool):
            # TODO
            ...

        location = player_list[1]
        location_string = gamestate.gamelocation(location, 1)
        location_string_fixed = Gamestate.location_spaced_string(location_string)
        self.engine.guiManager.query_confirmation(f"Would you like to buy {location_string_fixed}", 
                                                        300, 300, callback=wantsToBuy)

    def roll_dice(self, gamestate: Gamestate) -> int:
        """Provides GUI given a Game class and returns
        the rolled dice value.
        """
        # TODO: Animation / Simulation
        return random.randint(1,6)
    
    def start_turn(self, gamestate: Gamestate):
        # TODO: Prompt button to roll dice
        dice_roll = PlayerTurn.roll_dice()
    
    def end_turn(self):
        # TODO
        ...

    def bankrupt(self, gamestate: Gamestate):
        # TODO
        ...