from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np

VERSION: bytes = "#version 420\n"
SHADERS = [
    (GL_VERTEX_SHADER, "VERTEX"),
    (GL_FRAGMENT_SHADER, "FRAGMENT")
]

def load_shader(shader_file):
    shader_source = ""
    with open(shader_file) as f:
        shader_source = f.read()
    f.close()
    return shader_source

def compile_shader(source, shader_type):
    shader = glCreateShader(shader_type)
    glShaderSource(shader, source)
    glCompileShader(shader)
    result = glGetShaderiv(shader, GL_COMPILE_STATUS)
    if not result:
        raise OpenGL.GL.shaders.ShaderCompilationError("\n\n" + glGetShaderInfoLog( shader ).decode())
    return shader

def compile_program(*s):
    len_s = len(s)
    compiled_shaders = []

    if len_s == 1:
        shader = load_shader(s[0])
        for _shader in SHADERS:
            c_shader = compile_shader(VERSION + "#define " + _shader[1] + "_PROGRAM\n" + shader, _shader[0])
            compiled_shaders.append(c_shader)
    elif len_s == 2:
        vert_shader = load_shader(s[0])
        frag_shader = load_shader(s[1])
        compiled_shaders.append(compile_shader(vert_shader, GL_VERTEX_SHADER))
        compiled_shaders.append(compile_shader(frag_shader, GL_FRAGMENT_SHADER))

    
    program = OpenGL.GL.shaders.compileProgram(*compiled_shaders)
    return program


class ShaderProgram:
    def __init__(self, *s: list[str]):
        self.id = compile_program(*s)

    def __getitem__(self, key):
        return glGetUniformLocation(self.id, key)

    def __setitem__(self, key, value):
        glUseProgram(self.id)
        location = self[key]

        if location != -1:
            if isinstance(value, (int, np.integer)):
                glUniform1i(location, value)
            elif isinstance(value, (float, np.floating)):
                glUniform1f(location, value)
            # for bool
            elif isinstance(value, (bool, np.bool_)):
                glUniform1i(location, value)
            elif isinstance(value, (tuple, list)):
                if len(value) == 3:
                    glUniform3fv(location, 1, value)
                elif len(value) == 4:
                    glUniform4fv(location, 1, value)
            elif isinstance(value, (np.ndarray, np.generic)):
                if value.shape == (4, 4):
                    glUniformMatrix4fv(location, 1, GL_FALSE, value)
                elif value.shape == (3, 3):
                    glUniformMatrix3fv(location, 1, GL_FALSE, value)
                elif value.shape == (4,):
                    glUniform4fv(location, 1, value)
                elif value.shape == (3,):
                    glUniform3fv(location, 1, value)
                elif value.shape == (2,):
                    glUniform2fv(location, 1, value)
                elif value.shape == (1,):
                    glUniform1fv(location, 1, value)
                else:
                    raise ValueError(f"Unsupported matrix shape: {value.shape}")
            else:
                raise ValueError(f"Unsupported value type: {type(value)}")
                # Add more cases for different types of matrices if needed
            # Add more cases for different uniform types if needed


if __name__ == '__main__':
    '''
    Example usage: 

    To use the ShaderProgram class, you need to first create a shader program object by passing the vertex shader and fragment shader
    The ShaderProgram class will compile the shaders and link them to a shader program object
    
    shaderProgram = ShaderProgram("shaders/vert.glsl", "shaders/frag.glsl")
    
    Then you can set the uniform variables in the shader program by using the following syntax:
                        shaderProgram["uniform_name"] = value
    Example:
        shaderProgram["scale"] = (2, 2, 2)
        shaderProgram["model"] = model_mat
        shaderProgram["intensity"] = 0.5
        
    Every time you set a uniform variable, the shader program will be activated and the uniform variable will be set using the following three steps:
        1. glUseProgram(shader)
        2. location = glGetUniformLocation(shader, "uniform_name")
        3. glUniform*(location, 1, value)
        
    The line
        shaderProgram["scale"] = (2, 2, 2) 
    
    is equivalent to:
    
        glUseProgram(shader)
        location = glGetUniformLocation(shader, "scale")
        glUniform3fv(location, 1, (2, 2, 2))
        
        
    '''

    pass