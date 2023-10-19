from core.Engine import Engine
from core.Scene import Scene
from core.Object import Object
from core.Camera import Camera
from core.shaderLoader import ShaderProgram

width = 1000
height = 800

e = Engine(width, height)
def testPrint():
    print("Hello World!")
e.guiManager.create_button(width - 200, height - 100, 200, 100, text="Rules",
                           callback=testPrint)
e.guiManager.create_text(width - 200, 0, 200, 100, "Test")
s = Scene()
c = Camera([0, 1, 2], 45, width / height)
c.forward = -c.position
shader = ShaderProgram("resources/shaders/example.glsl")
o = Object("resources/objects/board.obj", shader)
o.set_scale([0.75, 0.75, 0.75])
s.add_object(o)
s.add_object(c)
e.add_scene(s)
e.run()