#ifdef VERTEX_PROGRAM
layout (location = 0) in vec3 aPosition;
layout (location = 1) in vec2 aTexCoord;
layout (location = 2) in vec3 aNormal;

uniform mat4 model_matrix;
uniform mat4 view_matrix;
uniform mat4 projection_matrix;

out vec3 fPosition;

void main()
{
    fPosition = vec3(aPosition.xy, 0.0);
    vec4 pos = vec4(fPosition, 1.0);
    gl_Position = pos;
}
#endif
#ifdef FRAGMENT_PROGRAM
in vec3 fPosition;

struct ray
{
    vec3 start;
    vec3 direction;
};

struct environment
{
    vec3 eye;
};

struct vertex
{
    vec3 position;
};

struct object
{
    vertex vertices[1000];
};

uniform object objs[1000];

uniform environment env;

out vec4 color;

void main()
{
    ray tRay;
    tRay.start      = fPosition;
    tRay.direction  = normalize(fPosition - env.eye);
    color = vec4(c, 1.0);
}
#endif