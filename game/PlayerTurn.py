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
    DONT_BUY    = 3
    MORTGAGE    = 4
    BANKRUPT    = 5
    LEAVE_JAIL  = 6
    END         = 7

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

        # if player_list[0] < prop_price:
        #     self.engine.guiManager.query_message(f"You have insufficient funds to buy {location_string_fixed}", 300, 300)
        #     return
        
        image, _, _ = self.engine.guiManager.query_image(f"resources/images/{prop}Front.png", self.engine.width // 3, self.engine.width // 3, offset=self.engine.guiManager.width // 5)
        def wantsToBuy(confirmed: bool):
            # if confirmed: gamestate.buy_property(player_index, prop)
            image.kill()
            if confirmed:
                self.player_action = GuiAction.BUY
            else:
                self.player_action = GuiAction.DONT_BUY
            self.should_update_logic = True

        self.engine.guiManager.query_confirmation(f"Would you like to buy {location_string_fixed} for {prop_price}?", 
                                                        self.engine.width // 3, self.engine.width // 3, callback=wantsToBuy, offset=self.engine.guiManager.width // 5)
        
        
    def prompt_jail(self, gamestate: Gamestate, player_index: int):
        player_list = gamestate.current_player_list(player_index)
        if player_list[3] <= 0:
            return
        
        def wantsToPay(pay):
            if pay:
                self.should_update_logic = True
                self.player_action = GuiAction.LEAVE_JAIL
            else:
                self.engine.roll_button.hide()

        self.engine.guiManager.query_confirmation(f"How would you like to leave jail?", self.engine.width // 3, self.engine.width // 3, 
                                                  "Pay $50", "No", callback=wantsToPay)

    def roll_dice(self, gamestate: Gamestate):
        def simulation(ui):
            # TODO: Some simulation
            self.dice = (random.randint(1, 6), random.randint(1, 6))
            if self.engine.cheat_slider.get_value():
                self.dice = (self.engine.dice_slider_1.get_value(), self.engine.dice_slider_2.get_value())
            self.dice_roll = self.dice[0] + self.dice[1]
            self.engine.roll_button.hide()

        self.engine.guiManager.query_message(f"Would you like to roll the dice?", self.engine.width // 3, self.engine.width // 3, callback=simulation)

    def buy_house(self, gamestate: Gamestate):
        ...

    def tick(self, gamestate: Gamestate, player_index: int):
        ...

    def should_end(self):
        return self.player_action == GuiAction.END
    
    def end_turn(self):
        self.player_action = GuiAction.END

    def bankrupt(self, gamestate: Gamestate):
        # TODO
        ...