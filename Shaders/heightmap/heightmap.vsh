#version 130

in vec3 in_Vertex;

uniform sampler2D heighttexture;
uniform mat4 modelview;

void main()
{
    float height = texture2D(heighttexture, (in_Vertex.xy+1)/2).r;
    gl_Position = modelview * vec4(in_Vertex.x, in_Vertex.y, 0.4*height, 1.0);
}
