// Version du GLSL

#version 150 core


// Entrées

in vec3 position;
in vec2 in_TexCoord0;


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

    gl_Position = projection * view * model * vec4(position, 1.0);


    // Envoi des coordonnées de texture au Fragment Shader

    coordTexture = in_TexCoord0;
}
