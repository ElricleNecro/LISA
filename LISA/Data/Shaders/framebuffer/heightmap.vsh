#version 330

in vec3 position;

uniform sampler2D map;
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

out vec3 worldPosition;
out vec3 modelPosition;

void main()
{
    float height = texture(map, (position.xy+1)/2).r;
    gl_Position = projection * view * model * vec4(position.x, position.y, 0.4*height, 1.0);
    worldPosition = mat3(model) * vec3(position.x, position.y, 0.4*height);
    modelPosition = position;
}
