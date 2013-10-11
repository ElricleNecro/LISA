#version 130

in vec3 color;
in vec2 texCoord0;

out vec4 out_Color;

uniform sampler2D texture;

void main()
{
    out_Color = texture2D(texture, texCoord0);
}
