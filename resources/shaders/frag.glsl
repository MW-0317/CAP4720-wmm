#version 330 core

in vec3 fragNormal;

out vec4 outColor;

void main()
{
    vec3 fragColor = abs(normalize(fragNormal));
    outColor = vec4(fragColor, 1.0);
}