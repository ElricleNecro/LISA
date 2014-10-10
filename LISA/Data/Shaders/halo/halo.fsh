#version 330
#pragma debug(on)

uniform float sigma;
uniform float cut_off;
uniform float voxelSize;
uniform vec3 in_color;
out vec4 color;

varying float v_pointsize;

void main()
{
	float x = 2.0 * gl_PointCoord.x - 1.0;
	float y = 2.0 * gl_PointCoord.y - 1.0;
	float a = ( 0.9 - (x*x + y*y) ) * min(1.0, v_pointsize / 1.5);

	color = vec4(in_color, a);
	/* gl_FragColor = color; */
}

/* vim: set ft=glsl */
