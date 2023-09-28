import pygame as pg, pyrr, math, numpy as np
from OpenGL.GL import *
from core.guiV1 import *
from core.shaderLoader import *
from core.Object import *
from core.Scene import *

class Engine:
    def __init__(self, width: int, height: int):
        self.scenes: list[Scene] = []

        pg.init()
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.set_mode((width, height), pg.OPENGL, pg.DOUBLEBUF)

        self.draw = True
        glClearColor(1.0, 1.0, 1.0, 1.0)
        glEnable(GL_DEPTH_TEST)

    def __del__(self):
        pg.quit()
        quit()
    
    def run(self):
        while self.draw:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.draw = False

            for scene in self.scenes:
                scene.frame_update()
            
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
                
            pg.display.flip()

    def add_scene(self, scene: Scene):
        self.scenes.append(scene)