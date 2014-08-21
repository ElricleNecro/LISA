#version 130
#pragma debug(on)

uniform mat4 modelview;
uniform mat4 projection;

in vec3 position;

void main(void)
{
    gl_Position = projection * modelview * vec4(position, 1.0);
}
