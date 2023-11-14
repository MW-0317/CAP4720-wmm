from core.Engine import Engine
from core.Scene import Scene
from core.Object import Object, Texture
from core.Camera import Camera
from core.shaderLoader import ShaderProgram

from game.Game import Game

# Texture loading
def load_object_with_texture(object_file, texture_file) -> Object:
    shader = ShaderProgram("resources/shaders/object.glsl")
    textures = [Texture(texture_file, "mat.texture")]
    return Object(object_file, shader, textures)

def main():
    width = 800
    height = 600
    g = Game(width, height)
    s = Scene()
    c = Camera([0, 1, 2], 45, width / height)
    c.forward = -c.position
    o = load_object_with_texture("resources/objects/board.obj", "./resources/images/Gameboard.png")
    o.set_scale([0.75, 0.75, 0.75])
    s.add_object(o)
    s.add_object(c)
    g.add_scene(s)
    g.run()

if __name__ == "__main__":
    main()