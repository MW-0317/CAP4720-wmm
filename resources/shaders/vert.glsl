#version 330 core

layout (location = 0) in vec3 aPosition;
layout (location = 1) in vec2 aTexCoord;
layout (location = 2) in vec3 aNormal;

uniform float aspect;

uniform mat4 model_matrix;
uniform mat4 view_matrix;
uniform mat4 projection_matrix;

out vec3 fragNormal;

void main()
{
    vec4 pos = projection_matrix * view_matrix * model_matrix * vec4(aPosition, 1.0);
    gl_Position = pos;

    mat4 normal_matrix = transpose(inverse(model_matrix));
    vec3 new_normal = (normal_matrix * vec4(aNormal, 0)).xyz;
    fragNormal = normalize(new_normal);
}