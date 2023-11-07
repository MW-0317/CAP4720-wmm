from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import game.Game as Game

import random

class GameState:
    players = [(0, 0)] # list of tuples that contain player position and money
    properties = [()]
    game = None

    def run(game: Game.Game):
        game.run()

class PlayerTurn:
    def rent(gamestate: GameState, player_index):
        if gamestate.players[player_index][0] < 0:
            PlayerTurn.bankrupt(gamestate, player_index)

    def buy(gamestate: GameState, player_index, property_index):
        if gamestate.players[player_index][0] < 0:
            PlayerTurn.bankrupt(gamestate, player_index)
        # TODO: Prompt and ask if they'd like to buy
        # game.guiManager.queryConfirmation(f"Would you like to buy ${gamestate.properties[property_index][...]}", confirm_callback)
        wantsToBuy = True
        if wantsToBuy and gamestate.players[player_index][0] > gamestate.properties[property_index][0]:
            ...

    def roll_dice(gamestate: GameState) -> int:
        """Provides GUI given a Game class and returns
        the rolled dice value.
        """
        # TODO: Animation / Simulation
        return random.randint(1,6)
    
    def start_turn(gamestate: GameState):
        # TODO: Prompt button to roll dice
        dice_roll = PlayerTurn.roll_dice()
    
    def end_turn(self):
        # TODO
        ...

    def bankrupt(gamestate: GameState):
        # TODO
        ...