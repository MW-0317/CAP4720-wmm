import pygame as pg, pyrr, math, numpy as np
from datetime import datetime, timedelta
from OpenGL.GL import *
from core.gui import *
from core.shaderLoader import *
from core.Object import *
from core.Scene import *
from core.Interval import *

class Engine:
    def __init__(self, width: int, height: int):
        self.TPS = 60
        self.INV_TPS = timedelta(1 / self.TPS)

        self.scenes: list[Scene] = []

        pg.init()
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.set_mode((width, height), pg.OPENGL | pg.DOUBLEBUF)

        self.draw = True
        glClearColor(0.25, 0.25, 0.25, 1.0)
        glEnable(GL_DEPTH_TEST)

    def delete(self):
        for scene in self.scenes:
            scene.delete()
        pg.quit()
        quit()
    
    def run(self):
        deltatime = timedelta() # Time since last frame
        deltatick = timedelta() # Time since last tick
        last_time = datetime.now()
        while self.draw:
            now = datetime.now()
            deltatime = now - last_time
            last_time = now
            deltatick += deltatime

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.draw = False

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            frame = Frame(deltatime)
            for scene in self.scenes:
                frame = scene.frame_update(frame)

            if deltatick > self.INV_TPS:
                tick = Tick(deltatick)
                for scence in self.scenes:
                    tick = scene.tick_update(tick)
            
            pg.display.flip()
        self.delete()

    def add_scene(self, scene: Scene):
        self.scenes.append(scene)