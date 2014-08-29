#version 130

in vec3 position;

uniform sampler2D map;
uniform mat4 modelview;
uniform mat4 projection;

void main()
{
    float height = texture2D(map, (position.xy+1)/2).r;
    gl_Position = projection * modelview * vec4(position.x, position.y, 0.4*height, 1.0);
    /* gl_Position = projection * modelview * vec4(position.x, position.y, 0., 1.0); */
}
