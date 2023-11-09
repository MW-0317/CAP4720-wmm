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
        self.player_turn : PlayerTurn = PlayerTurn(self)
        self.gamestate : Gamestate = Gamestate()

        self.test_gui = SimpleGUI("Debug & Testing")
        self.money_slider = self.test_gui.add_slider("Money", 0, 1500, 100, 10)
        self.position_slider = self.test_gui.add_slider("Position", 0, 7, 0, 1)
        self.gamestate.player1[0] = self.money_slider.get_value()
        self.gamestate.player1[1] = self.position_slider.get_value()

        super().__init__(width, height)

        self.guiSetup()

    def frame_update(self, frame: Frame):
        # TODO: Temporarily show current player positions using a beam or cylinder
        
        current_player_list = self.gamestate.current_player_list(self.gamestate.current_player)
        current_player_list[0] = self.money_slider.get_value()
        current_player_list[1] = self.position_slider.get_value()
        
        # TODO: Set camera to side of board given position,
        # need to now get this into a function like getCurrentCameraPosition.
        # Would love to introduce camera animations if given time to provide
        # smooth transitions.
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
        self.money_label = self.guiManager.create_label(relative_rect=money_rect, text="Money: " + str(self.gamestate.player1[0]))

        rules_height = self.ui_height * self.height_fraction * 1 / 4
        rules_rect = pg.Rect(self.width - self.ui_width, self.height - rules_height, self.ui_width, rules_height)
        self.guiManager.create_button(relative_rect=rules_rect, text="Rules", callback=lambda ui: help.toggle_visibility())

        self.player_turn.buy(self.gamestate, 1, "OfferToBuyAirZandZRental")