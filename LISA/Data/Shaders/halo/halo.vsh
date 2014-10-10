#version 330
#pragma debug(on)

uniform mat4 modelview;
uniform mat4 projection;
/* uniform vec2 screenSize; */
uniform float voxelSize;
uniform float scale;

in vec3 position;

varying float v_pointsize;

void main(void)
{
	vec4 eyePos = modelview * vec4(position, 1);
	gl_Position = projection * eyePos;

	vec4 projVoxel = projection * vec4(voxelSize, voxelSize, eyePos.z, eyePos.w);
	/* vec2 projSize = screenSize * projVoxel.xy / projVoxel.w; */
	gl_PointSize = scale * projVoxel.x / projVoxel.w; //0.25 * (projSize.x+projSize.y);
	v_pointsize = gl_PointSize;
}

/* vim: set ft=glsl */
