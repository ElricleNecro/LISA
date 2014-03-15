#version 130

in vec3 in_Vertex;

uniform sampler2D heighttexture;
uniform mat4 modelview;
uniform float time;

const float amplitude = 0.125;
const float frequency = 2;
const float PI = 3.14159;

void main()
{
    float height = texture(heighttexture, in_Vertex.xy).r * 100;
    gl_Position = modelview * vec4(in_Vertex.x, in_Vertex.y, height, 1.0);
}
