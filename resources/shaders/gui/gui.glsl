#ifdef VERTEX_PROGRAM
layout (location = 0) in vec3 aPosition;
layout (location = 1) in vec2 aTexCoord;

out vec3 fPosition;
out vec2 fTexCoord;

void main()
{
    fPosition = vec3(aPosition.xy, 0.0);
    vec4 pos = vec4(fPosition, 1.0);
    fTexCoord = aTexCoord;
    fTexCoord.y = -fTexCoord.y;
    gl_Position = pos;
}
#endif

#ifdef FRAGMENT_PROGRAM

in vec3 fPosition;
in vec2 fTexCoord;

uniform sampler2D GUITexture;

out vec4 outColor;

void main()
{
    vec4 texColor = texture(GUITexture, fTexCoord);
    float temp = texColor.r;
    texColor.r = texColor.b;
    texColor.b = temp;
    outColor = texColor;
}
#endif