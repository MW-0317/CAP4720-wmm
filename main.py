from core.Engine import Engine
from core.Scene import Scene
from core.Object import Object
from core.Camera import Camera
from core.shaderLoader import ShaderProgram

from game.guiSetup import guiSetup

width = 800
height = 600
e = Engine(width, height)
guiSetup(e)
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