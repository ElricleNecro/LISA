#version 130

in vec3 position;

uniform mat4 view;
uniform mat4 model;
uniform mat4 projection;

out vec3 fragNormal;

void main()
{
    gl_Position = projection * view * model * vec4(position, 1.0);

    // compute normals in world space
    fragNormal = mat3(model) * position;
}
