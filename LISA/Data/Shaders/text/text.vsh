#version 130

in vec3 window;
in vec2 texcoord;
out vec2 v_texcoord;

uniform mat4 modelview;
uniform vec2 size;
uniform vec2 corner;

void main()
{
    gl_Position = modelview * vec4(window * vec3(size, 0.) + vec3(corner, 0.), 1.0);
    v_texcoord = texcoord;
}
