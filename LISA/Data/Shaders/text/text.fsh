#version 130

uniform sampler2D  texture0;
in vec2 v_texcoord;
out vec4 vfragColor;

void main()
{
    vfragColor = texture(texture0, v_texcoord);
}
