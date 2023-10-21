from core.Engine import Engine
from core.Scene import Scene
from core.Object import Object
from core.Camera import Camera
from core.shaderLoader import ShaderProgram

def helpBox():
    print("test")

def guiSetup(e: Engine):
    help = e.guiManager.create_text(0, 0, 200, 200, "Test")
    help.hide()
    e.guiManager.create_button(e.width - 200, e.height - 100, 200, 100, text="Rules",
                            callback=e.guiManager.ui_elements[0].toggle_visibility)
    e.guiManager.create_label(e.width - 400, 0, 400, 100, "Where's My Money?")
