from core.Engine import Engine
from core.Interval import Frame
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
        self.player_turn : PlayerTurn = PlayerTurn()
        self.gamestate : Gamestate = Gamestate()

        self.test_gui = SimpleGUI("Debug & Testing")
        self.money_slider = self.test_gui.add_slider("Money", 0, 1500, 0, 10)

        super().__init__(width, height)

        self.guiSetup()

    def frame_update(self, frame: Frame):
        self.gamestate.player1[0] = self.money_slider.get_value()
        #self.money_label.set_text("Money: " + str(self.gamestate.player1[0]))
        super().frame_update(frame)

    def run(self):
        super().run()

    def guiSetup(self):
        help_rect = pg.Rect(0, 0, self.ui_width, self.ui_height * self.height_fraction * 2)
        help = self.guiManager.create_text(self.HELP_MESSAGE, relative_rect=help_rect)
        help.hide()

        money_height = self.ui_height * self.height_fraction * 1 / 2
        money_rect = pg.Rect(self.width - self.ui_width, 0, self.ui_width, money_height)
        self.money_label = self.guiManager.create_label(relative_rect=money_rect, text="Money: " + str(self.gamestate.player1[0]))

        rules_height = self.ui_height * self.height_fraction * 1 / 4
        rules_rect = pg.Rect(self.width - self.ui_width, self.height - rules_height, self.ui_width, rules_height)
        self.guiManager.create_button(relative_rect=rules_rect, text="Rules", callback=help.toggle_visibility)
        #self.guiManager.create_window(self.width / 2 - 100, self.height / 2 - 100, 200, 200)
        self.guiManager.query_confirmation("t", 300, 300, lambda: print("Here"))
    