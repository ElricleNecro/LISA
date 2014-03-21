#version 130

in vec3 in_Vertex;

uniform mat4 modelview;
uniform float time;

const float amplitude = 0.125;
const float frequency = 2;
const float PI = 3.14159;

void main()
{
    float distance = length(in_Vertex);
    float y = amplitude * sin(-PI * distance * frequency + time);
    gl_Position = modelview * vec4(in_Vertex.x, in_Vertex.y, y, 1.0);
}
