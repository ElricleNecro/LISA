#version 130

in vec3 in_Vertex;
in vec3 in_Color;
in vec2 in_TexCoord0;

out vec3 color;
out vec2 texCoord0;

uniform mat4 projection;
uniform mat4 modelview;

void main()
{
    gl_Position = projection * modelview * vec4(in_Vertex, 1.0);

    color = in_Color;
    texCoord0 = in_TexCoord0;
}
