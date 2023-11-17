from core.Engine import Engine
from core.Scene import Scene
from core.Object import Object, Texture
from core.Camera import Camera
from core.shaderLoader import ShaderProgram

from game.Game import Game

import math

def main():
    width = 800
    height = 600
    g = Game(width, height)
    s = Scene()
    c = Camera([0, 1, 2], 45, width / height)
    c.forward = -c.position
    shader = ShaderProgram("resources/shaders/object.glsl")
    textures = [Texture("./resources/images/Gameboard.png", "materialTexture")]
    o = Object("resources/objects/board.obj", shader, textures)
    o2 = Object("resources/objects/cat.obj", shader, [])
    o.set_scale([2/(o.diameter)] * 3)
    o2.set_scale([(2 / o2.diameter) / 3] * 3)
    o2.set_position([100, 0, 0])
    o2.set_rotation([math.pi / 2, 0, 0])
    s.add_object(o)
    s.add_object(o2)
    s.add_object(c)
    g.add_scene(s)
    g.run()

if __name__ == "__main__":
    main()