#version 130

in vec3 position;

uniform mat4 projection;
uniform mat4 modelview;
uniform float time;

const float amplitude = 0.125;
const float frequency = 2;
const float PI = 3.14159;

void main()
{
    float distance = length(position);
    float y = amplitude * sin(-PI * distance * frequency + time);
    gl_Position = projection * modelview * vec4(position.x, position.y, y, 1.0);
}
