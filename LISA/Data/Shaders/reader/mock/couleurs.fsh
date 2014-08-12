#version 130
#pragma debug(on)

out vec4 color;

void main()
{
    vec2 temp = gl_PointCoord - vec2(0.5);

    float f = dot(temp, temp);

    if (f > 0.25) discard;
    color = gl_Color;
}
