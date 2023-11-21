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
#define PI 3.141592653

struct material
{
    // Color
    vec3 albedo;

    // Texture
    sampler2D   albedoTexture;
    int         numTextures;

    // PBR
    float       metallic;
    float       roughness;
};
//layout (binding = 0) uniform sampler2D materialTexture;

struct light
{
    vec4        position;
    vec3        color;
};

struct environment
{
    vec3        color;
    vec3        eye;
    samplerCube texture;

    // PBR
    float ao;   // (Ambient Occlusion)
};
//layout (binding = 1) uniform samplerCube environmentTexture;

in vec3 fNormal;
in vec3 fPosition;
in vec2 fTexCoord;

uniform material    mat;
uniform light       sun;
uniform environment env;

uniform bool gamma_correction;

out vec4 fColor;

float microfacetDistributionFunction(float alpha, vec3 N, vec3 H)
{
    float alpha_squared = alpha*alpha;
    float D = alpha_squared / 
                (
                    PI * pow(
                        pow(dot(N, H), 2) * (alpha_squared - 1) + 1
                    , 2)
                );
    return D;
}

float attenuationFactorVector(float alpha, float nDotX)
{
    float k = pow(alpha +  1, 2) / 8;
    float Gx = nDotX / (nDotX * (1.0 - k) + k);
    return Gx;
}

void main()
{
    vec3 currentColor = mat.albedo;

    vec3 normal = normalize(fNormal);
    vec3 viewVector = normalize(env.eye - fPosition);

    // Texture
    vec3 mainColor      = texture(mat.albedoTexture, fTexCoord).xyz;
    vec3 reflectVector  = reflect(-viewVector, normal);
    vec3 envColor       = texture(env.texture, -reflectVector).xyz;

    if (mat.numTextures > 0)
    {
        vec3 textureColor = mix(mainColor, envColor, mat.metallic);
        currentColor = textureColor;
    }

    // Light
    vec3 lightDir = normalize(sun.position.xyz - fPosition * sun.position.w);
    vec3 halfVector = normalize(viewVector + lightDir);

    // PBR Specular:
    // Fresnel term using Schlick's approximation
    vec3 F0 = mix(vec3(0.04), currentColor, mat.metallic);
    vec3 F = F0 + (1 - F0) * 
            pow((1 - dot(viewVector, halfVector)), 5);

    float alpha = mat.roughness*mat.roughness;
    float D = microfacetDistributionFunction(alpha, normal, halfVector);

    float nDotV = clamp(dot(normal, viewVector), 0, 1);
    float nDotL = clamp(dot(normal, lightDir), 0, 1);
    float Gv = attenuationFactorVector(alpha, nDotV);
    float Gl = attenuationFactorVector(alpha, nDotL);
    float G = Gv * Gl;

    vec3 microfacet = (D * F * G);
    vec3 specular = microfacet * sun.color;

    vec3 K_d = 1 - F;
    vec3 diffuse = K_d * (1-mat.metallic) * currentColor * clamp(dot(normal, lightDir), 0, 1);
    vec3 ambient = vec3(0.03) * currentColor * env.ao;
    vec3 color = ambient + specular + diffuse;

    // Gamma correction
    if (gamma_correction)
    {
        color = color / (color + vec3(1.0));
        color = pow(color, vec3(1.0 / 2.2));
    }

    fColor = vec4(color, 1.0);    
}
#endif