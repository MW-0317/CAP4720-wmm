from core.Engine import Engine
from core.Interval import Frame
from core.Scene import Scene
from core.Object import Object
from core.Camera import Camera
from core.pggui import Frame
from core.shaderLoader import ShaderProgram
from game.PlayerTurn import PlayerTurn

from core.gui import *

class Game(Engine):
    HELP_MESSAGE = """<font size=5> Where's My Money -- Help </font>
    <p> Where's my money is a simple version of the classic board game monopoly. </p>
    """
    def __init__(self, width: int, height: int):
        # To be replaced with self.game_state, 
        # where player turn can be accessed from.
        self.current_player : PlayerTurn = PlayerTurn()

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
    