// Version du GLSL

#version 150 core


// Entrées

in vec3 position;


// Uniform

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;


// Sortie

out vec2 coordTexture;


// Fonction main

void main()
{
    // Position finale du vertex en 3D

    vec2 inter = position.xy - 0.5;
    gl_Position = projection * view * model * vec4(inter.xy, 0, 1.0);


    // Envoi des coordonnées de texture au Fragment Shader

    coordTexture = position.xy;
}
