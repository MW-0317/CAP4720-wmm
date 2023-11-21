from __future__ import annotations

from core.objLoader import ObjLoader
from core.shaderLoader import ShaderProgram
import core.Interval as Interval
from OpenGL.GL import *
import numpy as np
import math
import sys
import pyrr
import pygame as pg

"""
Object class wrapper for given objLoader.py with Texture class wrapper with help
from pygame image loader.
Author: Mark Williams
"""

class Material:
    # Material Types from: https://learnopengl.com/PBR/Theory
    materialTypes = {
        "water"             : [0.02] * 3,
        "plastic low"       : [0.03] * 3,
        "plastic high"      : [0.05] * 3,
        "glass high"        : [0.08] * 3,
        "diamond"           : [0.17] * 3,
        "iron"              : [0.56, 0.57, 0.58],
        "copper"            : [0.95, 0.64, 0.54],
        "gold"              : [1.00, 0.71, 0.29],
        "aluminium"         : [0.91, 0.92, 0.92],
        "silver"            : [0.95, 0.93, 0.88]
    }

    albedo:             pyrr.Vector3    = pyrr.Vector3(materialTypes["silver"])

    mixAmount:          float           = 0.0
    textures:           list[Texture]   = []

    metallic:           float           = 0.0
    roughness:          float           = 1.0

    gamma_correction:   bool            = True

    def __init__(self, roughness, metallic, gamma_correction=True):
        self.metallic = metallic
        self.roughness = roughness
        self.gamma_correction = gamma_correction

    def set_metallic(self, type: str):
        self.albedo = pyrr.Vector3(self.materialTypes[type])

    # Must be called after shader is enabled.
    def enable(self, shader):
        i = 0
        for texture in self.textures:
            texture.enable(i)
            shader[texture.name] = i
            i += 1

        shader_dict = {
            "mat.albedo":       self.albedo,
            
            "mat.mixAmount":    self.mixAmount,
            "mat.numTextures":  len(self.textures),

            "mat.metallic":     self.metallic,
            "mat.roughness":    self.roughness,

            "gamma_correction": self.gamma_correction
        }
        
        shader.from_json(shader_dict)

    def disable(self):
        for texture in self.textures:
            texture.disable()

class Texture:
    @staticmethod
    def load_image(filename, format="RGBA", flip=True):
        surface = pg.image.load(filename)
        image   = pg.image.tobytes(surface, format, flip)

        return surface.get_width(), surface.get_height(), image
    
    @staticmethod
    def create_empty() -> Texture:
        t = Texture(0, "")
        return t
    
    @staticmethod
    def textureFromId(id, name) -> Texture:
        t = Texture(id, name)
        return t
    
    @staticmethod
    def textureFromFile(filename, name) -> Texture:
        id = glGenTextures(1)
        w, h, image = Texture.load_image(filename)
        glBindTexture(GL_TEXTURE_2D, id)
        glTexImage2D(GL_TEXTURE_2D,
                     0,
                     GL_RGBA,
                     w,
                     h,
                     0,
                     GL_RGBA,
                     GL_UNSIGNED_BYTE,
                     image)
        glGenerateMipmap(GL_TEXTURE_2D)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glBindTexture(GL_TEXTURE_2D, 0)
        
        del image
        return Texture.textureFromId(id, name)

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def enable(self, index: int):
        glActiveTexture(GL_TEXTURE0 + index)
        glBindTexture(GL_TEXTURE_2D, self.id)

    def disable(self):
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, 0)

class Object:
    @staticmethod
    def create_silver_object(file, textures: list = []) -> Object:
        shader = ShaderProgram("resources/shaders/object.glsl")
        material = Material(0.5, 1.0)
        material.textures = textures

        return Object(file, shader, textures=textures, material=material)

    def __init__(self, file, shader, *, textures: list = [], material: Material = None):
        if material == None:
            self.material = Material(1.0, 0.0, False)
            self.material.textures = textures
        else:
            self.material = material

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

        self.rotation   = [0, 0, 0]
        self.position   = [0, 0, 0]
        self.scale      = [1, 1, 1]

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
    
    def set_material(self, material: Material):
        self.material = material
    
    def set_textures(self, textures: list):
        self.material.textures = textures
    
    def set_position(self, position: list[float, float, float]):
        self.position = position

    def set_scale(self, scale: list[float, float, float]):
        self.scale = scale

    def set_rotation(self, rotation: list[float, float, float]):
        self.rotation = rotation

    def get_model_matrix(self) -> pyrr.Matrix44:
        """
        Get the Model Matrix for the current object.
        Needs to be optimized.
        The Scale and Rotation matrices must be inverted to place the position
            being set into world space, where the rotation and scale matrices
            are in object space.
        """
        scaleModelMatrix: pyrr.Matrix44 = pyrr.Matrix44(pyrr.matrix44.create_from_scale(self.scale))
        rotModelMatrix: pyrr.Matrix44 = pyrr.Matrix44(pyrr.matrix44.create_from_x_rotation(self.rotation[0]))
        rotModelMatrix = pyrr.matrix44.multiply(rotModelMatrix, pyrr.matrix44.create_from_y_rotation(self.rotation[1]))
        rotModelMatrix = pyrr.matrix44.multiply(rotModelMatrix, pyrr.matrix44.create_from_z_rotation(self.rotation[2]))
        
        rotAndScaleModel = pyrr.matrix44.multiply(rotModelMatrix, scaleModelMatrix)

        newPos = pyrr.matrix44.apply_to_vector(rotAndScaleModel.inverse, pyrr.Vector3(self.position))

        model = pyrr.matrix44.create_from_translation(newPos - pyrr.Vector3(self.center))
        model = pyrr.matrix44.multiply(model, rotAndScaleModel)
        return model
    
    def enable(self):
        glUseProgram(self.shader.id)
        glBindVertexArray(self.vao)
        self.material.enable(self.shader)
        self.shader["sun.position"] = [0.0, 1.0, 0.0, 1.0]
        self.shader["sun.color"]    = [1.0] * 3

    def disable(self):
        glUseProgram(0)
        glBindVertexArray(0)
        self.material.disable()

    def frame_update(self, frame: Interval.Frame) -> Interval.Frame:
        self.draw(frame)
        return frame

    def draw(self, interval: Interval.Interval):
        self.enable()

        self.shader["model_matrix"]         = self.get_model_matrix()
        self.shader["view_matrix"]          = interval.camera.get_view_matrix()
        self.shader["projection_matrix"]    = interval.camera.get_projection_matrix()

        self.shader["env.ao"]               = 1.0
        self.shader["env.eye"]              = interval.camera.position

        glDrawArrays(GL_TRIANGLES, 0, self.n_vertices)
        self.disable()

    def delete(self):
        if (self.vao != None and self.vbo != None):
            glDeleteVertexArrays(1, [self.vao])
            glDeleteBuffers(1, [self.vbo])