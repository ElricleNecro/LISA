#version 130

in vec3 position;

uniform mat4 modelview;
uniform mat4 projection;

out vec3 texcoord;

void main()
{
    gl_Position = projection * modelview * vec4(position, 1.0);
    texcoord = position;
}
