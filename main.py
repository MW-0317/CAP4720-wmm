from core.Engine import Engine
from core.Scene import Scene
from core.Object import Object, Texture
from core.Camera import Camera
from core.shaderLoader import ShaderProgram

from game.Game import Game

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
    o.set_scale([0.75, 0.75, 0.75])
    s.add_object(o)
    s.add_object(c)
    g.add_scene(s)
    g.run()

if __name__ == "__main__":
    main()