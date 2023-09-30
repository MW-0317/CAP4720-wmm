from core.objLoaderV4 import ObjLoader
import core.Interval as Interval
from OpenGL.GL import *
import numpy as np
import math
import sys
import pyrr

class Object:
    def __init__(self, file, shader):
        self.obj = ObjLoader(file)
        if self.obj.v.size == 0:
            return
        self.stride = 0
        if self.obj.v.size > 0:
            self.size_position = self.obj.v[0].size
            self.offset_position = self.stride
            self.stride += self.size_position * 4
        if self.obj.vt.size > 0:
            self.size_texture = self.obj.vt[0].size
            self.offset_texture = self.stride
            self.stride += self.size_texture * 4
        if self.obj.vn.size > 0:
            self.size_normal = self.obj.vn[0].size
            self.offset_normal = self.stride
            self.stride += self.size_normal * 4
        self.n_vertices = self.obj.vertices.size // (self.size_position + self.size_texture + self.size_normal)

        self.center = self.getCenter()
        self.diameter = self.getDiameter()

        self.shader = shader
        glUseProgram(self.shader.id)

        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, 
                    size = self.obj.vertices.nbytes, 
                    data = self.obj.vertices,
                    usage=GL_STATIC_DRAW)
        
        float_size = sys.getsizeof(0.0)
        pos_loc = glGetAttribLocation(shader.id, "aPosition")
        glVertexAttribPointer(index = 0,
                              size = self.size_position,
                              type = GL_FLOAT,
                              normalized = GL_FALSE,
                              stride = self.stride,
                              pointer = ctypes.c_void_p(self.offset_position))
        glEnableVertexAttribArray(0)

        # I could not get glGetAttribLocation to work properly, presumably because
        # OpenGL may optimize attributes and remove them if they are unused
        # from the shaders, I found this information online and would like to know
        # if it is true.
        # Instead I modified the vert.glsl to define the locations of my attributes
        # to 0, 1, and 2 respectively.
        tex_loc = glGetAttribLocation(shader.id, "aTexCoord")
        glVertexAttribPointer(index = 1,
                              size = self.size_texture,
                              type = GL_FLOAT,
                              normalized = GL_FALSE,
                              stride = self.stride,
                              pointer = ctypes.c_void_p(self.offset_texture))
        glEnableVertexAttribArray(1)

        norm_loc = glGetAttribLocation(shader.id, "aNormal")
        glVertexAttribPointer(index = 2,
                              size = self.size_normal,
                              type = GL_FLOAT,
                              normalized = GL_FALSE,
                              stride = self.stride,
                              pointer = ctypes.c_void_p(self.offset_normal))
        glEnableVertexAttribArray(2)

        self.disable()

        self.position = [0, 0, 0]

    def __del__(self):
        self.delete()

    def getCenter(self):
        maxV = self.obj.v.max(axis=0)
        minV = self.obj.v.min(axis=0)
        return np.array([(maxV[i] + minV[i]) / 2 for i in range(0, 3)])
    
    def getDiameter(self):
        maxV = self.obj.v.max(axis=0)
        minV = self.obj.v.min(axis=0)
        diameter = math.sqrt(sum([(maxV[i] - minV[i])**2
                for i in range(0, 3)]))
        return diameter
    
    def set_position(self, position: list[float, float, float]):
        self.position = position

    def get_model_matrix(self) -> pyrr.Matrix44:
        return pyrr.matrix44.create_from_translation(pyrr.Vector3(self.position) - pyrr.Vector3(self.center))
    
    def enable(self):
        glUseProgram(self.shader.id)
        glBindVertexArray(self.vao)

    def disable(self):
        glUseProgram(0)
        glBindVertexArray(0)

    def draw(self, interval: Interval.Interval):
        self.enable()
        model_loc       = glGetUniformLocation(self.shader.id, "model_matrix")
        view_loc        = glGetUniformLocation(self.shader.id, "view_matrix")
        projection_loc  = glGetUniformLocation(self.shader.id, "projection_matrix")

        glUniformMatrix4fv(model_loc,       1, GL_FALSE, self.get_model_matrix())
        glUniformMatrix4fv(view_loc,        1, GL_FALSE, interval.camera.get_view_matrix())
        glUniformMatrix4fv(projection_loc,  1, GL_FALSE, interval.camera.get_projection_matrix())

        glDrawArrays(GL_TRIANGLES, 0, self.n_vertices)
        self.disable()

    def delete(self):
        glDeleteVertexArrays(1, [self.vao])
        glDeleteBuffers(1, [self.vbo])