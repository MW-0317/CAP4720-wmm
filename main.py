from core.Engine import Engine
from core.Scene import Scene
from core.Object import Object, Texture
from core.Camera import Camera
from core.shaderLoader import ShaderProgram

from game.Game import Game

import math

# Texture loading
def load_object_with_texture(object_file, texture_file) -> Object:
    shader = ShaderProgram("resources/shaders/object.glsl")
    textures = [Texture.textureFromFile(texture_file, "mat.albedoTexture")]
    return Object(object_file, shader, textures=textures)

def main():
    width = 800
    height = 600
    g = Game(width, height)
    s = Scene()

    # Board
    o = load_object_with_texture("resources/objects/board.obj", "./resources/images/Gameboard.png")
    o.set_scale([2 / o.diameter] * 3)
    s.add_object(o)

    # Cat (player 1)
    o2 = Object.create_silver_object("resources/objects/cat.obj")
    o2.set_scale([(2 / o2.diameter) / 5] * 3)
    o2.set_position([0, 0, 0])
    o2.set_rotation([math.pi / 2, 0, 0])
    s.add_object(o2)

    # Wolf (player 2)
    o3 = Object.create_silver_object("resources/objects/wolf.obj")
    o3.set_scale([(2 / o3.diameter) / 5] * 3)
    o3.set_position([0, 0.13, 0])
    o3.set_rotation([0, 0, 0])
    s.add_object(o3)

    #Starts Objects in correct location
    o2.set_position([0.5, 0.13, 0.5])
    o2.set_rotation([math.pi / 2, math.pi/2, 0])

    o3.set_position([0.50, 0.13, 0.50])
    o3.set_rotation([0, math.pi / 2, 0])

    # Camera
    c = Camera([0, 1, 2], 45, width / height)
    c.forward = -c.position
    s.add_object(c)

    g.add_scene(s)
    g.run()

if __name__ == "__main__":
    main()