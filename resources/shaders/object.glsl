#ifdef VERTEX_PROGRAM

layout (location = 0) in vec3 aPosition;
layout (location = 1) in vec2 aTexCoord;
layout (location = 2) in vec3 aNormal;

uniform mat4 model_matrix;
uniform mat4 view_matrix;
uniform mat4 projection_matrix;

out vec3 fNormal;
out vec3 fPos;
out vec2 fTexCoord;

void main()
{
    vec4 tPos = model_matrix * vec4(aPosition, 1.0);
    vec4 pos = projection_matrix * view_matrix * tPos;
    fPos = tPos.xyz;
    gl_Position = pos;

    mat4 normal_matrix = transpose(inverse(model_matrix));
    vec3 new_normal = (normal_matrix * vec4(aNormal, 0)).xyz;
    fNormal = normalize(new_normal);

    fTexCoord = aTexCoord;
}
#endif
#ifdef FRAGMENT_PROGRAM
struct material
{
    vec3        color;
    vec3        specular;
    float       shininess;
    int         textureType;
    float       mixAmount;
};
layout (binding = 0) uniform sampler2D materialTexture;

struct light
{
    vec4        position;
    float       K_s;
};

struct environment
{
    vec3        color;
    vec3        eye;
};
layout (binding = 1) uniform samplerCube environmentTexture;

in vec3 fNormal;
in vec3 fPosition;
in vec2 fTexCoord;

uniform material    mat;
uniform light       sun;
uniform environment env;

out vec4 fColor;

void main()
{
    vec3 currentColor = mat.color;

    vec3 normal = normalize(fNormal);
    vec3 viewVector = normalize(env.eye - fPosition);

    // Texture
    vec3 mainColor      = texture(materialTexture, fTexCoord).xyz;
    vec3 reflectVector  = reflect(-viewVector, normal);
    vec3 envColor       = texture(environmentTexture, -reflectVector).xyz;

    vec3 textureColor = mix(mainColor, envColor, mat.mixAmount);
    currentColor = textureColor;

    // Light
    vec3 lightDir = normalize(sun.position.xyz - fPosition * sun.position.w);
    vec3 diffuse = currentColor * clamp(dot(normal, lightDir), 0, 1);
    
    vec3 halfVector = normalize(viewVector + lightDir);
    float lightIntensity = clamp(dot(normal, halfVector), 0, 1);
    vec3 specular = sun.K_s * mat.specular * pow(lightIntensity, mat.shininess);

    vec3 lightColor = env.color * currentColor + specular + diffuse;

    lightColor = env.color * currentColor;
    
    fColor = vec4(lightColor, 1.0);
}
#endif