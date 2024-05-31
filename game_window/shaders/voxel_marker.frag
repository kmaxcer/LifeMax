#version 330 core

layout (location=0) out vec4 fragColor;

in vec2 uv;

uniform sampler2D u_texture_0;

void main(){
    fragColor = texture(u_texture_0, uv);
//    fragColor.rgb += marker_color;
    fragColor.a = 0.4;
}