#version 130
#pragma debug(on)

uniform mat4 modelview;
uniform mat4 projection;
uniform vec2 screenSize;
uniform float voxelSize;

in vec3 position;
in vec3 color;

void main(void)
{
    vec4 eyePos = modelview * vec4(position, 1);
    vec4 projVoxel = projection * vec4(voxelSize, voxelSize, eyePos.z, eyePos.w);
    vec2 projSize = screenSize * projVoxel.xy / projVoxel.w;
    gl_PointSize = 0.25 * (projSize.x+projSize.y);
    gl_Position = projection * eyePos;
    gl_FrontColor = vec4(color, 1);
}
