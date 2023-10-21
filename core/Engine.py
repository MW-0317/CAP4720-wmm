import pygame as pg, pyrr, math, numpy as np
from datetime import datetime, timedelta
from OpenGL.GL import *
from core.gui import *
from core.pggui import *
from core.shaderLoader import *
from core.Object import *
from core.Scene import *
from core.Interval import *

class Engine:
    def __init__(self, width: int, height: int):
        self.TPS = 60
        self.INV_TPS = timedelta(seconds=1 / self.TPS)

        self.width = width
        self.height = height

        self.scenes: list[Scene] = []
        
        pg.init()
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        self.opengl_surface     = pg.display.set_mode((width, height), pg.OPENGL | pg.DOUBLEBUF)
        self.gui_surface        = pg.Surface((width, height))

        self.guiManager = guiManager(width, height, self.gui_surface)

        self.draw = True
        glClearColor(0.25, 0.25, 0.25, 1.0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glDepthFunc(GL_LEQUAL)

    def delete(self):
        for scene in self.scenes:
            scene.delete()
        pg.quit()
        quit()
    
    def run(self):
        deltatime = timedelta(0) # Time since last frame
        deltatick = timedelta(0) # Time since last tick
        last_time = datetime.now()
        while self.draw:
            now = datetime.now()
            deltatime = now - last_time
            last_time = now
            deltatick += deltatime

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.draw = False
                
                self.guiManager.run_event(event)

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            self.gui_surface.fill(pg.Color(0.0, 0.0, 0.0, 0.0))

            frame = Frame()
            frame.time = pg.time.get_ticks()
            frame.deltatime = deltatime.seconds
            for scene in self.scenes:
                frame = scene.frame_update(frame)
            self.guiManager.frame_update(frame)

            self.gpuBlit(self.gui_surface, frame)

            while deltatick > self.INV_TPS:
                tick = Tick()
                tick.time = pg.time.get_ticks()
                tick.deltatick = self.INV_TPS.seconds
                for scene in self.scenes:
                    tick = scene.tick_update(tick)
                deltatick = timedelta(seconds=0)
            
            pg.display.flip()
        self.delete()

    def add_scene(self, scene: Scene):
        self.scenes.append(scene)

    def gpuBlit(self, surface: pg.Surface, frame: Frame):
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        width = surface.get_width()
        height = surface.get_height()
        buffer = surface.get_view("1")
        raw_buffer = buffer.raw

        id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, id)
        glTexImage2D(
            GL_TEXTURE_2D,
            0,
            GL_RGBA,
            width,
            height,
            0,
            GL_RGBA,
            GL_UNSIGNED_BYTE,
            raw_buffer
        )
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

        shader = ShaderProgram("resources/shaders/gui/gui.glsl")
        square = Object("resources/objects/square.obj", shader)

        square.draw(frame)

        glDeleteTextures(1, [id])
        glBlendFunc(GL_ONE, GL_ZERO)