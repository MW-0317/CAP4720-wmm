from core.Engine import Engine
from core.Scene import Scene
from core.Object import Object
from core.shaderLoader import Shader

e = Engine(800, 600)
s = Scene()
shader = Shader("resources/shaders/vert.glsl", "resources/shaders/frag.glsl")
o = Object("resources/objects/wolf.obj", shader)
s.add_object(o)
e.add_scene(s)
e.run()