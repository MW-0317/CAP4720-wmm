from core.Engine import Engine
from core.Scene import Scene
from core.Object import Object
from core.Camera import Camera
from core.shaderLoader import ShaderProgram

width = 800
height = 600

e = Engine(width, height)
s = Scene()
c = Camera([0, 0, 2], 45, width / height)
shader = ShaderProgram("resources/shaders/example.glsl")
o = Object("resources/objects/wolf.obj", shader)
s.add_object(o)
s.add_object(c)
e.add_scene(s)
e.run()