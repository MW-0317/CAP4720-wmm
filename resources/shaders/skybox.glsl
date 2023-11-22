#ifdef VERTEX_PROGRAM
layout (location = 0) in vec3 aPosition;
layout (location = 1) in vec2 aTexCoord;

out vec3 fPosition;
out vec2 fTexCoord;

void main()
{
    fPosition = vec3(aPosition.xy, 1.0);
    vec4 pos = vec4(fPosition, 1.0);
    fTexCoord = aTexCoord;
    fTexCoord.y = -fTexCoord.y;
    gl_Position = pos;
}
#endif

#ifdef FRAGMENT_PROGRAM

in vec3 fPosition;
in vec2 fTexCoord;

struct environment
{
    samplerCube texture;
};

uniform mat4 view_matrix;
uniform environment env;

out vec4 outColor;

void main()
{
     mat4 view_matrix_wo_translation = view_matrix;
    view_matrix_wo_translation[3] = vec4(0.0, 0.0, 0.0, view_matrix[3][3]);
    mat4 invViewProjMatrix = inverse(projection_matrix * view_matrix_wo_translation);
    vec4 inverseFragPos = invViewProjMatrix * vec4(fPos, 1.0);
    vec3 dir = normalize(inverseFragPos.xyz / inverseFragPos.w);
    vec3 envColor = texture(env.texture, -dir).xyz;
    outColor = vec4(envColor, 1.0);
}
#endif