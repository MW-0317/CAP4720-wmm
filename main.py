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

    # Houses for Light Blue
    h1 = Object.create_silver_object("resources/objects/house.obj")
    h1.set_scale([(2 / h1.diameter) / 15] * 3)
    h1.set_position([-0.19, -0.1, 0.26])
    h1.set_rotation([0, 0, 0])
    s.add_object(h1)
    g.LightBlueHouse_objects.append(h1)

    h2 = Object.create_silver_object("resources/objects/house.obj")
    h2.set_scale([(2 / h1.diameter) / 15] * 3)
    h2.set_position([-0.095, -0.1, 0.26])
    h2.set_rotation([0, 0, 0])
    s.add_object(h2)
    g.LightBlueHouse_objects.append(h2)

    h3 = Object.create_silver_object("resources/objects/house.obj")
    h3.set_scale([(2 / h1.diameter) / 15] * 3)
    h3.set_position([0.0, -0.1, 0.26])
    h3.set_rotation([0, 0, 0])
    s.add_object(h3)
    g.LightBlueHouse_objects.append(h3)

    h4 = Object.create_silver_object("resources/objects/house.obj")
    h4.set_scale([(2 / h1.diameter) / 15] * 3)
    h4.set_position([0.095, -0.1, 0.26])
    h4.set_rotation([0, 0, 0])
    s.add_object(h4)
    g.LightBlueHouse_objects.append(h4)

    h5 = Object.create_silver_object("resources/objects/house.obj")
    h5.set_scale([(2 / h1.diameter) / 15] * 3)
    h5.set_position([0.19, -0.1, 0.26])
    h5.set_rotation([0, 0, 0])
    s.add_object(h5)
    g.LightBlueHouse_objects.append(h5)

    # Houses for Orange
    h6 = Object.create_silver_object("resources/objects/house.obj")
    h6.set_scale([(2 / h1.diameter) / 15] * 3)
    h6.set_position([-0.26, -0.1, -0.19])
    h6.set_rotation([0, math.pi / 2, 0])
    s.add_object(h6)
    g.OrangeHouse_objects.append(h6)

    h7 = Object.create_silver_object("resources/objects/house.obj")
    h7.set_scale([(2 / h1.diameter) / 15] * 3)
    h7.set_position([-0.26, -0.1, -0.095])
    h7.set_rotation([0, math.pi / 2, 0])
    s.add_object(h7)
    g.OrangeHouse_objects.append(h7)

    h8 = Object.create_silver_object("resources/objects/house.obj")
    h8.set_scale([(2 / h1.diameter) / 15] * 3)
    h8.set_position([-0.26, -0.1, 0.0])
    h8.set_rotation([0, math.pi / 2, 0])
    s.add_object(h8)
    g.OrangeHouse_objects.append(h8)

    h9 = Object.create_silver_object("resources/objects/house.obj")
    h9.set_scale([(2 / h1.diameter) / 15] * 3)
    h9.set_position([-0.26, -0.1, 0.095])
    h9.set_rotation([0, math.pi / 2, 0])
    s.add_object(h9)
    g.OrangeHouse_objects.append(h9)

    h10 = Object.create_silver_object("resources/objects/house.obj")
    h10.set_scale([(2 / h1.diameter) / 15] * 3)
    h10.set_position([-0.26, -0.1, 0.19])
    h10.set_rotation([0, math.pi / 2, 0])
    s.add_object(h10)
    g.OrangeHouse_objects.append(h10)

    # Houses for Yellow
    h11 = Object.create_silver_object("resources/objects/house.obj")
    h11.set_scale([(2 / h1.diameter) / 15] * 3)
    h11.set_position([0.19, -0.1, -0.26])
    h11.set_rotation([0, 0, 0])
    s.add_object(h11)
    g.YellowHouse_objects.append(h11)

    h12 = Object.create_silver_object("resources/objects/house.obj")
    h12.set_scale([(2 / h1.diameter) / 15] * 3)
    h12.set_position([0.095, -0.1, -0.26])
    h12.set_rotation([0, 0, 0])
    s.add_object(h12)
    g.YellowHouse_objects.append(h12)

    h13 = Object.create_silver_object("resources/objects/house.obj")
    h13.set_scale([(2 / h1.diameter) / 15] * 3)
    h13.set_position([0.0, -0.1, -0.26])
    h13.set_rotation([0, 0, 0])
    s.add_object(h13)
    g.YellowHouse_objects.append(h13)

    h14 = Object.create_silver_object("resources/objects/house.obj")
    h14.set_scale([(2 / h1.diameter) / 15] * 3)
    h14.set_position([-0.095, -0.1, -0.26])
    h14.set_rotation([0, 0, 0])
    s.add_object(h14)
    g.YellowHouse_objects.append(h14)

    h15 = Object.create_silver_object("resources/objects/house.obj")
    h15.set_scale([(2 / h1.diameter) / 15] * 3)
    h15.set_position([-0.19, -0.1, -0.26])
    h15.set_rotation([0, 0, 0])
    s.add_object(h15)
    g.YellowHouse_objects.append(h15)

    # Houses for Dark Blue
    h16 = Object.create_silver_object("resources/objects/house.obj")
    h16.set_scale([(2 / h1.diameter) / 15] * 3)
    h16.set_position([0.26, -0.1, 0.19])
    h16.set_rotation([0, math.pi / 2, 0])
    s.add_object(h16)
    g.DarkBlueHouse_objects.append(h16)

    h17 = Object.create_silver_object("resources/objects/house.obj")
    h17.set_scale([(2 / h1.diameter) / 15] * 3)
    h17.set_position([0.26, -0.1, 0.095])
    h17.set_rotation([0, math.pi / 2, 0])
    s.add_object(h17)
    g.DarkBlueHouse_objects.append(h17)

    h18 = Object.create_silver_object("resources/objects/house.obj")
    h18.set_scale([(2 / h1.diameter) / 15] * 3)
    h18.set_position([0.26, -0.1, 0.0])
    h18.set_rotation([0, math.pi / 2, 0])
    s.add_object(h18)
    g.DarkBlueHouse_objects.append(h18)

    h19 = Object.create_silver_object("resources/objects/house.obj")
    h19.set_scale([(2 / h1.diameter) / 15] * 3)
    h19.set_position([0.26, -0.1, -0.095])
    h19.set_rotation([0, math.pi / 2, 0])
    s.add_object(h19)
    g.DarkBlueHouse_objects.append(h19)

    h20 = Object.create_silver_object("resources/objects/house.obj")
    h20.set_scale([(2 / h1.diameter) / 15] * 3)
    h20.set_position([0.26, -0.1, -0.19])
    h20.set_rotation([0, math.pi / 2, 0])
    s.add_object(h20)
    g.DarkBlueHouse_objects.append(h20)

    # Skybox
    skybox_textures = [Texture.cubemapFromFile("resources/textures/skybox", "bmp", "env.texture")]
    shader_skybox = ShaderProgram("resources/shaders/skybox.glsl")
    square_skybox = Object("resources/objects/square.obj", shader_skybox,
                           textures=skybox_textures)
    s.add_object(square_skybox)

    # Cat (player 1)
    o2 = Object.create_silver_object("resources/objects/cat.obj", skybox_textures)
    o2.set_scale([(2 / o2.diameter) / 5] * 3)
    o2.set_position([0, 0, 0])
    o2.set_rotation([math.pi / 2, 0, 0])
    s.add_object(o2)
    g.player_objects.append(o2)

    # Wolf (player 2)
    o3 = Object.create_silver_object("resources/objects/wolf.obj", skybox_textures)
    o3.set_scale([(2 / o3.diameter) / 5] * 3)
    o3.set_position([0, 0.13, 0])
    o3.set_rotation([0, 0, 0])
    s.add_object(o3)
    g.player_objects.append(o3)

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