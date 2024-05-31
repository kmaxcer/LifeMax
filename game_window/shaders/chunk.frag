# version 330 core

layout (location = 0) out vec4 fragColor;

const vec3 gamma = vec3(2.2);
const vec3 inv_gamma = 1 / gamma;

uniform sampler2DArray u_texture_array_0;

in vec3 voxel_color;
in vec2 uv;
in float shading;

flat in int voxel_id;
flat in int face_id;


void main(){
    vec2 face_uv = uv;
    face_uv.x = uv.x / 6.0 - min(face_id, 2) / 6.0;

    float tex_alpha = texture(u_texture_array_0, vec3(face_uv, voxel_id)).a;
    vec3 tex_col = texture(u_texture_array_0, vec3(face_uv, voxel_id)).rgb;
    tex_col = pow(tex_col, gamma);

//    tex_col.rgb *= voxel_color;
    tex_col *= shading;

    tex_col = pow(tex_col, inv_gamma);
    fragColor = vec4(tex_col, tex_alpha);
}