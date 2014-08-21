#version 130
#pragma debug(on)

uniform float sigma;
uniform float cut_off;
out vec4 color;

void main()
{

    const vec4 color1 = vec4(0.6, 0.0, 0.0, 1.0);
    const vec4 color2 = vec4(0.9, 0.7, 1.0, 1.0);
    color = color1;

    vec2 temp = gl_PointCoord - vec2(0.5);

    float f = dot(temp, temp);

    if (f > cut_off) discard;
    /* color = mix(color1, color2, smoothstep(0.1, 0.25, f)); */
    color.a = exp(-f / (2*sigma)) / sqrt(2*3.14159 * sigma);
}

/* vim: set ft=glsl */
